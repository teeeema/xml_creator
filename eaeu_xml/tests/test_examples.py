import unittest

from eaeu_xml.application.examples import ExampleValueResolver


class ExampleValueResolverTests(unittest.TestCase):
    def setUp(self): self.resolver=ExampleValueResolver()

    def test_datatype_safe_examples(self):
        cases={"bdt:DateType":"2026-08-24","bdt:DateTimeType":"2026-08-24T15:24:00+03:00","bdt:DecimalType":"10.5","bdt:BooleanType":"true","csdo:LanguageCodeType":"ru"}
        for datatype,value in cases.items():
            with self.subTest(datatype=datatype):
                result=self.resolver.resolve(datatype=datatype,description=None);self.assertEqual((result.value,result.origin),(value,"DATATYPE_EXAMPLE"))

    def test_uuid_only_when_datatype_confirms_it(self):
        uuid=self.resolver.resolve(datatype="UUIDType",description=None)
        business=self.resolver.resolve(datatype="csdo:Id50Type",description="номер заявления")
        self.assertEqual(uuid.value,"550e8400-e29b-41d4-a716-446655440000")
        self.assertEqual((business.value,business.origin),("[идентификатор]","PROJECT_DOCUMENTATION"))
        self.assertNotEqual(business.value,uuid.value)

    def test_classifier_uses_instructional_placeholder(self):
        result=self.resolver.resolve(datatype="CodeType",description=None,classifier=True)
        self.assertEqual((result.value,result.origin),("[значение выбирается из классификатора]","CLASSIFIER_EXAMPLE"))

    def test_project_documentation_organization_example(self):
        result=self.resolver.resolve(datatype="NameType",description="наименование организации")
        self.assertEqual((result.value,result.origin),("ООО «Пример»","PROJECT_DOCUMENTATION"))

    def test_any_xml_remains_without_invented_structure(self):
        result=self.resolver.resolve(datatype="ANY_XML",description=None)
        self.assertEqual((result.value,result.origin,result.unavailable_reason),(None,"UNAVAILABLE","ANY_XML"))
