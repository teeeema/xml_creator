"""User-facing form guidance derived from the selected message's field metadata."""

from dataclasses import dataclass

from eaeu_xml.application.models import FieldView


@dataclass(frozen=True)
class FieldHelp:
    purpose: str
    what_to_enter: str
    example: str
    required_type: str
    format: str | None = None


def resolve_field_help(field: FieldView, *, unconditionally_required: bool) -> FieldHelp:
    name = field.xml_name or ""
    path = field.path.casefold()
    datatype = (field.datatype or "").casefold()
    purpose = (field.description or "").strip()
    if name == "InfEnvelopeCode":
        purpose = "Определяет сообщение общего процесса, которое передается."
        guidance = "Код выбранного сообщения."
    elif name == "EDocCode":
        purpose = "Указывает структуру электронного документа внутри сообщения."
        guidance = "Код структуры, назначенной выбранному сообщению."
    elif name in {"EDocId", "EDocRefId"}:
        purpose = ("Уникально идентифицирует текущий электронный документ." if name == "EDocId" else
                   "Связывает документ с исходным электронным документом.")
        guidance = "UUID соответствующего электронного документа."
    elif "countrycode" in datatype:
        if "address" in path:
            purpose = "Указывает страну, к которой относится данный адрес."
        elif "patentauthority" in path:
            purpose = "Указывает государство национального патентного ведомства."
        elif "party" in path:
            purpose = "Указывает государство участника, описанного в этом блоке."
        guidance = "Двухбуквенный код страны, если он подтверждён локальным справочником."
    elif "datetime" in datatype:
        guidance = "Дату и время в формате ISO 8601."
    elif datatype.endswith("datetype") or datatype == "date":
        guidance = "Календарную дату в формате ГГГГ-ММ-ДД."
    elif "uuid" in datatype or "universallyuniqueid" in datatype:
        guidance = "UUID соответствующего объекта."
    elif "language" in datatype:
        guidance = "Двухбуквенный код языка."
    elif field.allowed_values:
        guidance = "Одно из допустимых значений, указанных ниже."
    elif field.classifier:
        guidance = "Значение из указанного классификатора. Если справочник недоступен локально, проверьте его в официальном источнике."
    elif field.children:
        guidance = "Заполните обязательные реквизиты этого блока."
    elif field.input_policy == "CONDITIONAL":
        guidance = field.condition_description or "Значение требуется при выполнении нормативного условия."
    elif "identifier" in datatype or "idtype" in datatype or name.endswith("Id"):
        guidance = "Идентификатор, присвоенный указанному документу или объекту; сохраните его точное написание."
    elif "code" in datatype:
        guidance = "Код соответствующего объекта из применимого нормативного справочника или правила."
    elif "name" in datatype:
        guidance = "Наименование соответствующего объекта в том виде, в котором оно используется в документе."
    elif "text" in datatype or "string" in datatype:
        guidance = "Текстовое значение, описывающее соответствующий реквизит."
    elif "indicator" in datatype or "boolean" in datatype:
        guidance = "Значение true или false согласно смыслу признака."
    elif "decimal" in datatype or "amount" in datatype:
        guidance = "Числовое значение с десятичной частью, без пробелов-разделителей."
    elif "quantity" in datatype or "integer" in datatype or "ordinal" in datatype:
        guidance = "Целое число без пробелов-разделителей."
    elif "duration" in datatype:
        guidance = "Длительность в формате, установленном типом реквизита."
    else:
        guidance = "Значение согласно назначению реквизита и требованиям выбранного сообщения."

    if not purpose:
        purpose = "Значение используется согласно требованиям выбранного сообщения; отдельное назначение в локальной модели не описано."
    if field.input_policy == "CONDITIONAL" or field.condition_description:
        required_type = "Условно обязательное"
    else:
        required_type = "Обязательное" if unconditionally_required else "Необязательное"
    if field.pattern:
        format_hint = field.pattern
    elif "uuid" in datatype or "universallyuniqueid" in datatype:
        format_hint = "UUID"
    elif "datetime" in datatype:
        format_hint = "ISO 8601"
    elif "countrycode" in datatype:
        format_hint = "Двухбуквенный код страны"
    else:
        format_hint = None
    example = (str(field.example_value) if field.example_value is not None else
               "Пример недоступен: локальные нормативные данные не задают безопасное значение.")
    return FieldHelp(purpose, guidance, example, required_type, format_hint)


def render_field_help(field: FieldView, *, unconditionally_required: bool) -> str:
    help_info = resolve_field_help(field, unconditionally_required=unconditionally_required)
    lines = [field.display_name, "", f"Назначение: {help_info.purpose}",
             f"Что указывать: {help_info.what_to_enter}", f"Пример: {help_info.example}"]
    if help_info.format:
        lines.append(f"Формат: {help_info.format}")
    if field.allowed_values:
        lines.append("Допустимые значения: " + ", ".join(map(str, field.allowed_values)))
    lines.append(f"Обязательность: {help_info.required_type}")
    lines.extend(("", "Технические сведения", f"XML: {field.xml_qname or field.xml_name or '—'}",
                  f"XML path: {field.path}", f"Тип: {field.datatype or '—'}"))
    return "\n".join(lines)
