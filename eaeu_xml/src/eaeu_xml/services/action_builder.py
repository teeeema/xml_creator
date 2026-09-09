from eaeu_xml.decision5.models.action import ApplicationAction


class ActionBuilder:
    def build_application(self, *, process_code: str, process_version: str, procedure_code: str, transaction_code: str, message_code: str) -> ApplicationAction:
        return ApplicationAction.build(
            process_code=process_code, process_version=process_version,
            procedure_code=procedure_code, transaction_code=transaction_code, message_code=message_code,
        )
