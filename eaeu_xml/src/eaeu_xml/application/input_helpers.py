"""Presentation helpers for editable date/time and identifier fields."""

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo, available_timezones


TIMEZONE_ALIASES = {
    "москва": "Europe/Moscow", "moscow": "Europe/Moscow",
    "стокгольм": "Europe/Stockholm", "stockholm": "Europe/Stockholm",
    "дубай": "Asia/Dubai", "dubai": "Asia/Dubai",
}


def datatype_category(datatype: str | None) -> str | None:
    value = (datatype or "").lower().rsplit(":", 1)[-1]
    if "datetime" in value: return "DATETIME"
    if value in {"time", "timetype"} or value.endswith("timetype"): return "TIME"
    if value in {"date", "datetype"} or value.endswith("datetype"): return "DATE"
    return None


def today_value(current: date | None = None) -> str:
    return (current or date.today()).isoformat()


def resolve_timezone(selection: str):
    if selection == "UTC": return timezone.utc
    if selection == "System": return datetime.now().astimezone().tzinfo
    return ZoneInfo(selection)


def datetime_value(selection: str = "System", current: datetime | None = None) -> str:
    zone = resolve_timezone(selection)
    value = (current.astimezone(zone) if current and current.tzinfo else
             current.replace(tzinfo=zone) if current else datetime.now(zone))
    value = value.replace(microsecond=0)
    return value.strftime("%Y-%m-%dT%H:%M:%SZ") if selection == "UTC" else value.isoformat()


def time_value(selection: str = "System", current: datetime | None = None) -> str:
    return datetime_value(selection,current).split("T",1)[-1]


def search_timezones(query: str) -> tuple[str, ...]:
    needle = query.strip().casefold()
    alias = TIMEZONE_ALIASES.get(needle)
    matches = [zone for zone in available_timezones() if needle in zone.casefold()]
    if alias and alias not in matches: matches.insert(0, alias)
    return tuple(sorted(dict.fromkeys(matches), key=lambda zone: (zone != alias, zone)))
