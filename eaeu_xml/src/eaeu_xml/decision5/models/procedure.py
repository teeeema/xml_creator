from dataclasses import dataclass

from eaeu_xml.decision5.models.identifiers import ProcedureId


@dataclass(frozen=True)
class ProcedureInstance:
    procedure_code: str
    procedure_id: ProcedureId
    parent: "ProcedureInstance | None" = None

    def start_child(self, procedure_code: str, identifier_service: object) -> "ProcedureInstance":
        return ProcedureInstance(procedure_code, self.procedure_id.child(identifier_service), self)
