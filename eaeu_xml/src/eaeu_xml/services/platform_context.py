from dataclasses import replace
from datetime import datetime, timezone
from uuid import uuid4

from eaeu_xml.decision5.models.integration import AcceptTime, IntegrationMetadata, TrackId
from eaeu_xml.decision5.validation.integration_validator import IntegrationValidator


class IntegrationPlatformContext:
    def create_metadata(self, *, track_id: TrackId | None = None, accept_time: AcceptTime | None = None) -> IntegrationMetadata:
        return IntegrationMetadata(
            track_id or TrackId(f"urn:uuid:{uuid4()}"),
            accept_time or AcceptTime(datetime.now(timezone.utc)),
        )

    def enrich(self, message, metadata: IntegrationMetadata):
        IntegrationValidator().validate(metadata)
        return replace(message, header=replace(message.header, integration=metadata))
