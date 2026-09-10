"""Small, system-aware presentation helpers for the wx frontend."""

import wx


class GuiTheme:
    """Keep the application palette and control hierarchy consistent."""

    @staticmethod
    def is_dark() -> bool:
        return wx.SystemSettings.GetAppearance().IsDark()

    @classmethod
    def colour(cls, name: str) -> wx.Colour:
        light = {
            "background": "#F5F7FA",
            "surface": "#FFFFFF",
            "sidebar": "#F1F4F8",
            "separator": "#D9E0EA",
            "text": "#20242B",
            "secondary_text": "#687386",
            "accent": "#0A6CFF",
            "accent_soft": "#E7F0FF",
            "success": "#188A42",
            "warning": "#B56800",
            "error": "#C53532",
        }
        dark = {
            "background": "#1E2025",
            "surface": "#2A2D33",
            "sidebar": "#25282E",
            "separator": "#424750",
            "text": "#F2F4F8",
            "secondary_text": "#B2BAC8",
            "accent": "#5B9DFF",
            "accent_soft": "#243A5B",
            "success": "#5FCB82",
            "warning": "#F2B45B",
            "error": "#FF8C89",
        }
        return wx.Colour((dark if cls.is_dark() else light)[name])

    @classmethod
    def apply_surface(cls, window) -> None:
        window.SetBackgroundColour(cls.colour("surface"))
        window.SetForegroundColour(cls.colour("text"))

    @classmethod
    def apply_sidebar_button(cls, button, *, selected: bool = False) -> None:
        button.SetBackgroundColour(cls.colour("accent_soft") if selected else cls.colour("sidebar"))
        button.SetForegroundColour(cls.colour("accent") if selected else cls.colour("text"))
        button.SetWindowStyleFlag(wx.BORDER_NONE | wx.BU_LEFT)

    @classmethod
    def apply_secondary_button(cls, button) -> None:
        button.SetBackgroundColour(cls.colour("surface"))
        button.SetForegroundColour(cls.colour("text"))
        button.SetWindowStyleFlag(wx.BORDER_NONE)

    @classmethod
    def apply_primary_button(cls, button) -> None:
        button.SetBackgroundColour(cls.colour("accent"))
        button.SetForegroundColour(wx.Colour("#FFFFFF"))
        button.SetWindowStyleFlag(wx.BORDER_NONE)

    @classmethod
    def apply_heading(cls, label, *, level: int = 1) -> None:
        font = label.GetFont()
        font.MakeBold()
        font.SetPointSize(font.GetPointSize() + (2 if level == 1 else 1))
        label.SetFont(font)
        label.SetForegroundColour(cls.colour("text"))

    @classmethod
    def apply_secondary_text(cls, label) -> None:
        label.SetForegroundColour(cls.colour("secondary_text"))
