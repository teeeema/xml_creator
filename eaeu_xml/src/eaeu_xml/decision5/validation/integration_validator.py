from eaeu_xml.core.errors import IntegrationOwnershipError, IntegrationValidationError
from eaeu_xml.decision5.models.integration import IntegrationMetadata


class IntegrationValidator:
    def validate(self, integration: IntegrationMetadata) -> None:
        if integration.track_id is None or integration.accept_time is None:
            raise IntegrationValidationError(code="D5_INTEGRATION_REQUIRED", rule_id="D5-INTEGRATION-STRUCTURE", message="Integration требует TrackID и AcceptTime.")


class IntegrationOwnershipValidator:
    def validate_application_input(self, integration: object | None) -> None:
        if integration is not None:
            raise IntegrationOwnershipError(code="D5_INTEGRATION_OWNER", rule_id="D5-INTEGRATION-OWNER", message="Integration формирует интеграционная платформа.")
