"""Small presentation-only building blocks shared by the workspace screens."""

import wx
from wx.lib.buttons import GenButton

from eaeu_xml.gui.theme import GuiTheme


class ActionButton(GenButton):
    def __init__(self, parent, label, handler=None, *, primary=False, flat=False):
        super().__init__(parent, label=label, style=wx.BORDER_NONE)
        self.flat = flat
        self.primary = primary
        self.SetBezelWidth(0)
        self.SetMinSize((-1, 32))
        self.SetUseFocusIndicator(True)
        if primary:
            GuiTheme.apply_primary_button(self)
        else:
            GuiTheme.apply_secondary_button(self)
        if handler:
            self.Bind(wx.EVT_BUTTON, handler)

    def DrawBezel(self, dc, x1, y1, x2, y2):
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()
        colour = self.GetBackgroundColour()
        dc.SetBrush(wx.Brush(colour))
        dc.SetPen(wx.Pen(colour if self.flat or self.primary else GuiTheme.colour("separator")))
        dc.DrawRoundedRectangle(x1, y1, x2, y2, 4)

    def DrawLabel(self, dc, width, height, dx=0, dy=0):
        dc.SetFont(self.GetFont())
        dc.SetTextForeground(self.GetForegroundColour() if self.IsEnabled() else GuiTheme.colour("secondary_text"))
        text = self.GetLabel()
        tw, th = dc.GetTextExtent(text)
        x = 12 if self.GetWindowStyleFlag() & wx.BU_LEFT else max(6, (width - tw) // 2)
        dc.DrawText(text, x, (height - th) // 2)


class NavigationButton(wx.Panel):
    def __init__(self, parent, label, handler):
        super().__init__(parent)
        GuiTheme.apply_surface(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.button = ActionButton(self, label, handler, flat=True)
        self.line = wx.Panel(self, size=(-1, 2))
        sizer.Add(self.button, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 8)
        sizer.Add(self.line, 0, wx.EXPAND)
        self.select(False)

    def select(self, selected):
        self.button.SetForegroundColour(GuiTheme.colour("accent" if selected else "text"))
        self.line.SetBackgroundColour(GuiTheme.colour("accent" if selected else "surface"))
        self.button.Refresh()
        self.line.Refresh()


class Card(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        GuiTheme.apply_surface(self)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self._paint)
        self.Bind(wx.EVT_SIZE, self._resize)

    def _resize(self, event):
        self.Refresh()
        event.Skip()

    def _paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(GuiTheme.colour("background")))
        dc.Clear()
        dc.SetPen(wx.Pen(GuiTheme.colour("separator")))
        dc.SetBrush(wx.Brush(GuiTheme.colour("surface")))
        width, height = self.GetClientSize()
        dc.DrawRoundedRectangle(0, 0, max(0, width - 1), max(0, height - 1), 5)


def heading(parent, label):
    control = wx.StaticText(parent, label=label)
    GuiTheme.apply_heading(control, level=2)
    return control


class FormSection(wx.Panel):
    def __init__(self, parent, title, *, expanded=False):
        super().__init__(parent)
        GuiTheme.apply_surface(self)
        self.title = title
        self.expanded = expanded
        self.header = ActionButton(self, "", flat=True)
        self.header.SetWindowStyleFlag(wx.BORDER_NONE | wx.BU_LEFT)
        self.header.SetBackgroundColour(GuiTheme.colour("sidebar"))
        self.header.Bind(wx.EVT_BUTTON, self._toggle)
        self.content = wx.Panel(self)
        GuiTheme.apply_surface(self.content)
        self.content.SetSizer(wx.BoxSizer(wx.VERTICAL))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        sizer.Add(self.header, 0, wx.EXPAND)
        sizer.Add(self.content, 0, wx.EXPAND | wx.ALL, 8)
        self._sync()

    def _sync(self):
        self.header.SetLabel(("⌄  " if self.expanded else "›  ") + self.title)
        self.content.Show(self.expanded)

    def expand(self):
        self.expanded = True
        self._sync()
        self._layout()

    def _toggle(self, event):
        self.expanded = not self.expanded
        self._sync()
        self._layout()

    def _layout(self):
        window = self
        while window:
            window.Layout()
            if isinstance(window, wx.ScrolledWindow):
                window.FitInside()
            window = window.GetParent()
