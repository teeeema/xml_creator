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
                allowed_values=(), existing_value=None, classifier=False) -> ResolvedExample:
        if fixed_value is not None: return ResolvedExample(fixed_value, "FIXED_VALUE")
        if allowed_values: return ResolvedExample(allowed_values[0], "ALLOWED_VALUE")
        if existing_value is not None: return ResolvedExample(existing_value, "TEST_DATA_GENERATOR")
        if classifier:
            return ResolvedExample("[значение выбирается из классификатора]", "CLASSIFIER_EXAMPLE")
        dtype=(datatype or "").casefold(); local_type=dtype.rsplit(":",1)[-1]; description_text=(description or "").casefold()
        if dtype == "any_xml" or "anyxml" in dtype:
            return ResolvedExample(unavailable_reason="ANY_XML")
        if "uuid" in dtype:return ResolvedExample("550e8400-e29b-41d4-a716-446655440000","DATATYPE_EXAMPLE")
        if "identifier" in dtype or "idtype" in dtype or re.fullmatch(r"id\d*type",local_type):
            return ResolvedExample("[идентификатор]","PROJECT_DOCUMENTATION")
        if "datetime" in dtype:return ResolvedExample("2026-08-24T15:24:00+03:00","DATATYPE_EXAMPLE")
        if dtype.endswith("datetype") or dtype.endswith(":date") or dtype=="date":return ResolvedExample("2026-08-24","DATATYPE_EXAMPLE")
        if "boolean" in dtype or "indicator" in dtype:return ResolvedExample("true","DATATYPE_EXAMPLE")
        if "decimal" in dtype:return ResolvedExample("10.5","DATATYPE_EXAMPLE")
        if any(token in dtype for token in ("integer","quantity","ordinal","number")):return ResolvedExample("1","DATATYPE_EXAMPLE")
        if "language" in dtype:return ResolvedExample("ru","DATATYPE_EXAMPLE")
        if any(token in description_text for token in ("наименование организации","наименование юридического лица","наименование хозяйствующего субъекта")):
            return ResolvedExample("ООО «Пример»","PROJECT_DOCUMENTATION")
        if "code" in dtype:
            return ResolvedExample("[код в соответствии с описанием реквизита]","PROJECT_DOCUMENTATION")
        if any(token in dtype for token in ("string","text","name")):
            return ResolvedExample("Пример текстового значения","DATATYPE_EXAMPLE")
        if any(token in dtype for token in ("binary","base64","hex")):
            return ResolvedExample(unavailable_reason="BUSINESS_VALUE_NOT_SAFE_TO_INVENT")
        return ResolvedExample(unavailable_reason="INSUFFICIENT_METADATA")
