from datetime import date, datetime, timezone
from pathlib import Path
from uuid import UUID
import unittest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.application.input_helpers import datetime_value, search_timezones, today_value


FIXTURES = Path(__file__).parent / "fixtures"


class AssistedInputTests(unittest.TestCase):
    def test_identifier_provider_uses_identifier_service_boundary(self):
        self.assertEqual(UUID(EaeuXmlApplication(FIXTURES).generate_identifier_value()).version, 4)

    def test_date_manual_value_and_today_helper_are_plain_iso_values(self):
        manual = "2026-08-25"
        self.assertEqual(manual, "2026-08-25")
        self.assertEqual(today_value(date(2026, 8, 25)), manual)

    def test_datetime_utc_and_named_zone(self):
        instant = datetime(2026, 8, 25, 8, 35, 42, tzinfo=timezone.utc)
        self.assertEqual(datetime_value("UTC", instant), "2026-08-25T08:35:42Z")
        self.assertEqual(datetime_value("Europe/Moscow", instant), "2026-08-25T11:35:42+03:00")

    def test_stockholm_offset_comes_from_zoneinfo_and_changes_with_dst(self):
        winter = datetime_value("Europe/Stockholm", datetime(2026, 1, 15, 12, tzinfo=timezone.utc))
        summer = datetime_value("Europe/Stockholm", datetime(2026, 7, 15, 12, tzinfo=timezone.utc))
        self.assertTrue(winter.endswith("+01:00"), winter)
        self.assertTrue(summer.endswith("+02:00"), summer)

    def test_timezone_search_supports_iana_and_presentation_aliases(self):
        self.assertIn("Europe/Moscow", search_timezones("moscow"))
        self.assertIn("Europe/Moscow", search_timezones("Москва"))
        self.assertIn("Europe/Stockholm", search_timezones("stockholm"))
        self.assertIn("Asia/Dubai", search_timezones("dubai"))


if __name__ == "__main__": unittest.main()
