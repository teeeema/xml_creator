import wx

try:
    import wx.stc as stc
except ImportError:
    stc = None

class XmlPanel(wx.Panel):
    def __init__(self,parent):
        super().__init__(parent); sizer=wx.BoxSizer(wx.VERTICAL); self.SetSizer(sizer)
        self.warning=wx.StaticText(self,label=""); self.warning.Hide()
        self.metadata=wx.StaticText(self,label="XML ещё не сформирован.")
        if stc:
            self.output=stc.StyledTextCtrl(self); self.output.SetLexer(stc.STC_LEX_XML); self._apply_system_theme(); self.output.SetReadOnly(True)
        else:self.output=wx.TextCtrl(self,style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        sizer.Add(self.warning,0,wx.EXPAND|wx.ALL,6); sizer.Add(self.metadata,0,wx.EXPAND|wx.ALL,4); sizer.Add(self.output,1,wx.EXPAND|wx.ALL,4)

    def _apply_system_theme(self):
        appearance=wx.SystemSettings.GetAppearance()
        colours=(self.output.GetBackgroundColour(),self.GetBackgroundColour(),self.GetParent().GetBackgroundColour())
        dark_colours=tuple(colour for colour in colours if (colour.Red()*299+colour.Green()*587+colour.Blue()*114)/1000<128)
        if not appearance.IsDark() and not dark_colours:return
        background=dark_colours[0] if dark_colours else wx.Colour("#1E1E1E")
        self.output.StyleSetForeground(stc.STC_STYLE_DEFAULT,wx.Colour("#FFFFFF"))
        self.output.StyleSetBackground(stc.STC_STYLE_DEFAULT,background)
        self.output.StyleClearAll()
        self.output.SetCaretForeground(wx.Colour("#FFFFFF"))

    def show_generation(self,result):
        self._set_text(result.xml or "")
        if result.metadata.get("uses_version_placeholders"):
            self.warning.SetLabel(self.warning_text(result))
            self.warning.Show()
        else:self.warning.Hide()
        self.metadata.SetLabel(" | ".join(f"{key}: {value}" for key,value in result.metadata.items() if value is not None) or f"Status: {result.status}")
        self.Layout()

    @staticmethod
    def warning_text(result):
        versions=" / ".join(result.metadata.get("placeholder_versions") or ())
        return ("ТЕСТОВЫЙ XML\n\nОдна или несколько версий моделей не определены.\n"
            f"В XML сохранены нормативные placeholders: {versions}.\nПеред production-использованием необходимо указать реальные версии.")

    def show_text(self,text): self._set_text(text); self.metadata.SetLabel("")

    def get_xml_text(self):
        return self.output.GetText() if stc and isinstance(self.output,stc.StyledTextCtrl) else self.output.GetValue()

    def clear(self):
        self.warning.Hide()
        self._set_text("XML ещё не сформирован.\n\nЗаполните данные во вкладке «Заполнение данных» и нажмите «Сформировать XML».")
        self.metadata.SetLabel("XML ещё не сформирован.")

    def _set_text(self,text):
        if stc and isinstance(self.output,stc.StyledTextCtrl):
            self.output.SetReadOnly(False); self.output.SetText(text); self.output.SetReadOnly(True)
        else:self.output.SetValue(text)
