"""Safety and verification tests for TestDataGenerator and align_sample_attributes.

This module guarantees that:
1. align_sample_attributes does not invent missing attributes.
2. align_sample_attributes does not overwrite distinct user values in list attributes.
3. align_sample_attributes aligns scalar attributes to repeated parent slots (turning orphan slots into None).
4. align_sample_attributes does not mask validation errors when a mandatory attribute is missing.
5. Missing mandatory attributes on present elements are strictly detected by validation.
6. Scalar parents remain untouched.
"""

from dataclasses import dataclass
from pathlib import Path
import pytest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.application.services import TestDataGenerator


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class MockField:
    path: str
    kind: str
    is_attribute: bool = False


@pytest.fixture()
def app(tmp_path: Path) -> EaeuXmlApplication:
    return EaeuXmlApplication(ROOT, drafts_root=tmp_path / "drafts")


class TestTestDataGeneratorSafety:
    """Rigorous safety verification of TestDataGenerator.align_sample_attributes."""

    def test_align_sample_attributes_does_not_invent_missing_attributes(self) -> None:
        """When an attribute is not present in values, it must NOT be added."""
        fields = [
            MockField(path="Root/Parent", kind="ELEMENT"),
            MockField(path="Root/Parent/@codeListId", kind="ATTRIBUTE", is_attribute=True),
        ]
        values = {
            "Root/Parent": [None, "RU"],
            # Root/Parent/@codeListId is completely omitted
        }
        TestDataGenerator.align_sample_attributes(values, fields)

        assert "Root/Parent/@codeListId" not in values
        assert values == {"Root/Parent": [None, "RU"]}

    def test_align_sample_attributes_preserves_distinct_user_values(self) -> None:
        """Distinct values provided in list attributes must NOT be collapsed to a single scalar."""
        fields = [
            MockField(path="Root/Items", kind="ELEMENT"),
            MockField(path="Root/Items/@code", kind="ATTRIBUTE", is_attribute=True),
        ]
        values = {
            "Root/Items": ["Item1", "Item2"],
            "Root/Items/@code": ["CODE_1", "CODE_2"],
        }
        TestDataGenerator.align_sample_attributes(values, fields)

        assert values["Root/Items/@code"] == ["CODE_1", "CODE_2"]

    def test_align_sample_attributes_clears_orphan_slots_matching_none_parent(self) -> None:
        """When parent slot is None, corresponding attribute slot must become None, preserving other slots."""
        fields = [
            MockField(path="Root/Items", kind="ELEMENT"),
            MockField(path="Root/Items/@code", kind="ATTRIBUTE", is_attribute=True),
        ]
        values = {
            "Root/Items": [None, "Item2"],
            "Root/Items/@code": ["CODE_1", "CODE_2"],
        }
        TestDataGenerator.align_sample_attributes(values, fields)

        assert values["Root/Items/@code"] == [None, "CODE_2"]

    def test_align_sample_attributes_shapes_scalar_to_multislot_parent(self) -> None:
        """A scalar attribute must be shaped to parent list with None for absent parent slots."""
        fields = [
            MockField(path="Root/Items", kind="ELEMENT"),
            MockField(path="Root/Items/@code", kind="ATTRIBUTE", is_attribute=True),
        ]
        values = {
            "Root/Items": [None, "Item2"],
            "Root/Items/@code": "COMMON_CODE",
        }
        TestDataGenerator.align_sample_attributes(values, fields)

        assert values["Root/Items/@code"] == [None, "COMMON_CODE"]

    def test_align_sample_attributes_handles_nested_repeated_structures(self) -> None:
        """Nested parent lists [[None, 'A'], ['B']] must align attribute hierarchy correctly."""
        fields = [
            MockField(path="Root/Group/Items", kind="ELEMENT"),
            MockField(path="Root/Group/Items/@id", kind="ATTRIBUTE", is_attribute=True),
        ]
        values = {
            "Root/Group/Items": [[None, "A"], ["B"]],
            "Root/Group/Items/@id": [["ID_0", "ID_1"], ["ID_2"]],
        }
        TestDataGenerator.align_sample_attributes(values, fields)

        assert values["Root/Group/Items/@id"] == [[None, "ID_1"], ["ID_2"]]

    def test_align_sample_attributes_does_not_affect_scalar_parents(self) -> None:
        """When parent is a scalar element, the attribute remains untouched."""
        fields = [
            MockField(path="Root/Country", kind="ELEMENT"),
            MockField(path="Root/Country/@codeListId", kind="ATTRIBUTE", is_attribute=True),
        ]
        values = {
            "Root/Country": "RU",
            "Root/Country/@codeListId": "P.CLS.019",
        }
        TestDataGenerator.align_sample_attributes(values, fields)

        assert values["Root/Country"] == "RU"
        assert values["Root/Country/@codeListId"] == "P.CLS.019"

    def test_validator_detects_missing_mandatory_attribute_on_present_element(self, app: EaeuXmlApplication) -> None:
        """Verify that omitting a mandatory attribute on a present element is caught by validation."""
        values = app.generate_test_data("P.DS.01", "P.DS.01.TRN.001", "P.DS.01.MSG.001", seed=42)
        attr_key = "ChargedDistributedReport/ds01sdo:ReportCountryCode/@codeListId"
        assert attr_key in values

        # Deliberately remove mandatory attribute from a present element
        del values[attr_key]

        # Ensure align_sample_attributes does not invent or fake the missing attribute
        form = app.get_form("P.DS.01", "P.DS.01.TRN.001", "P.DS.01.MSG.001")
        TestDataGenerator.align_sample_attributes(values, form.fields)
        assert attr_key not in values

        # Validate that the system correctly catches the missing mandatory attribute
        result = app.validate("P.DS.01", "P.DS.01.TRN.001", "P.DS.01.MSG.001", values)
        assert not result.is_valid
        error_paths = {issue.field_path for issue in result.errors}
        assert attr_key in error_paths
