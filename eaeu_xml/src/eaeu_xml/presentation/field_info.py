"""Human-readable field information shared by GUI surfaces and audits."""

from __future__ import annotations

import re

from .text_sanitizer import normalize_extracted_regex, sanitize_presentation_text


def field_info_multiplicity(field) -> str:
    minimum = "?" if field.min_occurs is None else str(field.min_occurs)
    if field.min_occurs == 1 and field.max_occurs == 1:
        return "1"
    if field.max_occurs in (None, "*"):
        return f"{minimum}..*"
    return f"{minimum}..{field.max_occurs}"


def field_info_datatype(field) -> str:
    datatype = sanitize_presentation_text(field.datatype)
    datatype_text = sanitize_presentation_text(field.datatype_text)
    model_id = re.search(r"\((M\.[^)]+)\)", datatype_text)
    model = sanitize_presentation_text(model_id.group(1)) if model_id else ""
    return f"{datatype}\n({model})" if datatype and model else datatype


def field_info_name(definition, field) -> str:
    qname = (
        f"{definition.namespace_prefix}:{definition.xml_name}"
        if definition.namespace_prefix and definition.xml_name
        else definition.xml_name
    )
    name = sanitize_presentation_text(
        definition.official_name or (field.display_name if field else definition.path)
    )
    suffix = f" ({qname})" if qname else ""
    return name[:-len(suffix)].strip() if suffix and name.endswith(suffix) else name


def _character_count(value: int) -> str:
    if value % 10 == 1 and value % 100 != 11:
        suffix = "символ"
    elif value % 10 in {2, 3, 4} and value % 100 not in {12, 13, 14}:
        suffix = "символа"
    else:
        suffix = "символов"
    return f"{value} {suffix}"


def _constraint_tail(source_text: str) -> str:
    model = re.search(r"\(M\.[^)]+\)\s*", source_text)
    tail = source_text[model.end():] if model else source_text
    # Table extraction in older structure files can append the multiplicity of
    # the current row before the next row text.  Multiplicity has its own GUI
    # field and is not part of the datatype constraint prose.
    tail = re.sub(r"\s+(?:0|1)(?:\.\.(?:1|\*))?\s*$", "", tail)
    tail = re.split(
        r"\s+(?:0|1)(?:\.\.(?:1|\*))?\s+(?=(?:\d+(?:\.\d+)*\.|\*\.|[а-яА-Я]\)))",
        tail,
        maxsplit=1,
    )[0]
    return tail.strip()


def field_info_constraints(definition, *, normalize_op22_regex: bool = False) -> list[dict[str, str]]:
    """Expose explicit constraints already present in structure metadata."""
    source_text = sanitize_presentation_text(definition.constraints)
    if not source_text:
        return []

    result: list[dict[str, str]] = []
    pattern_match = re.search(
        r"Шаблон:\s*(.*?)(?=\s+(?:Мин\. длина|Макс\. длина|Длина):|$)",
        source_text,
    )
    if pattern_match:
        pattern = pattern_match.group(1).strip()
        if normalize_op22_regex:
            pattern = normalize_extracted_regex(pattern)
        if pattern:
            result.append({"label": "Шаблон", "value": pattern})
            explanations = {
                r"\d{5}": "Ровно 5 цифр",
                r"\d{4}": "Ровно 4 цифры",
                r"\d+": "Одна или более цифр",
                r"[A-Z]{2}": "Ровно 2 заглавные латинские буквы",
            }
            explanation = explanations.get(pattern)
            if explanation:
                result.append({"label": "Пояснение", "value": explanation})

    exact_length = re.search(r"(?<!Мин\. )(?<!Макс\. )Длина:\s*(\d+)", source_text)
    if exact_length:
        result.append({
            "label": "Длина",
            "value": _character_count(int(exact_length.group(1))),
        })

    min_match = re.search(r"Мин\. длина:\s*(\d+)", source_text)
    if min_match:
        result.append({
            "label": "Минимальная длина",
            "value": _character_count(int(min_match.group(1))),
        })

    max_match = re.search(r"Макс\. длина:\s*(\d+)", source_text)
    if max_match:
        result.append({
            "label": "Максимальная длина",
            "value": _character_count(int(max_match.group(1))),
        })

    if "Обозначение даты в соответствии с ISO 8601" in source_text:
        result.append({"label": "Формат", "value": "ISO 8601"})
        result.append({"label": "Пояснение", "value": "Дата в соответствии с ISO 8601"})
    elif "Обозначение даты и времени в соответствии с ISO 8601" in source_text:
        result.append({"label": "Формат", "value": "ISO 8601"})
        result.append({"label": "Пояснение", "value": "Дата и время в соответствии с ISO 8601"})

    if "Одно из двух значений" in source_text:
        quoted = re.findall(r"«([^»]+)»", source_text)
        if quoted:
            result.append({
                "label": "Допустимые значения",
                "value": ", ".join(dict.fromkeys(sanitize_presentation_text(item) for item in quoted)),
            })

    if not result:
        tail = _constraint_tail(source_text)
        if tail:
            result.append({"label": "Условие", "value": tail})

    return result


def message_policy_text(field) -> str:
    if field is None or not field.effective_message_policy:
        return ""
    labels = {
        "REQUIRED": "Обязательно",
        "OPTIONAL": "Необязательно",
        "FORBIDDEN": "Не заполняется",
        "FIXED": "Фиксированное значение",
        "CONDITIONAL": "Условно",
    }
    label = labels.get(field.effective_message_policy)
    if label is None:
        return ""
    lines = [label]
    if field.effective_message_policy == "FIXED" and field.fixed_value is not None:
        lines.append(f"Значение: {sanitize_presentation_text(field.fixed_value)}")
    if field.message_policy_condition:
        lines.append(sanitize_presentation_text(field.message_policy_condition))
    if field.message_policy_external_dependency:
        dependency = sanitize_presentation_text(field.message_policy_external_dependency)
        if dependency:
            lines.append(f"Зависимость: {dependency}")
    return "\n".join(item for item in lines if item)


def build_field_details(definition, field, *, normalize_op22_regex: bool = False) -> dict[str, object]:
    return {
        "name": field_info_name(definition, field),
        "description": sanitize_presentation_text(definition.description),
        "datatype": field_info_datatype(definition),
        "multiplicity": field_info_multiplicity(definition),
        "constraints": field_info_constraints(definition, normalize_op22_regex=normalize_op22_regex),
        "policy": message_policy_text(field),
    }
