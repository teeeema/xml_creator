import wx

from eaeu_xml.gui.field_controls import GroupEditor, RepeatingGroupEditor, ScalarEditor
from eaeu_xml.gui.theme import GuiTheme
from eaeu_xml.gui.components import FormSection


class FormPanel(wx.ScrolledWindow):
    def __init__(self, parent, on_field_guide=None, on_value_changed=None, on_assisted_input=None):
        super().__init__(parent, style=wx.HSCROLL | wx.VSCROLL); self.SetScrollRate(12, 12)
        GuiTheme.apply_surface(self)
        self.root_sizer=wx.BoxSizer(wx.VERTICAL); self.SetSizer(self.root_sizer); self.editors=[]; self.on_field_guide=on_field_guide;self.on_value_changed=on_value_changed;self.on_assisted_input=on_assisted_input;self.force_expand=False
        self._resize_pending=False; self.Bind(wx.EVT_SIZE,self._on_size)

    def _on_size(self,event):
        event.Skip()
        if not self._resize_pending:
            self._resize_pending=True; wx.CallAfter(self._refresh_after_resize)

    def _refresh_after_resize(self):
        self._resize_pending=False
        if self.IsBeingDeleted():return
        self.Layout(); self.FitInside()

    def show_form(self, form):
        self.root_sizer.Clear(delete_windows=True); self.editors=[]
        mode=getattr(getattr(form,"mode",None),"value",getattr(form,"mode",None));self.force_expand=bool(getattr(form,"query","") or mode=="ERRORS")
        self.sections = {}
        for title in ("Общие сведения", "Сведения о заявителе", "Документы", "Дополнительные сведения"):
            section = FormSection(self, title, expanded=title == "Общие сведения" or self.force_expand)
            self.sections[title] = section
            self.root_sizer.Add(section, 0, wx.EXPAND | wx.BOTTOM, 8)
        for field in form.fields:
            if field.visibility == "HIDDEN": continue
            section = self.sections[self._section_title(field)]
            parent = section.content
            if field.children and field.repeatable:
                group = FormSection(parent, field.display_name, expanded=self.force_expand)
                parent.GetSizer().Add(group, 0, wx.EXPAND | wx.BOTTOM, 8)
                parent = group.content
            editor=self._editor(parent,field); self.editors.append(editor)
            if isinstance(editor, GroupEditor) and not self.force_expand and "header" not in (field.xml_name or "").casefold():
                editor.pane.Collapse(True)
            parent.GetSizer().Add(editor,0,wx.EXPAND|wx.BOTTOM,8)
        for section in self.sections.values():
            if not section.content.GetSizer().GetItemCount():
                text = wx.StaticText(section.content, label="В выбранном сообщении нет полей этой секции.")
                text.Wrap(280)
                GuiTheme.apply_secondary_text(text)
                section.content.GetSizer().Add(text, 0, wx.EXPAND | wx.ALL, 8)
        empty_message=getattr(form,"empty_message",None)
        if empty_message:self.root_sizer.Add(wx.StaticText(self,label=empty_message),0,wx.ALL,12)
        self.Layout(); self.FitInside(); self.Scroll(0,0)

    @staticmethod
    def _section_title(field):
        # Presentation grouping only: keep whole source groups and their paths intact.
        name = f"{field.xml_name or ''} {field.display_name}".casefold()
        if any(word in name for word in ("applicant", "заявител")):
            return "Сведения о заявителе"
        if any(word in name for word in ("header", "заголов", "общие сведения")):
            return "Общие сведения"
        if any(word in name for word in ("document", "документ", "attachment", "вложен")):
            return "Документы"
        if any(word in name for word in ("additional", "дополнитель", "note", "примечан")):
            return "Дополнительные сведения"
        return "Общие сведения"

    def _editor(self,parent,field):
        if field.children and field.repeatable: return RepeatingGroupEditor(parent,field,self._editor,self.on_value_changed)
        return GroupEditor(parent,field,self._editor,force_expand=self.force_expand) if field.children else ScalarEditor(parent,field,self.on_field_guide,self.on_value_changed,self.on_assisted_input)

    def get_values(self):
        result={}
        for editor in self.editors: result.update(editor.get_values())
        return result

    def set_values(self,values):
        for editor in self.editors:
            if isinstance(editor,ScalarEditor): editor.set_value(values.get(editor.field.path))
            else: editor.set_value_map(values)
        self.Layout(); self.FitInside()

    def clear_values(self,form):
        self.show_form(form)

    def focus_field(self,path):
        def walk(editors):
            for editor in editors:
                if isinstance(editor,ScalarEditor) and editor.field.path==path:
                    parent = editor.GetParent()
                    while parent and parent is not self:
                        if isinstance(parent, FormSection):parent.expand()
                        if isinstance(parent, wx.CollapsiblePane):parent.Expand()
                        parent = parent.GetParent()
                    control=editor.rows[0][1]
                    control.SetFocus()
                    position = self.CalcUnscrolledPosition(self.ScreenToClient(control.GetScreenPosition()))
                    step_x, step_y = self.GetScrollPixelsPerUnit()
                    self.Scroll(max(0, position.x // max(1, step_x)), max(0, position.y // max(1, step_y) - 1))
                    return True
                nested=getattr(editor,"editors",None)
                if nested and walk(nested):
                    expand=getattr(editor,"expand",None)
                    if expand:expand()
                    return True
                instances=getattr(editor,"instances",None)
                if instances:
                    for _,children in instances:
                        if walk(children):return True
            return False
        return walk(self.editors)
