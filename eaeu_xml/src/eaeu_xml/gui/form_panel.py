import wx

from eaeu_xml.gui.field_controls import GroupEditor, RepeatingGroupEditor, ScalarEditor
from eaeu_xml.gui.theme import GuiTheme


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
        for field in form.fields:
            if field.visibility == "HIDDEN": continue
            editor=self._editor(self,field); self.editors.append(editor); self.root_sizer.Add(editor,0,wx.EXPAND|wx.ALL,5)
        empty_message=getattr(form,"empty_message",None)
        if empty_message:self.root_sizer.Add(wx.StaticText(self,label=empty_message),0,wx.ALL,12)
        self.Layout(); self.FitInside(); self.Scroll(0,0)

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
                    control=editor.rows[0][1]; control.SetFocus(); self.ScrollChildIntoView(control); return True
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
