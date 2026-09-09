"""Versioned, portable persistence for Decision No. 5 transaction state."""

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Mapping

from eaeu_xml.core.enums import MessageKind, SignalKind, TransactionPattern, TransactionState
from eaeu_xml.decision5.models.action import ApplicationAction, FaultAction, SignalAction
from eaeu_xml.decision5.models.identifiers import ConversationId, MessageId, ProcedureId
from eaeu_xml.decision5.validation.correlation_validator import CorrelationValidator


SESSION_SNAPSHOT_VERSION = 1
SESSION_SUFFIX = ".eaeusession.json"
_DIRECTIONS = {"SENT", "RECEIVED"}


class SessionSnapshotError(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class SessionMessageSnapshot:
    sequence_number: int
    message_code: str | None
    direction: str
    action: str
    message_id: str
    relates_to: str | None
    relates_action: str | None
    created_at: str
    attempt_number: int
    retry_of: str | None
    message_kind: str
    signal_kind: str | None = None
    fault_kind: str | None = None
    transition_id: str | None = None
    procedure_id: str | None = None
    conversation_id: str | None = None


@dataclass(frozen=True)
class TransactionSessionSnapshot:
    session_snapshot_version: int
    created_at: str
    updated_at: str
    process_code: str
    process_version: str
    transaction_code: str
    procedure_code: str
    transaction_pattern: str
    guaranteed_delivery: bool | None
    transaction_parameters: Mapping[str, object]
    procedure_id: str
    conversation_id: str
    current_state: str
    retry_attempts: int
    history: tuple[SessionMessageSnapshot, ...]

    @classmethod
    def from_transaction(
        cls, transaction, *, process_code: str, process_version: str,
        transaction_pattern: str, guaranteed_delivery: bool | None = None,
        transaction_parameters: Mapping[str, object] | None = None,
        directions: Mapping[str, str] | None = None,
        record_metadata: Mapping[str, Mapping[str, object]] | None = None,
        created_at: str | None = None, updated_at: str | None = None,
    ) -> "TransactionSessionSnapshot":
        now = datetime.now(timezone.utc).isoformat()
        directions = directions or {}
        record_metadata = record_metadata or {}
        history = []
        for record in transaction.message_history:
            action = record.action.serialize()
            metadata = record_metadata.get(record.message_id.serialize(), {})
            message_code = metadata.get("message_code", record.action.message_code if isinstance(record.action, ApplicationAction) else None)
            signal_kind = metadata.get("signal_kind", record.action.signal_code if isinstance(record.action, SignalAction) else None)
            fault_kind = metadata.get("fault_kind", str(record.action) if isinstance(record.action, FaultAction) else None)
            history.append(SessionMessageSnapshot(
                sequence_number=record.sequence_number,
                message_code=message_code,
                direction=str(metadata.get("direction", directions.get(record.message_id.serialize(), "SENT"))),
                action=action,
                message_id=record.message_id.serialize(),
                relates_to=record.relates_to.serialize() if record.relates_to else None,
                relates_action=metadata.get("relates_action"),
                created_at=record.created_at.isoformat(),
                attempt_number=record.attempt_number,
                retry_of=record.retry_of.serialize() if record.retry_of else None,
                message_kind=record.message_kind.value,
                signal_kind=signal_kind,
                fault_kind=fault_kind,
                transition_id=record.transition_id,
                procedure_id=transaction.procedure_instance.procedure_id.serialize(),
                conversation_id=transaction.conversation_id.serialize(),
            ))
        return cls(
            SESSION_SNAPSHOT_VERSION, created_at or now, updated_at or now, process_code, process_version,
            transaction.transaction_code, transaction.procedure_instance.procedure_code,
            transaction_pattern, guaranteed_delivery, dict(transaction_parameters or {}),
            transaction.procedure_instance.procedure_id.serialize(),
            transaction.conversation_id.serialize(), transaction.state.value,
            transaction.retry_attempts, tuple(history),
        )


@dataclass(frozen=True)
class SessionSnapshotValidationResult:
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def continue_ready(self) -> bool:
        return not self.errors and not any(item.startswith("TIMING_REVALIDATION_REQUIRED") for item in self.warnings)


class SessionSnapshotValidator:
    """Strict structural and typed correlation validator; it performs no restore."""

    def validate(
        self, snapshot: TransactionSessionSnapshot, *, current_process_version: str | None = None,
        now: datetime | None = None,
    ) -> SessionSnapshotValidationResult:
        errors = []
        warnings = []
        if snapshot.session_snapshot_version != SESSION_SNAPSHOT_VERSION:
            errors.append("UNSUPPORTED_SESSION_SNAPSHOT_VERSION")
        if not snapshot.process_code or not snapshot.process_version or not snapshot.transaction_code or not snapshot.procedure_code:
            errors.append("SESSION_CONTEXT_REQUIRED")
        if current_process_version is not None and snapshot.process_version != current_process_version:
            errors.append("PROCESS_VERSION_MISMATCH")
        try:
            procedure_id = ProcedureId.parse(snapshot.procedure_id)
            conversation_id = ConversationId.parse(snapshot.conversation_id)
            state = TransactionState(snapshot.current_state)
            self._validate_pattern(snapshot.transaction_pattern)
        except Exception:
            errors.append("SESSION_IDENTIFIER_OR_STATE_INVALID")
            return SessionSnapshotValidationResult(tuple(dict.fromkeys(errors)), tuple(warnings))
        if snapshot.retry_attempts < 0:
            errors.append("RETRY_ATTEMPTS_INVALID")
        if state is TransactionState.NEW and snapshot.history:
            errors.append("NEW_STATE_HISTORY_NOT_EMPTY")
        if state is not TransactionState.NEW and not snapshot.history:
            errors.append("SESSION_HISTORY_REQUIRED")

        known = {}
        records = []
        for index, item in enumerate(snapshot.history, 1):
            try:
                message_id = MessageId.parse(item.message_id)
                relates_to = MessageId.parse(item.relates_to) if item.relates_to else None
                retry_of = MessageId.parse(item.retry_of) if item.retry_of else None
                created_at = datetime.fromisoformat(item.created_at)
                if created_at.tzinfo is None:
                    raise ValueError("naive timestamp")
                kind = MessageKind(item.message_kind)
                if item.direction not in _DIRECTIONS or item.sequence_number != index or item.attempt_number < 1:
                    raise ValueError("record shape")
                if item.procedure_id and ProcedureId.parse(item.procedure_id) != procedure_id:
                    errors.append("MESSAGE_PROCEDURE_ID_MISMATCH")
                if item.conversation_id and ConversationId.parse(item.conversation_id) != conversation_id:
                    errors.append("MESSAGE_CONVERSATION_ID_MISMATCH")
            except Exception:
                errors.append("MESSAGE_HISTORY_INVALID")
                continue
            if message_id in known:
                errors.append("DUPLICATE_MESSAGE_ID")
                continue
            if relates_to and relates_to not in known:
                errors.append("BROKEN_RELATES_TO")
            if retry_of and retry_of not in known:
                errors.append("BROKEN_RETRY_OF")
            self._validate_action(snapshot, item, kind, known, errors)
            if retry_of in known:
                original = known[retry_of]
                if item.attempt_number != original.attempt_number + 1 or item.action != original.action or item.message_code != original.message_code:
                    errors.append("RETRY_CHAIN_INVALID")
            known[message_id] = item
            try:
                records.append(self._core_record(item, message_id, relates_to, retry_of, kind, created_at))
            except Exception:
                if "ACTION_OR_MESSAGE_TYPE_INVALID" not in errors:
                    errors.append("ACTION_OR_MESSAGE_TYPE_INVALID")

        if not errors:
            from eaeu_xml.decision5.models.procedure import ProcedureInstance
            from eaeu_xml.decision5.models.transaction import TransactionInstance
            transaction = TransactionInstance(snapshot.transaction_code, conversation_id,
                ProcedureInstance(snapshot.procedure_code, procedure_id), records, state, retry_attempts=snapshot.retry_attempts)
            try:
                CorrelationValidator().validate_history(transaction)
            except Exception:
                errors.append("CORRELATION_GRAPH_INVALID")
        if self._timing_needs_revalidation(snapshot, now or datetime.now(timezone.utc)):
            warnings.append("TIMING_REVALIDATION_REQUIRED: saved transaction may be stale")
        return SessionSnapshotValidationResult(tuple(dict.fromkeys(errors)), tuple(warnings))

    @staticmethod
    def _validate_pattern(value: str) -> None:
        if value not in {*(item.name for item in TransactionPattern), *(item.value for item in TransactionPattern)}:
            raise ValueError("unknown pattern")

    @staticmethod
    def _validate_action(snapshot, item, kind, known, errors):
        try:
            if kind is MessageKind.APPLICATION:
                action = ApplicationAction.parse(item.action)
                if not item.message_code or action.message_code != item.message_code or action.process_code != snapshot.process_code or action.process_version != snapshot.process_version or action.procedure_code != snapshot.procedure_code or action.transaction_code != snapshot.transaction_code:
                    raise ValueError("application action mismatch")
                if item.signal_kind or item.fault_kind or item.relates_action:
                    raise ValueError("application subtype metadata")
            elif kind is MessageKind.SIGNAL:
                if not item.signal_kind or item.message_code or item.fault_kind or not item.relates_to:
                    raise ValueError("signal metadata")
                source = known.get(MessageId.parse(item.relates_to))
                source_action = ApplicationAction.parse(source.action) if source and source.message_kind == MessageKind.APPLICATION.value else None
                if source_action is None or SignalAction(source_action, SignalKind(item.signal_kind).value).serialize() != item.action:
                    raise ValueError("signal action mismatch")
            else:
                if item.message_code or item.signal_kind or not item.fault_kind or not item.relates_to or not item.relates_action:
                    raise ValueError("fault metadata")
                FaultAction(item.action)
                source = known.get(MessageId.parse(item.relates_to))
                if source is None or item.relates_action != source.action:
                    raise ValueError("fault correlation")
        except Exception:
            errors.append("ACTION_OR_MESSAGE_TYPE_INVALID")

    @staticmethod
    def _core_record(item, message_id, relates_to, retry_of, kind, created_at):
        from eaeu_xml.decision5.models.transaction import MessageRecord
        if kind is MessageKind.APPLICATION:
            action = ApplicationAction.parse(item.action)
        elif kind is MessageKind.SIGNAL:
            # The SignalAction was already checked against its source record.
            # CorrelationValidator consumes only record identity/graph fields.
            action = item.action
        else:
            action = FaultAction(item.action)
        return MessageRecord(message_id, action, created_at, item.sequence_number, kind,
                             relates_to, retry_of, item.attempt_number, item.transition_id)

    @staticmethod
    def _timing_needs_revalidation(snapshot, now):
        if snapshot.current_state not in {"WAITING_RECEIVED", "WAITING_PROCESSING", "WAITING_RESPONSE", "WAITING_RESPONSE_RECEIVED", "WAITING_RESPONSE_PROCESSING", "WAITING_FINAL_ERROR_WINDOW"}:
            return False
        if not snapshot.history:
            return True
        timing_keys = {"receive_confirmation", "processing_confirmation", "response",
                       "receive_confirmation_timeout", "processing_confirmation_timeout", "response_timeout"}
        durations = [SessionSnapshotValidator._duration_seconds(value) for key, value in snapshot.transaction_parameters.items()
                     if key in timing_keys]
        durations = [value for value in durations if value]
        if not durations:
            return True
        last = datetime.fromisoformat(snapshot.history[-1].created_at)
        return now > last + timedelta(seconds=max(durations))

    @staticmethod
    def _duration_seconds(value):
        if isinstance(value, (int, float)) and value > 0:
            return float(value)
        match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?", str(value))
        return (int(match.group(1) or 0) * 3600 + int(match.group(2) or 0) * 60 +
                float(match.group(3) or 0)) if match else None


class SessionPersistenceService:
    def __init__(self, validator: SessionSnapshotValidator | None = None):
        self.validator = validator or SessionSnapshotValidator()

    def save(self, snapshot: TransactionSessionSnapshot, path: Path) -> Path:
        result = self.validator.validate(snapshot)
        if result.errors:
            raise SessionSnapshotError("SESSION_SNAPSHOT_INVALID", ", ".join(result.errors))
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(asdict(snapshot), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        temporary = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                             prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if temporary and temporary.exists():
                temporary.unlink()
        return path

    def load(self, path: Path) -> TransactionSessionSnapshot:
        snapshot=self.load_candidate(path)
        result = self.validator.validate(snapshot)
        if result.errors:
            raise SessionSnapshotError("SESSION_SNAPSHOT_INVALID", ", ".join(result.errors))
        return snapshot

    def load_candidate(self, path: Path) -> TransactionSessionSnapshot:
        """Decode schema only; callers must pass the candidate to the strict restore service."""
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise SessionSnapshotError("SESSION_SNAPSHOT_INVALID_JSON", "Session snapshot is not valid UTF-8 JSON.") from error
        return self._decode(data)

    @staticmethod
    def _decode(data) -> TransactionSessionSnapshot:
        if not isinstance(data, dict):
            raise SessionSnapshotError("SESSION_SNAPSHOT_OBJECT_REQUIRED", "Session snapshot root must be an object.")
        if data.get("session_snapshot_version") != SESSION_SNAPSHOT_VERSION:
            raise SessionSnapshotError("UNSUPPORTED_SESSION_SNAPSHOT_VERSION", f"Unsupported session_snapshot_version: {data.get('session_snapshot_version')}")
        required = {field.name for field in TransactionSessionSnapshot.__dataclass_fields__.values()}
        missing = sorted(required - data.keys())
        unknown = sorted(data.keys() - required)
        if missing or unknown:
            raise SessionSnapshotError("SESSION_SNAPSHOT_SCHEMA_INVALID", f"Missing={missing}; unknown={unknown}")
        if not isinstance(data["history"], list) or not isinstance(data["transaction_parameters"], dict):
            raise SessionSnapshotError("SESSION_SNAPSHOT_SCHEMA_INVALID", "history/transaction_parameters have invalid types")
        records = []
        record_fields = {field.name for field in SessionMessageSnapshot.__dataclass_fields__.values()}
        try:
            for item in data["history"]:
                if not isinstance(item, dict) or set(item) != record_fields:
                    raise ValueError("record schema")
                records.append(SessionMessageSnapshot(**item))
            return TransactionSessionSnapshot(**{**data, "history": tuple(records)})
        except (TypeError, ValueError) as error:
            raise SessionSnapshotError("SESSION_SNAPSHOT_SCHEMA_INVALID", "Session snapshot field types are invalid.") from error
