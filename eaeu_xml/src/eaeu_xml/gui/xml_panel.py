from xml.dom import minidom

import wx

from eaeu_xml.gui.theme import GuiTheme

try:
    import wx.stc as stc
except ImportError:
    stc = None


class XmlPanel(wx.Panel):
    """Read-only, editor-style presentation of the generated XML document."""

    def __init__(self, parent):
        super().__init__(parent)
        GuiTheme.apply_surface(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        header = wx.BoxSizer(wx.HORIZONTAL)
        self.filename = wx.StaticText(self, label="Сообщение.xml")
        GuiTheme.apply_heading(self.filename, level=2)
        self.search = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.search.SetDescriptiveText("Поиск в XML")
        self.search.SetMinSize((220, -1))
        self.format_button = wx.Button(self, label="Форматировать")
        self.expand_button = wx.Button(self, label="Развернуть всё")
        self.format_button.Bind(wx.EVT_BUTTON, self._on_format)
        self.expand_button.Bind(wx.EVT_BUTTON, self._on_expand)
        self.search.Bind(wx.EVT_TEXT_ENTER, self._on_search)
        self.search.Bind(wx.EVT_TEXT, self._on_search)
        GuiTheme.apply_secondary_button(self.format_button)
        GuiTheme.apply_secondary_button(self.expand_button)
        header.Add(self.filename, 1, wx.ALIGN_CENTER_VERTICAL)
        header.Add(self.search, 0, wx.RIGHT, 6)
        header.Add(self.format_button, 0, wx.RIGHT, 6)
        header.Add(self.expand_button, 0)
        sizer.Add(header, 0, wx.EXPAND | wx.ALL, 10)

        self.warning = wx.StaticText(self, label="")
        self.warning.Hide()
        self.metadata = wx.StaticText(self, label="XML ещё не сформирован.")
        sizer.Add(self.warning, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        sizer.Add(self.metadata, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)

        if stc:
            self.output = stc.StyledTextCtrl(self)
            self.output.SetLexer(stc.STC_LEX_XML)
            self.output.SetReadOnly(True)
            self.output.SetMarginType(0, stc.STC_MARGIN_NUMBER)
            self.output.SetMarginWidth(0, 44)
            self.output.SetWrapMode(stc.STC_WRAP_NONE)
            self._apply_editor_theme()
        else:
            self.output = wx.TextCtrl(
                self,
                style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL,
            )
        sizer.Add(self.output, 1, wx.EXPAND | wx.ALL, 10)

    def _apply_editor_theme(self):
        appearance = wx.SystemSettings.GetAppearance()
        if appearance.IsDark():
            background = GuiTheme.colour("background")
            foreground = GuiTheme.colour("text")
        else:
            background = GuiTheme.colour("background")
            foreground = GuiTheme.colour("text")

        self.output.StyleSetForeground(stc.STC_STYLE_DEFAULT, foreground)
        self.output.StyleSetBackground(stc.STC_STYLE_DEFAULT, background)
        self.output.StyleSetForeground(stc.STC_STYLE_LINENUMBER, GuiTheme.colour("secondary_text"))
        self.output.StyleSetBackground(stc.STC_STYLE_LINENUMBER, background)
        self.output.StyleSetForeground(stc.STC_H_TAG, wx.Colour("#0066CC"))
        self.output.StyleSetForeground(stc.STC_H_ATTRIBUTE, wx.Colour("#7B3FB2"))
        self.output.StyleSetForeground(stc.STC_H_DOUBLESTRING, wx.Colour("#A15C00"))
        self.output.StyleClearAll()

    def show_generation(self, result):
        self._set_text(result.xml or "")
        if result.metadata.get("uses_version_placeholders"):
            self.warning.SetLabel(self.warning_text(result))
            self.warning.Show()
        else:
            self.warning.Hide()
        metadata = " | ".join(
            f"{key}: {value}"
            for key, value in result.metadata.items()
            if value is not None
        )
        self.metadata.SetLabel(metadata or f"Status: {result.status}")
        self.Layout()

    def set_filename(self, message_code: str | None):
        self.filename.SetLabel(f"{message_code or 'Сообщение'}.xml")

    @staticmethod
    def warning_text(result):
        versions = " / ".join(result.metadata.get("placeholder_versions") or ())
        return (
            "ТЕСТОВЫЙ XML\n\nОдна или несколько версий моделей не определены.\n"
            f"В XML сохранены нормативные placeholders: {versions}.\n"
            "Перед production-использованием необходимо указать реальные версии."
        )

    def show_text(self, text):
        self._set_text(text)
        self.metadata.SetLabel("")

    def get_xml_text(self):
        if stc and isinstance(self.output, stc.StyledTextCtrl):
            return self.output.GetText()
        return self.output.GetValue()

    def clear(self):
        self.warning.Hide()
        self._set_text(
            "XML ещё не сформирован.\n\n"
            "Заполните данные во вкладке «Заполнение полей» и нажмите «Сформировать XML»."
        )
        self.metadata.SetLabel("XML ещё не сформирован.")

    def _set_text(self, text):
        if stc and isinstance(self.output, stc.StyledTextCtrl):
            self.output.SetReadOnly(False)
            self.output.SetText(text)
            self.output.EmptyUndoBuffer()
            self.output.SetReadOnly(True)
        else:
            self.output.SetValue(text)

    def _on_search(self, event):
        query = self.search.GetValue()
        if not query or not (stc and isinstance(self.output, stc.StyledTextCtrl)):
            return
        start = self.output.GetCurrentPos()
        position = self.output.FindText(start, self.output.GetTextLength(), query)
        if position == -1:
            position = self.output.FindText(0, start, query)
        if position != -1:
            self.output.SetSelection(position, position + len(query))
            self.output.EnsureCaretVisible()

    def _on_format(self, event):
        xml_text = self.get_xml_text().strip()
        if not xml_text or xml_text.startswith("XML ещё не сформирован"):
            return
        try:
            formatted = minidom.parseString(xml_text).toprettyxml(indent="  ")
        except Exception:
            self.metadata.SetLabel("XML не удалось отформатировать: исходный текст не является корректным XML.")
            return
        self._set_text(formatted)
        self.metadata.SetLabel("XML отформатирован для чтения.")

    def _on_expand(self, event):
        if stc and isinstance(self.output, stc.StyledTextCtrl):
            for line in range(self.output.GetLineCount()):
                if self.output.GetFoldLevel(line) & stc.STC_FOLDLEVELHEADERFLAG:
                    self.output.SetFoldExpanded(line, True)
                    self.output.Expand(line, True, True, 1000)
