from dataclasses import dataclass, field
from datetime import datetime, timedelta

from eaeu_xml.core.enums import MessageKind, TransactionPattern, TransactionState
from eaeu_xml.decision5.models.action import ApplicationAction, FaultAction, SignalAction
from eaeu_xml.decision5.models.identifiers import ConversationId, MessageId
from eaeu_xml.decision5.models.procedure import ProcedureInstance


@dataclass(frozen=True)
class MessageRecord:
    message_id: MessageId
    action: ApplicationAction | SignalAction | FaultAction
    created_at: datetime
    sequence_number: int
    message_kind: MessageKind
    relates_to: MessageId | None = None
    retry_of: MessageId | None = None
    attempt_number: int = 1
    transition_id: str | None = None


@dataclass(frozen=True)
class TransactionParameters:
    receive_confirmation_timeout: timedelta | None = None
    processing_confirmation_timeout: timedelta | None = None
    response_timeout: timedelta | None = None
    retry_count: int = 0

    def __post_init__(self) -> None:
        durations = (self.receive_confirmation_timeout, self.processing_confirmation_timeout, self.response_timeout)
        if self.retry_count < 0 or any(value is not None and value.total_seconds() <= 0 for value in durations):
            from eaeu_xml.core.errors import TransactionPatternError
            raise TransactionPatternError(code="D5_PARAMETERS_INVALID", rule_id="D5-TRN-PARAMETERS", message="Параметры времени должны быть положительными, число повторов — неотрицательным.")


@dataclass(frozen=True)
class TransactionDefinition:
    pattern: TransactionPattern
    parameters: TransactionParameters = TransactionParameters()
    guaranteed_delivery: bool = False


@dataclass
class TransactionInstance:
    transaction_code: str
    conversation_id: ConversationId
    procedure_instance: ProcedureInstance
    message_history: list[MessageRecord] = field(default_factory=list)
    state: TransactionState = TransactionState.NEW
    definition: TransactionDefinition | None = None
    retry_attempts: int = 0
