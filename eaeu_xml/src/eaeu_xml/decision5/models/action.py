from dataclasses import dataclass
import re

from eaeu_xml.core.errors import ActionValidationError


PROCESS = re.compile(r"P\.[A-Z]{2}\.[0-9]{2}")
VERSION = re.compile(r"[0-9]+(?:\.[0-9]+)+")
PROCEDURE = re.compile(r"P\.[A-Z]{2}\.[0-9]{2}\.PRC\.[0-9]{3}")
TRANSACTION = re.compile(r"P\.[A-Z]{2}\.[0-9]{2}\.TRN\.[0-9]{3}")
MESSAGE = re.compile(r"P\.[A-Z]{2}\.[0-9]{2}\.MSG\.[0-9]{3}")


@dataclass(frozen=True)
class ApplicationAction:
    process_code: str
    process_version: str
    procedure_code: str
    transaction_code: str
    message_code: str
    address_space: str = "CP"

    def __post_init__(self) -> None:
        checks = (
            (PROCESS, self.process_code), (VERSION, self.process_version),
            (PROCEDURE, self.procedure_code), (TRANSACTION, self.transaction_code),
            (MESSAGE, self.message_code),
        )
        if self.address_space != "CP" or any(pattern.fullmatch(value) is None for pattern, value in checks):
            raise ActionValidationError(code="D5_ACTION_FORMAT", rule_id="D5-ACTION-APPLICATION", message="Некорректный формат Action.")
        prefix = self.process_code + "."
        if not self.procedure_code.startswith(prefix) or not self.transaction_code.startswith(prefix):
            raise ActionValidationError(code="D5_ACTION_PROCESS_MISMATCH", rule_id="D5-ACTION-APPLICATION", message="Коды процедуры и транзакции не согласованы с общим процессом.")

    @classmethod
    def build(cls, **components: str) -> "ApplicationAction":
        return cls(**components)

    def serialize(self) -> str:
        return f"int://{self.address_space}/" + "/".join((self.process_code, self.process_version, self.procedure_code, self.transaction_code, self.message_code))

    @classmethod
    def parse(cls, value: str) -> "ApplicationAction":
        if not value.startswith("int://CP/"):
            raise ActionValidationError(code="D5_ACTION_FORMAT", rule_id="D5-ACTION-APPLICATION", message="Action должен начинаться с int://CP/.")
        parts = value[len("int://CP/"):].split("/")
        if len(parts) != 5:
            raise ActionValidationError(code="D5_ACTION_FORMAT", rule_id="D5-ACTION-APPLICATION", message="Action должен содержать пять компонентов сведений.")
        return cls(*parts)


@dataclass(frozen=True)
class SignalAction:
    application_context: ApplicationAction
    signal_code: str

    def __post_init__(self) -> None:
        if self.signal_code not in {"P.MSG.RCV", "P.MSG.PRS", "P.MSG.ERR"}:
            raise ActionValidationError(code="D5_SIGNAL_ACTION", rule_id="D5-SIGNAL-ACTION", message="Неизвестный код сигнала.")

    def serialize(self) -> str:
        base = self.application_context
        return f"int://CP/{base.process_code}/{base.process_version}/{base.procedure_code}/{base.transaction_code}/{self.signal_code}"


class FaultAction(str):
    WSA = "http://www.w3.org/2005/08/addressing/fault"
    GENERIC = "http://www.w3.org/2005/08/addressing/soap/fault"

    def __new__(cls, value: str) -> "FaultAction":
        if value not in {cls.WSA, cls.GENERIC}:
            raise ActionValidationError(code="D5_FAULT_ACTION", rule_id="D5-FAULT-ACTION", message="Неизвестный Action технологической ошибки.")
        return str.__new__(cls, value)

    def serialize(self) -> str:
        return str(self)
