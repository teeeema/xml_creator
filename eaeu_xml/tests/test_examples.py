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
        self.assertEqual(uuid.value,"d1f6f86c-029a-4245-bb91-433a6aa79987")
        self.assertEqual((business.value,business.origin),("123456","DATATYPE_EXAMPLE"))
        self.assertNotEqual(business.value,uuid.value)

    def test_classifier_without_local_values_has_no_invented_example(self):
        result=self.resolver.resolve(datatype="CodeType",description=None,classifier=True)
        self.assertEqual((result.value,result.unavailable_reason),(None,"CLASSIFIER_NOT_AVAILABLE"))

    def test_pattern_accepts_only_matching_example(self):
        result=self.resolver.resolve(datatype="CountryCodeType",description=None,pattern="[A-Z]{2}")
        self.assertEqual(result.value,"RU")
        self.assertIsNone(self.resolver.resolve(datatype="CountryCodeType",description=None,
                                                pattern="[0-9]{8}").value)
        self.assertEqual(self.resolver.resolve(datatype="CodeType", description=None,
                                               pattern=r"\d{4}/(AM|BY|KG|KZ|RU)-\d{6}").value,
                         "2026/RU-123456")
        self.assertEqual(self.resolver.resolve(datatype="CodeType", description=None,
                                               allowed_values=("BAD", "RU"), pattern="[A-Z]{2}").value,
                         "RU")

    def test_project_documentation_organization_example(self):
        result=self.resolver.resolve(datatype="NameType",description="наименование организации")
        self.assertEqual((result.value,result.origin),("ООО «Пример»","PROJECT_DOCUMENTATION"))

    def test_any_xml_remains_without_invented_structure(self):
        result=self.resolver.resolve(datatype="ANY_XML",description=None)
        self.assertEqual((result.value,result.origin,result.unavailable_reason),(None,"UNAVAILABLE","ANY_XML"))
