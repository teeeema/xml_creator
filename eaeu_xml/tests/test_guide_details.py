import unittest

from eaeu_xml.application import FieldGuide, GuideSourceView
from eaeu_xml.gui.guide_details import GuideNodeKey, build_guide_node_details, resolve_guide_node


def guide_field(path="Header/Code", *, name="Code", display="Код сообщения", kind="XML-элемент",
                policy="READ_ONLY", children=(), example="P.TEST.MSG.001"):
    return FieldGuide(
        "P.TEST.MSG.001",path,name,display,"Назначение реквизита","StringType",kind,
        "Обязательно","1..1",False,"Программа","AUTO_FIXED",policy,"MESSAGE_METADATA",
        "Код выбранного сообщения общего процесса",example_value=example,
        sources=(GuideSourceView("Тестовый нормативный документ","таблица реквизитов","8","1",10),),
        children=tuple(children),xml_qname=("@codeListId" if kind=="XML-атрибут" else f"csdo:{name}"),
    )


class GuideDetailsTests(unittest.TestCase):
    def test_leaf_details_include_complete_nonempty_card(self):
        text=build_guide_node_details(guide_field())
        for expected in ("Название: Код сообщения","XML name: csdo:Code","XML path: Header/Code",
                         "Тип: XML-элемент","Datatype: StringType","Обязательность: Обязательно",
                         "Кто заполняет: Программа","Заполнение в программе: формируется программой",
                         "Пример: P.TEST.MSG.001","Документ: Тестовый нормативный документ",
                         "Таблица: 8","Пункт/строка: 1","Страница: 10"):
            self.assertIn(expected,text)

    def test_group_details_include_structural_type_and_child_count(self):
        group=guide_field("Header",name="Header",display="Заголовок",policy="GROUP",children=(guide_field(),),example=None)
        text=build_guide_node_details(group)
        self.assertIn("Тип: Структурный блок",text)
        self.assertIn("Дочерних реквизитов: 1",text)

    def test_attribute_is_not_presented_as_element(self):
        text=build_guide_node_details(guide_field("Header/@codeListId",name="codeListId",kind="XML-атрибут"))
        self.assertIn("XML name: @codeListId",text);self.assertIn("Тип: XML-атрибут",text)
        self.assertNotIn("Тип: XML-элемент",text)

    def test_stable_key_resolves_new_value_equal_instance_and_switches_details(self):
        first=guide_field();second=guide_field("Header/Name",name="Name",display="Наименование",policy="USER_INPUT",example="Пример")
        mapping={GuideNodeKey(first.message_code,first.path):first,GuideNodeKey(second.message_code,second.path):second}
        selected=resolve_guide_node(GuideNodeKey("P.TEST.MSG.001","Header/Code"),mapping)
        self.assertIs(selected,first)
        self.assertNotEqual(build_guide_node_details(selected),build_guide_node_details(second))
        self.assertIsNone(resolve_guide_node(None,mapping))

    def test_message_code_is_part_of_mapping_and_old_message_mapping_can_be_cleared(self):
        field=guide_field();key=GuideNodeKey("P.TEST.MSG.001",field.path);mapping={key:field}
        self.assertIsNone(resolve_guide_node(GuideNodeKey("P.TEST.MSG.002",field.path),mapping))
        mapping.clear();self.assertIsNone(resolve_guide_node(key,mapping))


if __name__=="__main__":unittest.main()
