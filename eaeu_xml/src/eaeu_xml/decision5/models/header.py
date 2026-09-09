from dataclasses import dataclass
from typing import Any

from eaeu_xml.decision5.models.action import ApplicationAction, FaultAction, SignalAction
from eaeu_xml.decision5.models.address import LogicalAddress
from eaeu_xml.decision5.models.identifiers import ConversationId, MessageId, ProcedureId


@dataclass(frozen=True)
class EndpointReference:
    address: LogicalAddress


@dataclass(frozen=True)
class RelatesTo:
    message_id: MessageId
    relates_action: str | None = None


@dataclass(frozen=True)
class SoapHeader:
    to: LogicalAddress
    reply_to: EndpointReference | None
    action: ApplicationAction | SignalAction | FaultAction
    message_id: MessageId
    procedure_id: ProcedureId
    conversation_id: ConversationId
    relates_to: RelatesTo | None = None
    from_: EndpointReference | None = None
    fault_to: EndpointReference | None = None
    integration: Any | None = None


HEADER_ELEMENT_ORDER = (
    "to", "reply_to", "from_", "fault_to", "message_id", "relates_to",
    "action", "procedure_id", "conversation_id", "integration",
)
