"""Font helpers for the Qt GUI."""

from __future__ import annotations

from PySide6.QtGui import QFontDatabase


def fixed_font_family() -> str:
    """Return an installed fixed-width family without generic alias lookup."""
    families = QFontDatabase.families()
    system_family = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont).family()
    if system_family in families and QFontDatabase.isFixedPitch(system_family):
        return system_family

    fixed_families = [family for family in families if QFontDatabase.isFixedPitch(family)]
    return fixed_families[0] if fixed_families else QFontDatabase.systemFont(
        QFontDatabase.SystemFont.GeneralFont
    ).family()
