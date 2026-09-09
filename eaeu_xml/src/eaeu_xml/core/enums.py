from enum import Enum


class MessageKind(str, Enum):
    APPLICATION = "APPLICATION"
    SIGNAL = "SIGNAL"
    TECHNICAL_FAULT = "TECHNICAL_FAULT"


class SignalKind(str, Enum):
    RECEIVED = "P.MSG.RCV"
    ACCEPTED_FOR_PROCESSING = "P.MSG.PRS"
    ERROR = "P.MSG.ERR"


class TransactionPattern(str, Enum):
    MUTUAL_OBLIGATIONS = "Взаимные обязательства"
    QUESTION_RESPONSE = "Вопрос/ответ"
    REQUEST_RESPONSE = "Запрос/ответ"
    REQUEST_CONFIRMATION = "Запрос/подтверждение"
    NOTIFICATION = "Оповещение"
    INFORMATION_DISTRIBUTION = "Распространение информации"


class HeaderFieldStatus(str, Enum):
    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"
    FORBIDDEN = "FORBIDDEN"
    DERIVED = "DERIVED"
    PLATFORM_GENERATED = "PLATFORM_GENERATED"


class LogicalAddressSpace(str, Enum):
    CP = "CP"
    CA = "CA"
    SR = "SR"


class SegmentKind(str, Enum):
    EEC = "EEC"
    MEMBER_STATE = "MEMBER_STATE"


class TransactionState(str, Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    WAITING_RECEIVED = "WAITING_RECEIVED"
    WAITING_PROCESSING = "WAITING_PROCESSING"
    WAITING_RESPONSE = "WAITING_RESPONSE"
    WAITING_RESPONSE_RECEIVED = "WAITING_RESPONSE_RECEIVED"
    WAITING_RESPONSE_PROCESSING = "WAITING_RESPONSE_PROCESSING"
    WAITING_FINAL_ERROR_WINDOW = "WAITING_FINAL_ERROR_WINDOW"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ROLLBACK_REQUIRED = "ROLLBACK_REQUIRED"


class TimeoutKind(str, Enum):
    RECEIVE_CONFIRMATION = "RECEIVE_CONFIRMATION"
    PROCESSING_CONFIRMATION = "PROCESSING_CONFIRMATION"
    RESPONSE = "RESPONSE"


class TimeoutOutcome(str, Enum):
    RETRY = "RETRY"
    FAIL = "FAIL"
    COMPLETE = "COMPLETE"
