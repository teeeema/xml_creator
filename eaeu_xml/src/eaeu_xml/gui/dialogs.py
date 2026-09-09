import wx
import wx.adv
from pathlib import Path

from eaeu_xml.gui.controller import GuiSettings
from eaeu_xml.application.input_helpers import datetime_value, search_timezones


def show_error(parent, message, details=None):
    text=message + (f"\n\nDetails:\n{details}" if details else "")
    wx.MessageBox(text,"Ошибка",wx.OK|wx.ICON_ERROR,parent)


def issue_text(validation):
    if validation.is_valid and not validation.warnings: return "✓ Проверка пройдена"
    lines=[]
    for issue in (*validation.errors,*validation.warnings): lines.append(f"{issue.field_path or '—'} | {issue.severity} | {issue.code} | {issue.message}")
    return "\n".join(lines)


class FieldInfoDialog(wx.Dialog):
    def __init__(self,parent,field,help_text):
        super().__init__(parent,title="Информация о поле",size=(620,520))
        sizer=wx.BoxSizer(wx.VERTICAL); self.SetSizer(sizer)
        title=wx.StaticText(self,label=field.display_name); font=title.GetFont(); font.MakeBold(); title.SetFont(font)
        text=wx.TextCtrl(self,value=help_text,style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2)
        sizer.Add(title,0,wx.EXPAND|wx.ALL,10); sizer.Add(text,1,wx.EXPAND|wx.LEFT|wx.RIGHT,10); sizer.Add(self.CreateButtonSizer(wx.OK),0,wx.EXPAND|wx.ALL,10)


class TextInfoDialog(wx.Dialog):
    def __init__(self,parent,title,text):
        super().__init__(parent,title=title,size=(760,420));sizer=wx.BoxSizer(wx.VERTICAL);self.SetSizer(sizer)
        content=wx.TextCtrl(self,value=text,style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2|wx.TE_WORDWRAP)
        sizer.Add(content,1,wx.EXPAND|wx.ALL,10);sizer.Add(self.CreateButtonSizer(wx.OK),0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,10)


class SettingsDialog(wx.Dialog):
    def __init__(self,parent,settings):
        super().__init__(parent,title="Настройки",size=(700,420))
        outer=wx.BoxSizer(wx.VERTICAL); self.SetSizer(outer); grid=wx.FlexGridSizer(7,3,10,8); grid.AddGrowableCol(1,1)
        self.root=wx.TextCtrl(self,value=str(settings.processes_root)); browse=wx.Button(self,label="Выбрать…"); browse.Bind(wx.EVT_BUTTON,self.on_browse)
        self.mode=wx.Choice(self,choices=["TEST","STRICT"]); self.mode.SetStringSelection(settings.mode)
        self.seed=wx.SpinCtrl(self,min=0,max=2147483647,initial=settings.seed)
        self.autosave=wx.CheckBox(self,label="Включено"); self.autosave.SetValue(settings.autosave_enabled)
        self.autosave_delay=wx.SpinCtrl(self,min=2,max=30,initial=settings.autosave_delay_seconds)
        self.drafts=wx.TextCtrl(self,value=str(settings.drafts_directory or "")); browse_drafts=wx.Button(self,label="Выбрать…"); browse_drafts.Bind(wx.EVT_BUTTON,self.on_browse_drafts)
        self.timezone=wx.TextCtrl(self,value=settings.default_timezone)
        grid.Add(wx.StaticText(self,label="Корень общих процессов"),0,wx.ALIGN_CENTER_VERTICAL); grid.Add(self.root,1,wx.EXPAND); grid.Add(browse)
        grid.Add(wx.StaticText(self,label="Режим"),0,wx.ALIGN_CENTER_VERTICAL); grid.Add(self.mode,1,wx.EXPAND); grid.AddSpacer(1)
        grid.Add(wx.StaticText(self,label="Seed"),0,wx.ALIGN_CENTER_VERTICAL); grid.Add(self.seed,1,wx.EXPAND); grid.AddSpacer(1)
        grid.Add(wx.StaticText(self,label="Автосохранение"),0,wx.ALIGN_CENTER_VERTICAL); grid.Add(self.autosave,1,wx.EXPAND); grid.AddSpacer(1)
        grid.Add(wx.StaticText(self,label="Задержка, секунд"),0,wx.ALIGN_CENTER_VERTICAL); grid.Add(self.autosave_delay,1,wx.EXPAND); grid.AddSpacer(1)
        grid.Add(wx.StaticText(self,label="Папка черновиков"),0,wx.ALIGN_CENTER_VERTICAL); grid.Add(self.drafts,1,wx.EXPAND); grid.Add(browse_drafts)
        grid.Add(wx.StaticText(self,label="Часовой пояс по умолчанию"),0,wx.ALIGN_CENTER_VERTICAL); grid.Add(self.timezone,1,wx.EXPAND); grid.Add(wx.StaticText(self,label="System / UTC / IANA"))
        outer.Add(grid,1,wx.EXPAND|wx.ALL,12); outer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL),0,wx.EXPAND|wx.ALL,12)

    def on_browse(self,event):
        with wx.DirDialog(self,"Выберите корневую папку общих процессов",defaultPath=self.root.GetValue(),style=wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST) as dialog:
            if dialog.ShowModal()==wx.ID_OK:self.root.SetValue(dialog.GetPath())

    def on_browse_drafts(self,event):
        with wx.DirDialog(self,"Выберите папку черновиков",defaultPath=self.drafts.GetValue(),style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal()==wx.ID_OK:self.drafts.SetValue(dialog.GetPath())

    def get_settings(self): return GuiSettings(Path(self.root.GetValue()),self.mode.GetStringSelection(),self.seed.GetValue(),self.autosave.GetValue(),self.autosave_delay.GetValue(),Path(self.drafts.GetValue()),self.timezone.GetValue().strip() or "System")


class TimezoneDialog(wx.Dialog):
    def __init__(self,parent,initial=""):
        super().__init__(parent,title="Выбор часового пояса",size=(680,520)); self.selected=None
        outer=wx.BoxSizer(wx.VERTICAL);self.SetSizer(outer)
        outer.Add(wx.StaticText(self,label="Поиск по IANA name или названию города:"),0,wx.ALL,10)
        self.search=wx.SearchCtrl(self,value=initial);outer.Add(self.search,0,wx.EXPAND|wx.LEFT|wx.RIGHT,10)
        self.results=wx.ListBox(self);outer.Add(self.results,1,wx.EXPAND|wx.ALL,10)
        self.preview=wx.StaticText(self);outer.Add(self.preview,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,10)
        outer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL),0,wx.EXPAND|wx.ALL,10)
        self.search.Bind(wx.EVT_TEXT,self._refresh);self.results.Bind(wx.EVT_LISTBOX,self._select);self._refresh(None)
    def _refresh(self,event):
        values=search_timezones(self.search.GetValue())[:500];self.results.Set(values)
        if values:self.results.SetSelection(0);self._select(None)
    def _select(self,event):
        self.selected=self.results.GetStringSelection() or None
        self.preview.SetLabel(f"Текущее время: {datetime_value(self.selected)}" if self.selected else "")
    def get_timezone(self):return self.selected


class DateSelectionDialog(wx.Dialog):
    def __init__(self,parent):
        super().__init__(parent,title="Выбор даты",size=(420,180));sizer=wx.BoxSizer(wx.VERTICAL);self.SetSizer(sizer)
        self.picker=wx.adv.DatePickerCtrl(self,style=wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY)
        sizer.Add(self.picker,0,wx.EXPAND|wx.ALL,12);sizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL),0,wx.EXPAND|wx.ALL,12)
    def get_value(self):
        value=self.picker.GetValue();return f"{value.GetYear():04d}-{value.GetMonth()+1:02d}-{value.GetDay():02d}"


class ProcessIssuesDialog(wx.Dialog):
    def __init__(self,parent,controller):
        super().__init__(parent,title="Проблемы процесса",size=(950,650)); self.controller=controller; self.items=()
        outer=wx.BoxSizer(wx.VERTICAL); self.SetSizer(outer); top=wx.BoxSizer(wx.HORIZONTAL)
        top.Add(wx.StaticText(self,label=f"Процесс: {controller.process_code}"),1,wx.ALIGN_CENTER_VERTICAL)
        self.filter=wx.Choice(self,choices=["Все","Блокирующие","Предупреждения"]); self.filter.SetSelection(0); self.filter.Bind(wx.EVT_CHOICE,self.on_filter); top.Add(self.filter,0)
        outer.Add(top,0,wx.EXPAND|wx.ALL,10)
        self.list=wx.ListCtrl(self,style=wx.LC_REPORT|wx.BORDER_SUNKEN); self.list.InsertColumn(0,"Severity",width=100); self.list.InsertColumn(1,"Категория",width=180); self.list.InsertColumn(2,"Проблема",width=580)
        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED,self.on_select); self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.on_select); outer.Add(self.list,1,wx.EXPAND|wx.LEFT|wx.RIGHT,10)
        self.details=wx.TextCtrl(self,style=wx.TE_MULTILINE|wx.TE_READONLY); self.details.SetMinSize((-1,190)); outer.Add(self.details,0,wx.EXPAND|wx.ALL,10); outer.Add(self.CreateButtonSizer(wx.CLOSE),0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,10)
        self.refresh()

    def on_filter(self,event):self.refresh()
    def refresh(self):
        key=("ALL","BLOCKING","WARNINGS")[self.filter.GetSelection()]; self.items=self.controller.filtered_process_issues(key); self.list.DeleteAllItems(); self.details.Clear()
        for issue in self.items:
            index=self.list.InsertItem(self.list.GetItemCount(),issue.severity); self.list.SetItem(index,1,issue.category); self.list.SetItem(index,2,f"{issue.title}: {issue.code}")
    def on_select(self,event):
        issue=self.items[event.GetIndex()]; lines=[issue.title,issue.description,"",f"Код: {issue.code}",f"Категория: {issue.category}",
            f"Блокирует TEST generation: {'да' if issue.blocks_test_generation else 'нет'}",
            f"Блокирует STRICT generation: {'да' if issue.blocks_strict_generation else 'нет'}"]
        if issue.affected_messages:lines.append("Сообщения: "+", ".join(issue.affected_messages))
        if issue.affected_structures:lines.append("Структуры: "+", ".join(issue.affected_structures))
        if issue.referenced_fields:lines.append("Реквизиты: "+", ".join(issue.referenced_fields))
        lines.extend("Источник: "+source for source in issue.source_display)
        if issue.suggested_action:lines.extend(("","Что сделать:",issue.suggested_action))
        self.details.SetValue("\n".join(lines))
