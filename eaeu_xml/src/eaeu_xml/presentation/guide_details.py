"""Display-independent formatting and metadata lookup for Guide tree nodes."""

from dataclasses import dataclass
from typing import Mapping

from eaeu_xml.application import FieldGuide


@dataclass(frozen=True)
class GuideNodeKey:
    message_code: str
    field_path: str


def resolve_guide_node(item_data, fields_by_key: Mapping[GuideNodeKey, FieldGuide]):
    return fields_by_key.get(item_data) if isinstance(item_data,GuideNodeKey) else None


def build_guide_node_details(field: FieldGuide) -> str:
    """Build one complete card for a leaf, attribute or structural group."""
    lines=[]
    def add(label,value):
        if value not in (None,"",(),[]):lines.append(f"{label}: {value}")
    add("Название",field.display_name)
    add("XML name",field.xml_qname or field.xml_name)
    add("XML path",field.path)
    add("Тип","Структурный блок" if field.children else field.xml_kind)
    if field.children:add("Дочерних реквизитов",len(field.children))
    add("Datatype",field.datatype)
    add("Обязательность",field.requirement)
    add("Кратность",field.cardinality)
    add("Кто заполняет",field.who_fills)
    filling={
        "USER_INPUT":"пользователем", "USER_SELECT":"выбирается пользователем",
        "AUTO":"формируется программой", "READ_ONLY":"формируется программой; ручное изменение недоступно",
        "EXTERNAL_SYSTEM":"поступает из внешней информационной системы",
        "CONDITIONAL":"зависит от условия", "GROUP":"структурный блок",
        "UNRESOLVED_UI_POLICY":"способ заполнения не определён", "HIDDEN":"служебный реквизит",
    }.get(field.ui_input_policy,field.who_fills)
    add("Заполнение в программе",filling)
    add("Что необходимо указать",field.what_to_enter)
    add("Помощь при вводе",field.input_assistance)
    add("Источник значения",field.value_source)
    if field.example_value is not None:add(field.example_label,field.example_value)
    add("Условие",field.condition)
    if field.condition:add("Автоматическая проверка","Да" if field.automatic_condition_check else "Нет")
    if field.classifier:
        add("Классификатор",field.classifier)
        add("Набор классификатора","доступен" if field.classifier_dataset_available else "не включён в текущую конфигурацию")
    if field.automatic_condition_check:
        add("Поле-источник условия",field.condition_source_field)
        add("Сравнение",field.condition_operator_description)
        add("Ожидаемое значение",field.condition_expected_value)
        add("Текущий результат",field.condition_result)
    if field.repeatable:lines.append("Может быть указано несколько значений. Для добавления экземпляра используется кнопка «Добавить».")
    for source in field.sources:
        lines.append("Нормативный источник:")
        add("Документ",source.document);add("Раздел",source.location);add("Таблица",source.table)
        add("Пункт/строка",source.item);add("Страница",source.page)
    return "\n".join(lines)
