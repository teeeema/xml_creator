"""Two-phase, ProcessPackage-aware reconstruction of persisted sessions."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from eaeu_xml.application.session_snapshot import (
    SessionPersistenceService, SessionSnapshotError, SessionSnapshotValidator,
    TransactionSessionSnapshot,
)
from eaeu_xml.application.message_artifacts import SessionBundlePersistenceService
from eaeu_xml.core.enums import MessageKind, SignalKind, TransactionPattern, TransactionState
from eaeu_xml.decision5.models.action import ApplicationAction, FaultAction, SignalAction
from eaeu_xml.decision5.models.identifiers import ConversationId, MessageId, ProcedureId
from eaeu_xml.decision5.models.procedure import ProcedureInstance
from eaeu_xml.decision5.models.transaction import (
    MessageRecord, TransactionDefinition as RuntimeTransactionDefinition,
    TransactionInstance, TransactionParameters,
)
from eaeu_xml.decision5.validation.retry_validator import RetryValidator
from eaeu_xml.decision5.validation.transaction_validator import TransactionValidator
from eaeu_xml.services.transaction_engine import TransactionEngine


class SessionRestoreStatus(str, Enum):
    RESTORABLE = "RESTORABLE"
    SNAPSHOT_INVALID = "SNAPSHOT_INVALID"
    PROCESS_NOT_FOUND = "PROCESS_NOT_FOUND"
    PROCESS_VERSION_MISMATCH = "PROCESS_VERSION_MISMATCH"
    TRANSACTION_NOT_FOUND = "TRANSACTION_NOT_FOUND"
    TRANSACTION_DEFINITION_MISMATCH = "TRANSACTION_DEFINITION_MISMATCH"
    MESSAGE_DEFINITION_MISMATCH = "MESSAGE_DEFINITION_MISMATCH"
    ACTION_INVALID = "ACTION_INVALID"
    DIRECTION_INVALID = "DIRECTION_INVALID"
    CORRELATION_INVALID = "CORRELATION_INVALID"
    RETRY_INVALID = "RETRY_INVALID"
    SIGNAL_INVALID = "SIGNAL_INVALID"
    FAULT_INVALID = "FAULT_INVALID"
    STATE_INVALID = "STATE_INVALID"
    TIMING_REVALIDATION_REQUIRED = "TIMING_REVALIDATION_REQUIRED"


@dataclass(frozen=True)
class SessionRestoreResult:
    status: SessionRestoreStatus
    session: object | None = None
    issues: tuple[str, ...] = ()
    timing_status: str = "CURRENT"

    @property
    def continue_ready(self) -> bool:
        return self.status is SessionRestoreStatus.RESTORABLE and self.session is not None


@dataclass(frozen=True)
class SessionOpenResult:
    """Application-layer result for opening a snapshot path in an interactive client."""
    restore: SessionRestoreResult
    snapshot: TransactionSessionSnapshot | None = None
    path: object | None = None

    @property
    def status(self):return self.restore.status

    @property
    def continue_ready(self):return self.restore.continue_ready


class TransactionSessionRestoreService:
    def __init__(self, application):
        self.application = application
        self.snapshot_validator = SessionSnapshotValidator()
        self.persistence = SessionPersistenceService(self.snapshot_validator)

    def restore_path(self, path, *, seed=0):
        try:
            snapshot = self.persistence.load(path)
        except SessionSnapshotError as error:
            return SessionRestoreResult(SessionRestoreStatus.SNAPSHOT_INVALID, issues=(f"{error.code}: {error.message}",))
        return self.restore(snapshot, seed=seed)

    def restore(self, snapshot: TransactionSessionSnapshot, *, seed=0) -> SessionRestoreResult:
        structural = self.snapshot_validator.validate(snapshot)
        if structural.errors:
            return self._structural_failure(structural.errors)
        if structural.warnings:
            return SessionRestoreResult(SessionRestoreStatus.TIMING_REVALIDATION_REQUIRED,
                                        issues=structural.warnings, timing_status="REVALIDATION_REQUIRED")
        try:
            engine = self.application._engine(snapshot.process_code)
        except KeyError as error:
            return SessionRestoreResult(SessionRestoreStatus.PROCESS_NOT_FOUND, issues=(str(error),))
        current_version = engine.package.profile.process_version
        if snapshot.process_version != current_version:
            return SessionRestoreResult(SessionRestoreStatus.PROCESS_VERSION_MISMATCH,
                issues=(f"snapshot={snapshot.process_version}; current={current_version}",))
        try:
            definition = engine.get_transaction(snapshot.transaction_code)
        except Exception as error:
            return SessionRestoreResult(SessionRestoreStatus.TRANSACTION_NOT_FOUND, issues=(str(error),))
        mismatch = self._definition_mismatch(snapshot, definition)
        if mismatch:
            return SessionRestoreResult(SessionRestoreStatus.TRANSACTION_DEFINITION_MISMATCH, issues=tuple(mismatch))
        semantic = self._message_semantics(snapshot, engine, definition)
        if semantic:
            return semantic
        candidate = self._rebuild(snapshot, definition)
        if isinstance(candidate, SessionRestoreResult):
            return candidate
        transaction, metadata = candidate
        try:
            TransactionValidator().validate(transaction)
        except Exception as error:
            return SessionRestoreResult(SessionRestoreStatus.CORRELATION_INVALID, issues=(str(error),))
        if transaction.state.value != snapshot.current_state:
            return SessionRestoreResult(SessionRestoreStatus.STATE_INVALID,
                issues=(f"snapshot={snapshot.current_state}; replay={transaction.state.value}",))
        from eaeu_xml.application.facade import TransactionSession
        session = TransactionSession._from_validated_restore(
            self.application, snapshot, transaction, metadata, seed=seed)
        if session.create_snapshot() != snapshot:
            return SessionRestoreResult(SessionRestoreStatus.SNAPSHOT_INVALID,
                                        issues=("RUNTIME_ROUNDTRIP_MISMATCH",))
        return SessionRestoreResult(SessionRestoreStatus.RESTORABLE, session=session)

    @staticmethod
    def _structural_failure(errors):
        mapping = {
            "PROCESS_VERSION_MISMATCH": SessionRestoreStatus.PROCESS_VERSION_MISMATCH,
            "SESSION_IDENTIFIER_OR_STATE_INVALID": SessionRestoreStatus.STATE_INVALID,
            "BROKEN_RELATES_TO": SessionRestoreStatus.CORRELATION_INVALID,
            "DUPLICATE_MESSAGE_ID": SessionRestoreStatus.CORRELATION_INVALID,
            "BROKEN_RETRY_OF": SessionRestoreStatus.RETRY_INVALID,
            "RETRY_CHAIN_INVALID": SessionRestoreStatus.RETRY_INVALID,
        }
        status = next((mapping[item] for item in errors if item in mapping), SessionRestoreStatus.SNAPSHOT_INVALID)
        return SessionRestoreResult(status, issues=tuple(errors))

    @staticmethod
    def _definition_mismatch(snapshot, definition):
        issues = []
        if snapshot.procedure_code != definition.procedure_code:
            issues.append("PROCEDURE_CODE_MISMATCH")
        if snapshot.transaction_pattern != definition.pattern:
            issues.append("TRANSACTION_PATTERN_MISMATCH")
        if snapshot.guaranteed_delivery != definition.guaranteed_delivery:
            issues.append("GUARANTEED_DELIVERY_MISMATCH")
        expected = {**definition.timeouts, "retry_count": definition.retry_count}
        if dict(snapshot.transaction_parameters) != expected:
            issues.append("TRANSACTION_PARAMETERS_MISMATCH")
        return issues

    @staticmethod
    def _message_semantics(snapshot, engine, definition):
        application_records = [item for item in snapshot.history if item.message_kind == MessageKind.APPLICATION.value]
        if snapshot.history and (not application_records or application_records[0] is not snapshot.history[0]):
            return SessionRestoreResult(SessionRestoreStatus.MESSAGE_DEFINITION_MISMATCH,
                                        issues=("INITIAL_APPLICATION_MESSAGE_REQUIRED",))
        for index, item in enumerate(snapshot.history):
            if item.direction != "SENT":
                return SessionRestoreResult(SessionRestoreStatus.DIRECTION_INVALID,
                                            issues=(f"Unsupported runtime direction at history[{index}]",))
            if item.message_kind == MessageKind.APPLICATION.value:
                allowed = {definition.initiating_message, *definition.response_messages}
                if item.message_code not in allowed or item.message_code not in engine.messages:
                    return SessionRestoreResult(SessionRestoreStatus.MESSAGE_DEFINITION_MISMATCH,
                                                issues=(f"Unknown transaction message: {item.message_code}",))
                if index == 0 and item.message_code != definition.initiating_message:
                    return SessionRestoreResult(SessionRestoreStatus.MESSAGE_DEFINITION_MISMATCH,
                                                issues=("INITIAL_MESSAGE_MISMATCH",))
                expected = engine.build_application_action(definition.transaction_code, item.message_code).serialize()
                if item.action != expected:
                    return SessionRestoreResult(SessionRestoreStatus.ACTION_INVALID,
                                                issues=(f"Action mismatch: {item.message_code}",))
        return None

    def _rebuild(self, snapshot, definition):
        procedure = ProcedureInstance(snapshot.procedure_code, ProcedureId.parse(snapshot.procedure_id))
        transaction = TransactionInstance(snapshot.transaction_code, ConversationId.parse(snapshot.conversation_id),
            procedure, definition=self._runtime_definition(definition))
        runtime = TransactionEngine()
        metadata = {}
        known = {}
        latest_application = None
        retry_attempts = 0
        for index, item in enumerate(snapshot.history):
            message_id = MessageId.parse(item.message_id)
            relates_to = MessageId.parse(item.relates_to) if item.relates_to else None
            retry_of = MessageId.parse(item.retry_of) if item.retry_of else None
            kind = MessageKind(item.message_kind)
            try:
                if kind is MessageKind.APPLICATION:
                    action = ApplicationAction.parse(item.action)
                elif kind is MessageKind.SIGNAL:
                    source = known.get(relates_to)
                    if source is None or source.message_kind is not MessageKind.APPLICATION:
                        return SessionRestoreResult(SessionRestoreStatus.SIGNAL_INVALID, issues=("SIGNAL_SOURCE_INVALID",))
                    action = SignalAction(source.action, SignalKind(item.signal_kind).value)
                    if action.serialize() != item.action or latest_application != relates_to:
                        return SessionRestoreResult(SessionRestoreStatus.SIGNAL_INVALID, issues=("SIGNAL_CORRELATION_INVALID",))
                else:
                    action = FaultAction(item.action)
                    source = known.get(relates_to)
                    source_item = next((record for record in snapshot.history if record.message_id == item.relates_to), None)
                    if source is None or source_item is None or item.relates_action != source_item.action:
                        return SessionRestoreResult(SessionRestoreStatus.FAULT_INVALID, issues=("FAULT_CORRELATION_INVALID",))
            except Exception as error:
                status = SessionRestoreStatus.SIGNAL_INVALID if kind is MessageKind.SIGNAL else SessionRestoreStatus.FAULT_INVALID if kind is MessageKind.TECHNICAL_FAULT else SessionRestoreStatus.ACTION_INVALID
                return SessionRestoreResult(status, issues=(str(error),))
            record = MessageRecord(message_id, action, datetime.fromisoformat(item.created_at),
                item.sequence_number, kind, relates_to, retry_of, item.attempt_number, item.transition_id)
            try:
                if index == 0:
                    transaction.message_history.append(record)
                    transaction.state = runtime.state_machine.after_initial(transaction)
                    latest_application = message_id
                elif retry_of:
                    original = known.get(retry_of)
                    if original is None:
                        raise ValueError("retry predecessor missing")
                    RetryValidator().validate(original, record)
                    if original is not transaction.message_history[-1] or retry_attempts >= transaction.definition.parameters.retry_count:
                        raise ValueError("retry predecessor/state is not permitted")
                    transaction.message_history.append(record)
                    retry_attempts += 1
                    latest_application = message_id
                elif kind is MessageKind.APPLICATION:
                    if relates_to != latest_application:
                        return SessionRestoreResult(SessionRestoreStatus.CORRELATION_INVALID,
                                                    issues=("APPLICATION_RELATESTO_SEMANTIC_MISMATCH",))
                    transaction.message_history.append(record)
                    runtime.receive_application_message(transaction)
                    latest_application = message_id
                elif kind is MessageKind.SIGNAL:
                    transaction.message_history.append(record)
                    runtime.receive_signal(transaction, SignalKind(item.signal_kind))
                else:
                    transaction.message_history.append(record)
                    runtime.receive_fault(transaction)
            except Exception as error:
                status = SessionRestoreStatus.RETRY_INVALID if retry_of else SessionRestoreStatus.STATE_INVALID
                return SessionRestoreResult(status, issues=(str(error),))
            known[message_id] = record
            metadata[item.message_id] = {
                "message_code": item.message_code, "direction": item.direction,
                "signal_kind": item.signal_kind, "fault_kind": item.fault_kind,
                "relates_action": item.relates_action,
            }
        transaction.retry_attempts = retry_attempts
        if retry_attempts != snapshot.retry_attempts:
            return SessionRestoreResult(SessionRestoreStatus.RETRY_INVALID,
                                        issues=("RETRY_ATTEMPT_TOTAL_MISMATCH",))
        return transaction, metadata

    @staticmethod
    def _runtime_definition(definition):
        def duration(name):
            value = definition.timeouts.get(name)
            seconds = SessionSnapshotValidator._duration_seconds(value) if value else None
            return timedelta(seconds=seconds) if seconds else None
        return RuntimeTransactionDefinition(TransactionPattern[definition.pattern], TransactionParameters(
            receive_confirmation_timeout=duration("receive_confirmation"),
            processing_confirmation_timeout=duration("processing_confirmation"),
            response_timeout=duration("response"), retry_count=definition.retry_count or 0,
        ), bool(definition.guaranteed_delivery))


class TransactionSessionLifecycleService:
    def __init__(self, application):
        self.application = application

    def create_new(self, process_code, transaction_code, *, seed=0):
        from eaeu_xml.application.facade import TransactionSession
        return TransactionSession(self.application, process_code, transaction_code, seed)

    def restore_existing(self, snapshot, *, seed=0):
        return TransactionSessionRestoreService(self.application).restore(snapshot, seed=seed)

    def open_existing(self, path, *, seed=0):
        bundle_service=SessionBundlePersistenceService()
        try:
            bundle=bundle_service.load(path);snapshot=bundle.snapshot;artifacts=bundle.artifacts
        except SessionSnapshotError as bundle_error:
            persistence=SessionPersistenceService()
            try:snapshot=persistence.load_candidate(path);artifacts=()
            except SessionSnapshotError as error:
                result=SessionRestoreResult(SessionRestoreStatus.SNAPSHOT_INVALID,issues=(f"{error.code}: {error.message}",))
                return SessionOpenResult(result,None,path)
        result=self.restore_existing(snapshot,seed=seed)
        if result.continue_ready:
            result.session.message_artifacts={item.message_id_ref:item for item in artifacts}
            result.session.artifact_persistence_available=bool(artifacts)
        return SessionOpenResult(result,snapshot,path)
