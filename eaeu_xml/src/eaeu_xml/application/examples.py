from dataclasses import dataclass
from typing import Any
import re


@dataclass(frozen=True)
class ResolvedExample:
    value: Any = None
    origin: str = "UNAVAILABLE"
    unavailable_reason: str | None = None


class ExampleValueResolver:
    """Produces documentation examples from explicit metadata and unambiguous datatypes."""

    def resolve(self, *, datatype: str | None, description: str | None, fixed_value=None,
                allowed_values=(), existing_value=None, classifier=False,
                pattern: str | None = None) -> ResolvedExample:
        def valid(value):
            if not pattern:
                return True
            try:
                return re.fullmatch(pattern, str(value)) is not None
            except re.error:
                return False

        if fixed_value is not None and valid(fixed_value):
            return ResolvedExample(fixed_value, "FIXED_VALUE")
        for value in allowed_values:
            if valid(value):
                return ResolvedExample(value, "ALLOWED_VALUE")
        if existing_value is not None and valid(existing_value):
            return ResolvedExample(existing_value, "TEST_DATA_GENERATOR")
        dtype=(datatype or "").casefold(); local_type=dtype.rsplit(":",1)[-1]; description_text=(description or "").casefold()
        if dtype == "any_xml" or "anyxml" in dtype:
            return ResolvedExample(unavailable_reason="ANY_XML")
        candidates = []
        if "uuid" in dtype or "universallyuniqueid" in dtype:
            candidates.append(("d1f6f86c-029a-4245-bb91-433a6aa79987", "DATATYPE_EXAMPLE"))
        elif "countrycode" in dtype:
            candidates.append(("RU", "DATATYPE_EXAMPLE"))
        elif "language" in dtype:
            candidates.append(("ru", "DATATYPE_EXAMPLE"))
        elif "datetime" in dtype:
            candidates.append(("2026-08-24T15:24:00+03:00", "DATATYPE_EXAMPLE"))
        elif dtype.endswith("datetype") or dtype.endswith(":date") or dtype == "date":
            candidates.append(("2026-08-24", "DATATYPE_EXAMPLE"))
        elif "boolean" in dtype or "indicator" in dtype:
            candidates.append(("true", "DATATYPE_EXAMPLE"))
        elif "decimal" in dtype:
            candidates.append(("10.5", "DATATYPE_EXAMPLE"))
        elif "identifier" in dtype or "idtype" in dtype or re.fullmatch(r"id\d*type", local_type):
            candidates.append(("123456", "DATATYPE_EXAMPLE"))
        elif any(token in dtype for token in ("integer", "quantity", "ordinal", "number")):
            candidates.append(("10", "DATATYPE_EXAMPLE"))
        elif "phone" in dtype:
            candidates.append(("+79991234567", "DATATYPE_EXAMPLE"))
        elif "email" in dtype:
            candidates.append(("example@example.com", "DATATYPE_EXAMPLE"))
        elif "url" in dtype or "urtype" in local_type:
            candidates.append(("https://example.com", "DATATYPE_EXAMPLE"))
        if any(token in description_text for token in ("наименование организации","наименование юридического лица","наименование хозяйствующего субъекта")):
            candidates.append(("ООО «Пример»", "PROJECT_DOCUMENTATION"))
        if not classifier and any(token in dtype for token in ("string", "text", "name")):
            candidates.append(("Пример текстового значения", "DATATYPE_EXAMPLE"))
        for value, origin in candidates:
            if valid(value):
                return ResolvedExample(value, origin)
        if pattern:
            if valid("2026/RU-123456"):
                return ResolvedExample("2026/RU-123456", "PATTERN_EXAMPLE")
            return ResolvedExample(unavailable_reason="PATTERN_EXAMPLE_UNAVAILABLE")
        if classifier:
            return ResolvedExample(unavailable_reason="CLASSIFIER_NOT_AVAILABLE")
        if any(token in dtype for token in ("binary","base64","hex")):
            return ResolvedExample(unavailable_reason="BUSINESS_VALUE_NOT_SAFE_TO_INVENT")
        return ResolvedExample(unavailable_reason="INSUFFICIENT_METADATA")
