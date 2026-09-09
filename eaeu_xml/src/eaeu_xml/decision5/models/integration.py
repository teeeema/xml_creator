from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlparse
from uuid import UUID

from eaeu_xml.core.errors import IntegrationValidationError


@dataclass(frozen=True)
class TrackId:
    value: str

    def __post_init__(self) -> None:
        parsed = urlparse(self.value)
        if parsed.scheme != "urn" or not self.value.startswith("urn:uuid:"):
            raise IntegrationValidationError(code="D5_TRACK_ID_URI", rule_id="D5-INTEGRATION-TRACK", message="TrackID должен быть UUID в URI-представлении urn:uuid.")
        try:
            UUID(self.value[9:])
        except ValueError as error:
            raise IntegrationValidationError(code="D5_TRACK_ID_UUID", rule_id="D5-INTEGRATION-TRACK", message="TrackID должен содержать UUID RFC 4122.") from error

    def serialize(self) -> str:
        return self.value


@dataclass(frozen=True)
class AcceptTime:
    value: datetime

    def __post_init__(self) -> None:
        if self.value.tzinfo is None or self.value.utcoffset() is None:
            raise IntegrationValidationError(code="D5_ACCEPT_TIME_TZ", rule_id="D5-INTEGRATION-TIME", message="AcceptTime должен содержать часовой пояс.")
        if self.value.utcoffset().total_seconds() != 0:
            raise IntegrationValidationError(code="D5_ACCEPT_TIME_UTC", rule_id="D5-INTEGRATION-TIME", message="AcceptTime должен быть указан в UTC.")

    def serialize(self) -> str:
        return self.value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class IntegrationMetadata:
    track_id: TrackId
    accept_time: AcceptTime
