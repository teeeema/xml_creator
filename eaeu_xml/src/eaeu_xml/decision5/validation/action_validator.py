from eaeu_xml.decision5.models.action import ApplicationAction


class ActionValidator:
    def validate(self, action: ApplicationAction) -> None:
        ApplicationAction.parse(action.serialize())
