"""Recursive wx field editors. Imported only when the GUI is launched."""

import wx
from xml.etree import ElementTree as ET

from eaeu_xml.application.file_input import FileInputService, FileInputValue
from eaeu_xml.gui.controller import GuiController
from eaeu_xml.gui.dialogs import FieldInfoDialog


def _convert(text, datatype):
    if text == "": return None
    dtype = (datatype or "").lower()
    if dtype == "any_xml":
        try:return ET.fromstring(text)
        except ET.ParseError:return text
    if "quantity" in dtype or "integer" in dtype:
        try: return int(text)
        except ValueError: return text
    return text


def _group_instance_count(field, values):
    value=values.get(field.path)
    if isinstance(value,list):return len(value)
    if field.path in values or any(path.startswith(field.path+"/") for path in values):return 1
    return field.min_occurs or 0


def _is_boolean_field(field):
    dtype=(field.datatype or "").lower();return "indicator" in dtype or "boolean" in dtype


def _choice_value(field, raw):
    if _is_boolean_field(field):
        return True if raw in {"Да", "true"} else False if raw in {"Нет", "false"} else None
    return raw or None


def _file_description(value):
    media_type = value.media_type or "Тип не определён"
    return f"{value.filename} · {value.size} байт · {media_type}"


class ScalarEditor(wx.Panel):
    def __init__(self, parent, field, on_field_guide=None, on_value_changed=None, on_assisted_input=None):
        super().__init__(parent); self.field = field; self.rows = []
        self.on_field_guide=on_field_guide;self.on_value_changed=on_value_changed;self.on_assisted_input=on_assisted_input
        self.sizer = wx.BoxSizer(wx.VERTICAL); self.SetSizer(self.sizer)
        self._add_row(field.fixed_value)
        if field.repeatable:
            button = wx.Button(self, label="+ Добавить")
            button.Bind(wx.EVT_BUTTON, lambda event: self._add_row(None, layout=True))
            self.sizer.Add(button, 0, wx.TOP, 3)

    def _add_row(self, value=None, layout=False):
        row = wx.Panel(self); sizer = wx.BoxSizer(wx.VERTICAL); row.SetSizer(sizer)
        label = ("@" if self.field.is_attribute else "") + self.field.display_name + (" *" if self.field.required else "")
        if self.field.normative_input_policy=="CONDITIONAL":label += "  [Условно]"
        title=wx.StaticText(row,label=label); sizer.Add(title,0,wx.EXPAND|wx.BOTTOM,3)
        if self.field.normative_input_policy == "CLASSIFIER":
            marker=wx.StaticText(row,label="Классификатор")
            marker.SetToolTip("Набор допустимых значений не загружен в текущую конфигурацию.")
            sizer.Add(marker,0,wx.BOTTOM,3)
        input_row=wx.BoxSizer(wx.HORIZONTAL)
        dtype = (self.field.datatype or "").lower()
        if self.field.supports_file_picker:
            control = wx.TextCtrl(row, style=wx.TE_READONLY)
            control._file_value = None
            control.SetHint("Файл не выбран")
        elif self.field.ui_input_policy == "USER_SELECT" and self.field.allowed_values:
            choices = ["", *map(str, self.field.allowed_values)]
            control = wx.Choice(row, choices=choices)
            if value is not None and str(value) in choices: control.SetStringSelection(str(value))
        elif "indicator" in dtype or "boolean" in dtype:
            control = wx.Choice(row, choices=["", "Да", "Нет"]); control.SetSelection(1 if value is True else 2 if value is False else 0)
        else:
            control = wx.TextCtrl(row, value="" if value is None else str(value), style=wx.TE_READONLY if not self.field.editable else 0)
        help_text=GuiController.field_help(self.field); tooltip=GuiController.field_tooltip(self.field); control.SetToolTip(tooltip); title.SetToolTip(tooltip)
        if self.on_value_changed:
            event_type=wx.EVT_CHOICE if isinstance(control,wx.Choice) else wx.EVT_TEXT
            control.Bind(event_type,lambda event:(self.on_value_changed(self.field.path,isinstance(control,wx.Choice)),event.Skip()))
        if self.field.fixed_value is None and self.field.example_value is not None and isinstance(control,wx.TextCtrl): control.SetHint(str(self.field.example_value))
        input_row.Add(control,1,wx.EXPAND)
        def assist(action):
            if self.on_assisted_input and isinstance(control,wx.TextCtrl):
                value=self.on_assisted_input(action,self.field)
                if isinstance(value, FileInputValue):
                    control._file_value = value.value
                    control.SetValue(_file_description(value))
                elif value is not None:
                    control.SetValue(value)
        if self.field.supports_file_picker:
            choose=wx.Button(row,label="Выбрать файл…")
            choose.Bind(wx.EVT_BUTTON,lambda event:assist("PICK_FILE"))
            input_row.Add(choose,0,wx.LEFT,5)
            def clear_file(event):
                control._file_value=None
                control.SetValue("")
            clear=wx.Button(row,label="Очистить")
            clear.Bind(wx.EVT_BUTTON,clear_file)
            input_row.Add(clear,0,wx.LEFT,5)
        if self.field.show_identifier_generator:
            button=wx.Button(row,label="Сгенерировать");button.Bind(wx.EVT_BUTTON,lambda event:assist("GENERATE_IDENTIFIER"));input_row.Add(button,0,wx.LEFT,5)
        if self.field.show_today_button:
            button=wx.Button(row,label="Сегодня");button.Bind(wx.EVT_BUTTON,lambda event:assist("TODAY"));input_row.Add(button,0,wx.LEFT,5)
        if self.field.show_date_picker:
            button=wx.Button(row,label="Выбрать дату…");button.Bind(wx.EVT_BUTTON,lambda event:assist("PICK_DATE"));input_row.Add(button,0,wx.LEFT,5)
        if self.field.show_now_button:
            button=wx.Button(row,label="Сейчас ▼")
            def on_now(event):
                menu=wx.Menu()
                for label,zone in (("Системный часовой пояс","System"),("UTC","UTC"),("Выбрать часовой пояс…","PICK")):
                    item=menu.Append(wx.ID_ANY,label);self.Bind(wx.EVT_MENU,lambda evt,z=zone:assist("NOW:"+z),item)
                self.PopupMenu(menu,button.GetPosition());menu.Destroy()
            button.Bind(wx.EVT_BUTTON,on_now);input_row.Add(button,0,wx.LEFT,5)
        info=wx.Button(row,label="ⓘ",size=(34,-1)); info.SetToolTip(help_text)
        if self.on_field_guide: info.Bind(wx.EVT_BUTTON,lambda event:self.on_field_guide(self.field.path))
        else: info.Bind(wx.EVT_BUTTON,lambda event:FieldInfoDialog(self,self.field,help_text).ShowModal())
        input_row.Add(info,0,wx.LEFT,5)
        if self.field.repeatable:
            remove = wx.Button(row, label="Удалить")
            remove.Bind(wx.EVT_BUTTON, lambda event, target=row: self._remove(target))
            input_row.Add(remove,0,wx.LEFT,5)
        sizer.Add(input_row,0,wx.EXPAND)
        if self.field.ui_input_policy in {"EXTERNAL_SYSTEM", "UNRESOLVED_UI_POLICY", "CONDITIONAL"}:
            notice = {"EXTERNAL_SYSTEM": "Значение должно быть получено из внешней информационной системы.",
                      "UNRESOLVED_UI_POLICY": "⚠ Способ заполнения не определён.",
                      "CONDITIONAL": self.field.condition_description or "Поле зависит от условия правила."}[self.field.ui_input_policy]
            sizer.Add(wx.StaticText(row, label=notice), 0, wx.TOP, 2)
        self.rows.append((row, control)); self.sizer.Insert(max(0, len(self.rows)-1), row, 0, wx.EXPAND | wx.BOTTOM, 3)
        if layout: self.GetParent().Layout(); self.GetParent().FitInside()

    def _remove(self, row):
        if len(self.rows) <= max(1, self.field.min_occurs or 0): return
        pair = next(pair for pair in self.rows if pair[0] is row); self.rows.remove(pair); row.Destroy()
        self.GetParent().Layout(); self.GetParent().FitInside()

    def get_values(self):
        values=[]
        for _, control in self.rows:
            if isinstance(control, wx.Choice):
                raw=control.GetStringSelection();value=_choice_value(self.field,raw)
            elif self.field.supports_file_picker:
                value=control._file_value
            else: value=_convert(control.GetValue(), self.field.datatype)
            if value is not None: values.append(value)
        if not values: return {}
        return {self.field.path: values if self.field.repeatable else values[0]}

    def set_value(self, value):
        values=value if isinstance(value,list) else [value]
        while len(self.rows)<len(values): self._add_row()
        for index,(_,control) in enumerate(self.rows):
            item=values[index] if index<len(values) else None
            if isinstance(control,wx.Choice):
                if _is_boolean_field(self.field):control.SetSelection(1 if item is True else 2 if item is False else 0)
                else:control.SetStringSelection("" if item is None else str(item))
            elif self.field.supports_file_picker:
                if item in (None, ""):
                    control._file_value=None
                    control.SetValue("")
                else:
                    restored=FileInputService.restored(str(item))
                    control._file_value=restored.value
                    control.SetValue(_file_description(restored))
            else: control.SetValue("" if item is None else str(item))


class GroupEditor(wx.Panel):
    def __init__(self, parent, field, editor_factory, force_expand=False):
        super().__init__(parent);outer=wx.BoxSizer(wx.VERTICAL);self.SetSizer(outer)
        group_label=field.display_name + (" *" if field.required else "") + ("  [Условно]" if field.normative_input_policy=="CONDITIONAL" else "")
        self.pane=wx.CollapsiblePane(self,label=group_label);self.pane.SetToolTip(GuiController.field_help(field));outer.Add(self.pane,0,wx.EXPAND)
        box=self.pane.GetPane();content=wx.BoxSizer(wx.VERTICAL);box.SetSizer(content)
        callback=getattr(getattr(editor_factory,"__self__",None),"on_field_guide",None)
        value_callback=getattr(getattr(editor_factory,"__self__",None),"on_value_changed",None)
        assist_callback=getattr(getattr(editor_factory,"__self__",None),"on_assisted_input",None)
        self.field=field; self.value_editor = ScalarEditor(box, field, callback,value_callback,assist_callback) if field.ui_input_policy != "GROUP" or field.supports_file_picker else None
        self.editors=([self.value_editor] if self.value_editor else []) + [editor_factory(box, child) for child in field.children if child.visibility != "HIDDEN"]
        for editor in self.editors: content.Add(editor, 0, wx.EXPAND | wx.ALL, 4)
        descendants=sum(1 for _ in self._walk(field.children));self.pane.Collapse(not (force_expand or field.required or descendants<=8))
        self.pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED,self._on_toggle)

    @classmethod
    def _walk(cls,fields):
        for field in fields:
            yield field
            yield from cls._walk(field.children)

    def _on_toggle(self,event):
        window=self
        while window:
            window.Layout()
            if hasattr(window,"FitInside"):window.FitInside()
            window=window.GetParent()
        event.Skip()

    def expand(self):
        self.pane.Expand();self._on_toggle(type("Event",(),{"Skip":lambda self:None})())

    def get_values(self):
        result={}
        for editor in self.editors: result.update(editor.get_values())
        if result: result.setdefault(self.field.path, None)
        return result

    def set_value_map(self, values):
        for editor in self.editors:
            if isinstance(editor,ScalarEditor): editor.set_value(values.get(editor.field.path))
            else: editor.set_value_map(values)


class RepeatingGroupEditor(wx.Panel):
    def __init__(self, parent, field, editor_factory, on_value_changed=None):
        super().__init__(parent); self.field=field; self.editor_factory=editor_factory; self.instances=[];self.on_value_changed=on_value_changed
        self.sizer=wx.BoxSizer(wx.VERTICAL); self.SetSizer(self.sizer)
        count=field.min_occurs or 0
        for _ in range(count): self._add_instance()
        suffix=" [Условно]" if field.normative_input_policy=="CONDITIONAL" else ""
        button=wx.Button(self,label=f"+ Добавить: {field.display_name}{suffix}"); button.Bind(wx.EVT_BUTTON,lambda event:self._add_instance(layout=True)); self.sizer.Add(button,0,wx.TOP,3)

    def _add_instance(self,layout=False):
        panel=wx.Panel(self); static=wx.StaticBox(panel,label=f"{self.field.display_name} [{len(self.instances)+1}]"); static.SetToolTip(GuiController.field_help(self.field)); box=wx.StaticBoxSizer(static,wx.VERTICAL); panel.SetSizer(box)
        editors=[self.editor_factory(static,child) for child in self.field.children if child.visibility!="HIDDEN"]
        for editor in editors: box.Add(editor,0,wx.EXPAND|wx.ALL,4)
        remove=wx.Button(static,label="Удалить")
        remove.Bind(wx.EVT_BUTTON,lambda event,target=panel:self._remove(target)); box.Add(remove,0,wx.ALIGN_RIGHT|wx.ALL,3)
        self.instances.append((panel,editors)); self.sizer.Insert(max(0,len(self.instances)-1),panel,0,wx.EXPAND|wx.BOTTOM,5)
        if layout: self.GetParent().Layout(); self.GetParent().FitInside()
        if layout and self.on_value_changed:self.on_value_changed(self.field.path,True)

    def _remove(self,panel):
        minimum=self.field.min_occurs or 0
        if len(self.instances)<=minimum:return
        item=next(item for item in self.instances if item[0] is panel); self.instances.remove(item); panel.Destroy(); self.GetParent().Layout(); self.GetParent().FitInside()
        if self.on_value_changed:self.on_value_changed(self.field.path,True)

    def get_values(self):
        if not self.instances:return {}
        combined={self.field.path:[None]*len(self.instances)}
        collected={}
        for _,editors in self.instances:
            instance={}
            for editor in editors: instance.update(editor.get_values())
            for path,value in instance.items(): collected.setdefault(path,[]).append(value)
        combined.update(collected); return combined

    def set_value_map(self,values):
        count=_group_instance_count(self.field,values)
        while len(self.instances)<count:self._add_instance()
        while len(self.instances)>count:
            panel,_=self.instances.pop(); panel.Destroy()
        for index,(_,editors) in enumerate(self.instances):
            for editor in editors:
                if isinstance(editor,ScalarEditor):
                    raw=values.get(editor.field.path); editor.set_value(raw[index] if isinstance(raw,list) and index<len(raw) else raw)
                else: editor.set_value_map(values)
