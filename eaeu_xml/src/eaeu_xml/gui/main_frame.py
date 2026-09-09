import logging
from datetime import datetime
from pathlib import Path
import traceback
from dataclasses import replace

import wx

from eaeu_xml.application import FormDisplayMode
from eaeu_xml.gui.controller import GuiController
from eaeu_xml.gui.dialogs import DateSelectionDialog, ProcessIssuesDialog, SettingsDialog, TextInfoDialog, TimezoneDialog, issue_text, show_error
from eaeu_xml.gui.form_panel import FormPanel
from eaeu_xml.gui.xml_panel import XmlPanel
from eaeu_xml.gui.guide_dialog import GuideDialog

LOG = logging.getLogger(__name__)


def copy_text_to_clipboard(clipboard, text):
    if not text or not clipboard.Open():return False
    try:
        if not clipboard.SetData(wx.TextDataObject(text)):return False
        flush=getattr(clipboard,"Flush",None)
        if flush:flush()
        return True
    finally:clipboard.Close()


class MainFrame(wx.Frame):
    def __init__(self, application):
        display=wx.GetDisplaySize(); size=(min(1280,max(760,display.width-120)),min(900,max(600,display.height-140)))
        super().__init__(None,title="EAEU XML Creator",size=size); self.SetMinSize((700,560)); self.controller=GuiController(application); self._synchronizing_form=False; self._layout_pending=False
        self.Bind(wx.EVT_SIZE,self._on_frame_size)
        config=wx.Config("EAEU XML Creator");saved_timezone=config.Read("default_timezone","System")
        self.controller.settings=replace(self.controller.settings,default_timezone=saved_timezone)
        self._build_menu(); self.Bind(wx.EVT_CLOSE,self._safe(self.on_close))
        self.CreateStatusBar(); root=wx.Panel(self); outer=wx.BoxSizer(wx.VERTICAL); root.SetSizer(outer)
        top=wx.BoxSizer(wx.HORIZONTAL); title=wx.StaticText(root,label="EAEU XML Creator"); font=title.GetFont(); font.MakeBold(); font.SetPointSize(font.GetPointSize()+2); title.SetFont(font)
        problems=wx.Button(root,label="Проблемы процесса"); problems.Bind(wx.EVT_BUTTON,self._safe(self.on_process_issues))
        settings=wx.Button(root,label="Настройки…"); settings.Bind(wx.EVT_BUTTON,self._safe(self.on_settings)); top.Add(title,1,wx.ALIGN_CENTER_VERTICAL); top.Add(problems,0,wx.RIGHT,6); top.Add(settings,0)
        outer.Add(top,0,wx.EXPAND|wx.ALL,8)
        self.notebook=wx.Notebook(root); self.data_tab=wx.Panel(self.notebook); self.xml_tab=wx.Panel(self.notebook)
        self.notebook.AddPage(self.data_tab,"Заполнение данных"); self.notebook.AddPage(self.xml_tab,"XML"); outer.Add(self.notebook,1,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8)
        self._build_data_tab(); self._build_xml_tab(); self._load_processes()
        # No persisted window position exists yet; if one is added, restore it
        # instead of applying this default launch position.
        self.CentreOnScreen()
        self.autosave_timer=wx.Timer(self); self.Bind(wx.EVT_TIMER,self._safe(self.on_autosave_timer),self.autosave_timer); self.autosave_timer.Start(750)
        wx.CallAfter(self._offer_recovery)

    def _build_menu(self):
        menu=wx.Menu(); open_item=menu.Append(wx.ID_OPEN,"Открыть черновик…\tCtrl+O"); save_item=menu.Append(wx.ID_SAVE,"Сохранить черновик\tCtrl+S"); save_as=menu.Append(wx.ID_SAVEAS,"Сохранить черновик как…")
        menu.AppendSeparator();open_session=menu.Append(wx.ID_ANY,"Открыть сессию…");save_session=menu.Append(wx.ID_ANY,"Сохранить сессию…")
        menu.AppendSeparator(); close_item=menu.Append(wx.ID_EXIT,"Выход")
        guide_menu=wx.Menu(); guide_item=guide_menu.Append(wx.ID_HELP,"Сводка…\tF1")
        bar=wx.MenuBar(); bar.Append(menu,"Файл"); bar.Append(guide_menu,"Сводка"); self.SetMenuBar(bar)
        self.Bind(wx.EVT_MENU,self._safe(self.on_open_draft),open_item); self.Bind(wx.EVT_MENU,self._safe(self.on_save_draft),save_item); self.Bind(wx.EVT_MENU,self._safe(self.on_save_draft_as),save_as); self.Bind(wx.EVT_MENU,lambda event:self.Close(),close_item)
        self.Bind(wx.EVT_MENU,self._safe(self.on_open_session),open_session);self.Bind(wx.EVT_MENU,self._safe(self.on_save_session),save_session);self._save_session_menu=save_session
        self.Bind(wx.EVT_MENU,self._safe(self.on_guide),guide_item)

    def _build_data_tab(self):
        outer=wx.BoxSizer(wx.VERTICAL); self.data_tab.SetSizer(outer);self.buttons={}
        self.process_choice=wx.ComboBox(self.data_tab,style=wx.CB_READONLY); self.transaction_choice=wx.ComboBox(self.data_tab,style=wx.CB_READONLY); self.message_choice=wx.ComboBox(self.data_tab,style=wx.CB_READONLY)
        self.selector_info_buttons={};self._selector_info={}
        for key,label,choice in (("process","Общий процесс:",self.process_choice),("transaction","Транзакция:",self.transaction_choice),("message","Сообщение:",self.message_choice)):
            outer.Add(wx.StaticText(self.data_tab,label=label),0,wx.LEFT|wx.RIGHT|wx.TOP,8)
            row=wx.BoxSizer(wx.HORIZONTAL);info=wx.Button(self.data_tab,label="ⓘ",size=(38,-1));info.Bind(wx.EVT_BUTTON,lambda event,item=key:self._show_selector_info(item));row.Add(choice,1,wx.EXPAND);row.Add(info,0,wx.LEFT,5)
            self.selector_info_buttons[key]=info;outer.Add(row,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8)
        self.status_block=wx.StaticText(self.data_tab); outer.Add(self.status_block,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8)
        session_box=wx.StaticBoxSizer(wx.VERTICAL,self.data_tab,"Сессия транзакции")
        session_parent=session_box.GetStaticBox()
        self.session_info=wx.StaticText(session_parent,label="Новая сессия будет создана обычным runtime при формировании первого сообщения.")
        session_box.Add(self.session_info,0,wx.EXPAND|wx.ALL,6)
        session_actions=wx.WrapSizer(wx.HORIZONTAL)
        for label,handler in (("Открыть сессию",self.on_open_session),("Продолжить сессию",self.on_continue_session),
                              ("Открыть как новую",self.on_open_as_new),("Сохранить сессию",self.on_save_session),
                              ("ⓘ Сведения о сессии",self.on_session_info)):
            button=wx.Button(session_parent,label=label);button.Bind(wx.EVT_BUTTON,self._safe(handler));session_actions.Add(button,0,wx.RIGHT|wx.BOTTOM,6);self.buttons[label]=button
        session_box.Add(session_actions,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,6);outer.Add(session_box,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8)
        filter_row=wx.WrapSizer(wx.HORIZONTAL)
        filter_row.Add(wx.StaticText(self.data_tab,label="Показывать:"),0,wx.ALIGN_CENTER_VERTICAL|wx.RIGHT,6)
        self.form_mode=wx.Choice(self.data_tab,choices=["Все поля","Только обязательные","Только для заполнения","С ошибками","Только заполненные"])
        self._form_modes=(FormDisplayMode.ALL,FormDisplayMode.REQUIRED,FormDisplayMode.USER_FIELDS,FormDisplayMode.ERRORS,FormDisplayMode.FILLED)
        self.form_mode.SetSelection(0);filter_row.Add(self.form_mode,0,wx.RIGHT,8)
        self.form_search=wx.SearchCtrl(self.data_tab,style=wx.TE_PROCESS_ENTER);self.form_search.SetDescriptiveText("Поиск по полям…");self.form_search.ShowCancelButton(True);self.form_search.SetMinSize((220,-1));filter_row.Add(self.form_search,0,wx.RIGHT,8)
        self.user_fields_toggle=wx.Button(self.data_tab,label="Показать только поля для заполнения");filter_row.Add(self.user_fields_toggle,0)
        outer.Add(filter_row,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8)
        self.form_summary=wx.StaticText(self.data_tab);outer.Add(self.form_summary,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8)
        self.hidden_condition_info=wx.Button(self.data_tab,label="ⓘ Скрыто текущим условием");self.hidden_condition_info.Hide();self.hidden_condition_info.Bind(wx.EVT_BUTTON,self._safe(self.on_hidden_condition_guide));outer.Add(self.hidden_condition_info,0,wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.BOTTOM,8);self._hidden_condition_paths=()
        self.form_panel=FormPanel(self.data_tab,self.on_field_guide,self.on_form_value_changed,self.on_assisted_input); outer.Add(self.form_panel,1,wx.EXPAND|wx.LEFT|wx.RIGHT,8)
        buttons=wx.WrapSizer(wx.HORIZONTAL)
        for label,handler in (("Открыть черновик",self.on_open_draft),("Сохранить черновик",self.on_save_draft),("Заполнить тестовыми",self.on_test_data),("Проверить",self.on_validate),("Очистить",self.on_clear),("Начать новую транзакцию",self.on_new_session),("Сформировать XML",self.on_generate)):
            button=wx.Button(self.data_tab,label=label); button.Bind(wx.EVT_BUTTON,self._safe(handler)); buttons.Add(button,0,wx.RIGHT,6); self.buttons[label]=button
        outer.Add(buttons,0,wx.EXPAND|wx.ALL,8)
        self.validation_summary=wx.StaticText(self.data_tab,label=""); outer.Add(self.validation_summary,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8)
        self.issue_list=wx.ListCtrl(self.data_tab,style=wx.LC_REPORT|wx.BORDER_SUNKEN); self.issue_list.InsertColumn(0,"Поле",width=260); self.issue_list.InsertColumn(1,"Severity",width=90); self.issue_list.InsertColumn(2,"Сообщение",width=650)
        self.issue_list.SetMinSize((-1,110)); self.issue_list.Hide(); outer.Add(self.issue_list,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8); self.issue_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.on_issue_activate)
        self.issue_list.Bind(wx.EVT_LIST_ITEM_SELECTED,self.on_issue_selected);self.issue_info=wx.Button(self.data_tab,label="ⓘ Полный текст");self.issue_info.Disable();self.issue_info.Hide();self.issue_info.Bind(wx.EVT_BUTTON,self.on_issue_info);outer.Add(self.issue_info,0,wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT|wx.BOTTOM,8);self._validation_issues=()
        self.process_choice.Bind(wx.EVT_COMBOBOX,self._safe(self.on_process)); self.transaction_choice.Bind(wx.EVT_COMBOBOX,self._safe(self.on_transaction)); self.message_choice.Bind(wx.EVT_COMBOBOX,self._safe(self.on_message))
        self.form_mode.Bind(wx.EVT_CHOICE,self._safe(self.on_form_mode));self.user_fields_toggle.Bind(wx.EVT_BUTTON,self._safe(self.on_user_fields_toggle))
        self.form_search.Bind(wx.EVT_TEXT,self._safe(self.on_form_search));self.form_search.Bind(wx.EVT_TEXT_ENTER,self._safe(self.on_form_search_now));self._search_later=None
        self._condition_later=None;self._pending_condition_sources=set()

    def _build_xml_tab(self):
        outer=wx.BoxSizer(wx.VERTICAL); self.xml_tab.SetSizer(outer); self.xml_panel=XmlPanel(self.xml_tab); outer.Add(self.xml_panel,1,wx.EXPAND|wx.ALL,6)
        buttons=wx.WrapSizer(wx.HORIZONTAL); copy=wx.Button(self.xml_tab,label="Копировать XML"); save=wx.Button(self.xml_tab,label="Сохранить XML")
        copy.Bind(wx.EVT_BUTTON,self._safe(self.on_copy)); save.Bind(wx.EVT_BUTTON,self._safe(self.on_save)); self.buttons.update({"Копировать XML":copy,"Сохранить XML":save})
        buttons.Add(copy,0,wx.RIGHT,6); buttons.Add(save,0); outer.Add(buttons,0,wx.EXPAND|wx.ALL,8)

    def _on_frame_size(self,event):
        event.Skip()
        if not self._layout_pending:
            self._layout_pending=True; wx.CallAfter(self._apply_responsive_layout)

    def _apply_responsive_layout(self):
        self._layout_pending=False
        if self.IsBeingDeleted():return
        data_tab=getattr(self,"data_tab",None)
        if data_tab:
            wrap_width=max(280,data_tab.GetClientSize().width-32)
            for control in (getattr(self,"status_block",None),getattr(self,"form_summary",None),getattr(self,"validation_summary",None)):
                if control:control.Wrap(wrap_width)
            session_info=getattr(self,"session_info",None)
            if session_info:session_info.Wrap(wrap_width)
            data_tab.Layout()
            form_panel=getattr(self,"form_panel",None)
            if form_panel:
                form_panel.Layout(); form_panel.FitInside()
        xml_tab=getattr(self,"xml_tab",None)
        if xml_tab:xml_tab.Layout()

    def _safe(self,handler):
        def wrapped(event):
            try:handler(event)
            except Exception:
                details=traceback.format_exc(); LOG.exception("GUI boundary failure"); show_error(self,"Произошла внутренняя ошибка.",details)
        return wrapped

    def on_assisted_input(self, action, field):
        if action=="PICK_FILE":
            with wx.FileDialog(self,"Выберите файл",wildcard="Все файлы (*.*)|*.*",style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as dialog:
                if dialog.ShowModal()!=wx.ID_OK:return None
                path=Path(dialog.GetPath())
            file_size=path.stat().st_size
            if file_size > self.controller.application.file_input_service.warning_threshold:
                size=file_size/(1024*1024)
                if wx.MessageBox(f"Размер выбранного файла: {size:.1f} МБ.\nФайл будет включён в XML. Продолжить?","Большой файл",wx.YES_NO|wx.ICON_WARNING,self)!=wx.YES:return None
            value=self.controller.application.load_file_value(path)
        elif action=="PICK_DATE":
            dialog=DateSelectionDialog(self)
            try:value=dialog.get_value() if dialog.ShowModal()==wx.ID_OK else None
            finally:dialog.Destroy()
            if value is None:return None
        elif action.startswith("NOW:"):
            zone=action.split(":",1)[1]
            if zone=="PICK":
                dialog=TimezoneDialog(self,self.controller.settings.last_used_timezone or "")
                try:
                    if dialog.ShowModal()!=wx.ID_OK:return None
                    zone=dialog.get_timezone()
                finally:dialog.Destroy()
                if not zone:return None
            value=self.controller.assisted_value("NOW",timezone_name=zone,temporal_kind=field.assisted_input_kind or "DATETIME")
        else:value=self.controller.assisted_value(action)
        self.SetStatusText("Значение сформировано. Оно остаётся доступным для ручного изменения.")
        return value

    def _load_processes(self):
        label=lambda p:self.controller.short_text(p.process_code,p.name,normative_document_number=p.normative_document_number)
        self.process_choice.Set([label(p) for p in self.controller.processes]); self.process_choice.SetToolTip("\n".join(label(p) for p in self.controller.processes))
        if self.controller.processes:
            index=next((i for i,p in enumerate(self.controller.processes) if p.process_code==self.controller.process_code),0); self.process_choice.SetSelection(index); self._refresh_transactions()
            self._set_selector_info("process",self.controller.processes[index].process_code,self.controller.processes[index].name)
        else:self.SetStatusText("В выбранной папке процессы не найдены.")

    def _refresh_transactions(self):
        self.transaction_choice.Set([self.controller.short_text(t.transaction_code,t.name) for t in self.controller.transactions]); self.transaction_choice.SetToolTip("\n".join(f"{t.transaction_code} — {t.name}" for t in self.controller.transactions))
        index=next((i for i,t in enumerate(self.controller.transactions) if t.transaction_code==self.controller.transaction_code),wx.NOT_FOUND); self.transaction_choice.SetSelection(index); self._refresh_messages()
        if index!=wx.NOT_FOUND:self._set_selector_info("transaction",self.controller.transactions[index].transaction_code,self.controller.transactions[index].name)

    def _refresh_messages(self):
        self.message_choice.Set([" ".join(filter(None,(self.controller.message_marker(m.generation_status),self.controller.short_text(m.message_code,m.name)))) for m in self.controller.messages]); self.message_choice.SetToolTip("\n".join(f"{m.message_code} — {m.name}" for m in self.controller.messages))
        index=next((i for i,m in enumerate(self.controller.messages) if m.message_code==self.controller.message_code),wx.NOT_FOUND); self.message_choice.SetSelection(index); self._refresh_form()
        if index!=wx.NOT_FOUND:self._set_selector_info("message",self.controller.messages[index].message_code,self.controller.messages[index].name)

    def _refresh_form(self):
        m=self.controller.current_message
        if not m:return
        self.status_block.SetLabel(f"Структура: {m.structure_id}    Версия: {m.active_version or 'не задана'}    Статус: {m.generation_status}    Режим: {self.controller.settings.mode}")
        self.form_search.ChangeValue(self.controller.search_query);self._sync_form_mode();self._refresh_visible_form()
        self.xml_panel.clear(); self._clear_issues(); self._sync_buttons(); self.notebook.SetSelection(0); self._update_title()
        self.SetStatusText(f"Process: {self.controller.process_code} | TRN: {self.controller.transaction_code} | Status: {m.generation_status}")

    def _refresh_visible_form(self,focus_path=None):
        presentation=self.controller.form_presentation
        if not presentation:return
        self._synchronizing_form=True
        try:self.form_panel.show_form(presentation);self.form_panel.set_values(self.controller.values)
        finally:self._synchronizing_form=False
        summary=self.controller.message_input_summary
        self.form_summary.SetLabel(
            f"{self.controller.message_code}    Всего реквизитов: {summary.visible_fields}    "
            f"Пользователь заполняет: {summary.manual_fields}    Автоматически: {summary.automatic_fields}    "
            f"Классификаторы: {summary.classifier_fields}    Условные: {summary.conditional_fields}    "
            f"Не определено: {summary.unresolved_fields}\n"
            f"Условных реквизитов: {summary.conditional_total}    Сейчас применимо: {summary.conditional_active}    "
            f"Не применимо: {summary.conditional_inactive}    Условие не определено: {summary.conditional_unknown}"
        )
        self._hidden_condition_paths=presentation.conditionally_hidden_search_paths
        self.hidden_condition_info.SetLabel(f"ⓘ Скрыто текущим условием: {len(self._hidden_condition_paths)}")
        self.hidden_condition_info.Show(bool(self._hidden_condition_paths))
        if focus_path:wx.CallAfter(self.form_panel.focus_field,focus_path)
        self.data_tab.Layout()

    def _sync_form_mode(self):
        self.form_mode.SetSelection(self._form_modes.index(self.controller.display_mode))
        self.user_fields_toggle.SetLabel("Показать все поля" if self.controller.display_mode is FormDisplayMode.USER_FIELDS else "Показать только поля для заполнения")

    def _capture_and_refresh_filter(self,focus_path=None):
        self._capture_values();self._sync_form_mode();self._refresh_visible_form(focus_path)

    def on_form_mode(self,event):
        self._capture_values();self.controller.set_display_mode(self._form_modes[self.form_mode.GetSelection()]);self._sync_form_mode();self._refresh_visible_form()

    def on_user_fields_toggle(self,event):
        self._capture_values();target=FormDisplayMode.ALL if self.controller.display_mode is FormDisplayMode.USER_FIELDS else FormDisplayMode.USER_FIELDS
        self.controller.set_display_mode(target);self._sync_form_mode();self._refresh_visible_form()

    def on_form_search(self,event):
        if self._search_later:self._search_later.Stop()
        self._search_later=wx.CallLater(225,self._apply_form_search)

    def on_form_search_now(self,event):
        if self._search_later:self._search_later.Stop()
        self._apply_form_search()

    def _apply_form_search(self):
        self._capture_values();self.controller.set_search_query(self.form_search.GetValue());self._refresh_visible_form()

    def on_form_value_changed(self,path,immediate=False):
        if self._synchronizing_form or path not in self.controller.condition_dependency_index:return
        self._pending_condition_sources.add(path)
        if self._condition_later:self._condition_later.Stop()
        if immediate:wx.CallAfter(self._apply_condition_change)
        else:self._condition_later=wx.CallLater(225,self._apply_condition_change)

    def _apply_condition_change(self):
        if self._synchronizing_form:return
        self._capture_values();self.controller.reevaluate_condition_sources(self._pending_condition_sources);self._pending_condition_sources.clear();self._refresh_visible_form()

    def on_process(self,event):
        if not self._confirm_dirty():self._load_processes(); return
        selected=self.controller.processes[self.process_choice.GetSelection()];self.controller.select_process(selected.process_code);self._set_selector_info("process",selected.process_code,selected.name);self._refresh_transactions()
    def on_transaction(self,event):
        if not self._confirm_dirty():self._refresh_transactions(); return
        self.controller.select_transaction(self.controller.transactions[self.transaction_choice.GetSelection()].transaction_code); self._refresh_messages()
    def on_message(self,event):
        if not self._confirm_dirty():self._refresh_messages(); return
        self.controller.select_message(self.controller.messages[self.message_choice.GetSelection()].message_code); self._refresh_form()
    def on_test_data(self,event):self.form_panel.set_values(self.controller.apply_test_data()); self.SetStatusText("Тестовые данные заполнены.")
    def on_validate(self,event):
        self.controller.update_visible_values(self.form_panel.get_values());result=self.controller.validate();self._show_validation(result)
        if self.controller.display_mode is FormDisplayMode.ERRORS:self._refresh_visible_form()
        self.SetStatusText("Проверка пройдена." if result.is_valid else "Обнаружены ошибки проверки.")
    def _show_validation(self,result):
        self.validation_summary.SetLabel(issue_text(result) if result.is_valid else f"Обнаружено ошибок: {len(result.errors)}, предупреждений: {len(result.warnings)}")
        self.issue_list.DeleteAllItems();self._validation_issues=(*result.errors,*result.warnings)
        for issue in (*result.errors,*result.warnings):
            index=self.issue_list.InsertItem(self.issue_list.GetItemCount(),issue.field_path or "—"); self.issue_list.SetItem(index,1,issue.severity); self.issue_list.SetItem(index,2,f"{issue.code}: {issue.message}")
        visible=bool(result.errors or result.warnings);self.issue_list.Show(visible);self.issue_info.Show(visible);self.issue_info.Disable();self.data_tab.Layout()
    def on_issue_activate(self,event):
        path=self.issue_list.GetItemText(event.GetIndex());self.notebook.SetSelection(0)
        if self.controller.reveal_error_field(path):self._refresh_visible_form(path)
    def on_issue_selected(self,event):
        issue=self._validation_issues[event.GetIndex()];text=f"{issue.field_path or '—'}\n{issue.severity} | {issue.code}\n\n{issue.message}"
        self.issue_list.SetToolTip(text);self.issue_info.SetToolTip(text);self.issue_info.Enable()
    def on_issue_info(self,event):
        index=self.issue_list.GetFirstSelected()
        if index==wx.NOT_FOUND:return
        issue=self._validation_issues[index];dialog=TextInfoDialog(self,"Полный текст сообщения проверки",f"Поле:\n{issue.field_path or '—'}\n\nSeverity: {issue.severity}\nКод: {issue.code}\n\n{issue.message}");dialog.ShowModal();dialog.Destroy()
    def on_generate(self,event):
        self.controller.update_visible_values(self.form_panel.get_values()); result=self.controller.generate_xml(); self.xml_panel.show_generation(result)
        if result.success:self.notebook.SetSelection(1)
        else:
            self.notebook.SetSelection(0)
            if result.errors or result.warnings:self._show_validation(type("Result",(),{"is_valid":False,"errors":result.errors,"warnings":result.warnings})())
            self.validation_summary.SetLabel(self.controller.status_notice if result.status in {"UNRESOLVED_STRUCTURE_VERSION","NORMATIVE_CONFLICT"} else f"Generation status: {result.status}")
        self._sync_buttons(); self.SetStatusText(f"Generation status: {result.status}")
    def on_new_session(self,event):
        session=self.controller.start_session(); self._refresh_session_ui();self.SetStatusText(f"Новая сессия активна | ConversationID: {session.transaction.conversation_id.serialize()}")

    def on_open_session(self,event):
        if not self._confirm_dirty():return
        with wx.FileDialog(self,"Открыть сессию транзакции",defaultDir=str(self.controller.settings.drafts_directory or Path.home()),wildcard="EAEU transaction session (*.eaeusession.json)|*.eaeusession.json",style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal()==wx.ID_CANCEL:return
            path=Path(dialog.GetPath())
        return self._open_session_path(path)

    def _open_session_path(self,path):
        result=self.controller.open_session_snapshot(Path(path))
        self._refresh_session_ui();presentation=self.controller.session_presentation()
        self.SetStatusText(f"Сессия: {presentation.status.value} — {presentation.title}")
        return result

    def on_continue_session(self,event):
        self.controller.continue_session();self._load_processes();self._refresh_session_ui();self.SetStatusText("Восстановленная сессия продолжена без пересоздания correlation history.")

    def on_open_as_new(self,event):
        if not self._confirm_dirty():return
        with wx.FileDialog(self,"Выберите черновик Body для новой транзакции",defaultDir=str(self.controller.settings.drafts_directory or Path.home()),wildcard="EAEU XML draft (*.eaeudraft.json)|*.eaeudraft.json",style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal()==wx.ID_CANCEL:return
            loaded,_=self.controller.open_draft_as_new(Path(dialog.GetPath()))
        self._show_loaded_draft(loaded);self._refresh_session_ui();self.SetStatusText("Черновик Body открыт как новая транзакция с новыми ProcedureID и ConversationID.")

    def _session_filename(self):
        short=lambda value:(value or "unknown").rsplit('.',1)[-1]
        return f"{self.controller.process_code}_{short(self.controller.transaction_code)}.eaeusession.json"

    def on_save_session(self,event):
        if not self.controller.session_save_enabled:return
        with wx.FileDialog(self,"Сохранить сессию транзакции",defaultDir=str(self.controller.settings.drafts_directory or Path.home()),defaultFile=self._session_filename(),wildcard="EAEU transaction session (*.eaeusession.json)|*.eaeusession.json",style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal()==wx.ID_CANCEL:return
            path=self._save_session_path(Path(dialog.GetPath()))
        self.SetStatusText(f"Сессия сохранена: {path.name}")

    def _save_session_path(self,path):return self.controller.save_session(Path(path))

    def on_session_info(self,event):
        presentation=self.controller.session_presentation()
        if presentation:text=f"{presentation.title}\n\n{presentation.description}\n\n"+"\n".join(presentation.details)
        elif self.controller.session:
            snapshot=self.controller.session.create_snapshot();text=(f"Режим: {self.controller.session_mode.value}\nПроцесс: {snapshot.process_code}\nВерсия: {snapshot.process_version}\nТранзакция: {snapshot.transaction_code}\nProcedureID: {snapshot.procedure_id}\nConversationID: {snapshot.conversation_id}\nСостояние: {snapshot.current_state}\nСобытий истории: {len(snapshot.history)}")
        else:text="Активная transaction session отсутствует. Body draft и session snapshot являются разными файлами."
        dialog=TextInfoDialog(self,"Сведения о сессии транзакции",text);dialog.ShowModal();dialog.Destroy()

    def _refresh_session_ui(self):
        presentation=self.controller.session_presentation()
        if presentation:self.session_info.SetLabel(f"{presentation.status.value}: {presentation.title}. {presentation.description}")
        elif self.controller.session:self.session_info.SetLabel(f"Режим: {self.controller.session_mode.value}. Активная transaction session; история событий: {len(self.controller.session.transaction.message_history)}.")
        else:self.session_info.SetLabel("Новая сессия будет создана обычным runtime при формировании первого сообщения.")
        self.buttons["Продолжить сессию"].Enable(self.controller.session_continue_enabled)
        self.buttons["Сохранить сессию"].Enable(self.controller.session_save_enabled);self._save_session_menu.Enable(self.controller.session_save_enabled)
        self.buttons["ⓘ Сведения о сессии"].Enable(bool(presentation or self.controller.session));self._apply_responsive_layout()
    def on_clear(self,event):self.controller.clear();self._refresh_visible_form();self.xml_panel.clear();self._clear_issues();self._sync_buttons()
    def on_copy(self,event):
        xml_text=self.xml_panel.get_xml_text()
        if not xml_text:self.SetStatusText("Сначала сформируйте XML."); return
        try:copied=copy_text_to_clipboard(wx.TheClipboard,xml_text)
        except Exception as error:LOG.debug("Clipboard copy failed: %s",error); copied=False
        if copied:self.SetStatusText("XML скопирован в буфер обмена.")
        else:show_error(self,"Не удалось скопировать XML в буфер обмена.")
    def on_save(self,event):
        if not self.controller.save_enabled:return
        short=lambda value:value.rsplit('.',1)[-1]; filename=f"{self.controller.process_code}_{short(self.controller.transaction_code)}_{short(self.controller.message_code)}_{datetime.now():%Y%m%d_%H%M%S}.xml"
        with wx.FileDialog(self,"Сохранить XML",wildcard="XML files (*.xml)|*.xml",defaultFile=filename,style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal()==wx.ID_CANCEL:return
            self._save_current_xml(Path(dialog.GetPath()))
        self.SetStatusText("XML сохранён.")
    def _save_current_xml(self,path):Path(path).write_text(self.xml_panel.get_xml_text(),encoding="utf-8")
    def on_settings(self,event):
        if not self._confirm_dirty():return
        dialog=SettingsDialog(self,self.controller.settings)
        if dialog.ShowModal()==wx.ID_OK:
            settings=dialog.get_settings();self.controller.apply_settings(settings)
            config=wx.Config("EAEU XML Creator");config.Write("default_timezone",settings.default_timezone);config.Flush();self._load_processes()
        dialog.Destroy()
    def on_process_issues(self,event):
        dialog=ProcessIssuesDialog(self,self.controller); dialog.ShowModal(); dialog.Destroy()
    def on_guide(self,event):
        if not self.controller.process_code:return
        process,message,field=self.controller.guide_context();dialog=GuideDialog(self,self.controller.application,process,message,field);dialog.ShowModal();dialog.Destroy()
    def on_field_guide(self,field_path):
        if not self.controller.process_code or not self.controller.message_code:return
        process,message,field=self.controller.guide_context(field_path);dialog=GuideDialog(self,self.controller.application,process,message,field);dialog.ShowModal();dialog.Destroy()
    def on_hidden_condition_guide(self,event):
        if self._hidden_condition_paths:self.on_field_guide(self._hidden_condition_paths[0])
    def _set_selector_info(self,key,code,name):
        text=f"{code} — {name}" if name else code;self._selector_info[key]=text;self.selector_info_buttons[key].SetToolTip(text)
    def _show_selector_info(self,key):
        titles={"process":"Общий процесс","transaction":"Транзакция","message":"Сообщение"};text=self._selector_info.get(key,"Информация отсутствует.")
        dialog=TextInfoDialog(self,titles[key],text);dialog.ShowModal();dialog.Destroy()
    def _draft_filename(self):
        short=lambda value:(value or "unknown").rsplit('.',1)[-1]
        return f"{self.controller.process_code}_{short(self.controller.transaction_code)}_{short(self.controller.message_code)}.eaeudraft.json"
    def _choose_draft_path(self):
        with wx.FileDialog(self,"Сохранить черновик",defaultDir=str(self.controller.settings.drafts_directory or Path.home()),defaultFile=self._draft_filename(),wildcard="EAEU XML draft (*.eaeudraft.json)|*.eaeudraft.json|JSON (*.json)|*.json",style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            return None if dialog.ShowModal()==wx.ID_CANCEL else Path(dialog.GetPath())
    def on_save_draft(self,event):return self._save_draft(False)
    def on_save_draft_as(self,event):return self._save_draft(True)
    def _save_draft(self,as_new=False):
        self._capture_values(); path=None if not as_new else self._choose_draft_path()
        if as_new and path is None:return False
        if path is None:path=self.controller.current_draft_path or self._choose_draft_path()
        if path is None:return False
        self.controller.save_draft(path); self._update_title(); self.SetStatusText(f"Черновик сохранён: {path.name}"); return True
    def on_open_draft(self,event):
        if not self._confirm_dirty():return
        with wx.FileDialog(self,"Открыть черновик",defaultDir=str(self.controller.settings.drafts_directory or Path.home()),wildcard="EAEU XML draft (*.eaeudraft.json)|*.eaeudraft.json|JSON (*.json)|*.json",style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal()==wx.ID_CANCEL:return
            result=self.controller.load_draft(Path(dialog.GetPath()))
        self._show_loaded_draft(result)
    def _show_loaded_draft(self,result):
        self._load_processes(); self._show_validation(result.validation)
        lines=[f"Черновик загружен. Совместимые поля: {result.compatible_count}; не сопоставлены: {result.unmapped_count}.",*result.warnings]
        self.validation_summary.SetLabel("\n".join(lines)); self.SetStatusText(lines[0]); self._update_title()
    def _capture_values(self):
        if not self._synchronizing_form and self.controller.form:self.controller.update_visible_values(self.form_panel.get_values())
    def on_autosave_timer(self,event):
        self._capture_values(); path=self.controller.autosave_if_due()
        if path:self.SetStatusText("Черновик автоматически сохранён.")
        self._update_title()
    def _update_title(self):self.SetTitle("EAEU XML Creator"+(" — *черновик изменён" if self.controller.dirty else ""))
    def _confirm_dirty(self):
        self._capture_values()
        if not self.controller.requires_dirty_confirmation:return True
        dialog=wx.MessageDialog(self,"В черновике есть несохранённые изменения. Сохранить их?","Несохранённый черновик",wx.YES_NO|wx.CANCEL|wx.CANCEL_DEFAULT|wx.ICON_WARNING)
        answer=dialog.ShowModal(); dialog.Destroy()
        if answer==wx.ID_CANCEL:return False
        if answer==wx.ID_YES:return self._save_draft(False)
        self.controller.discard_autosave(); self.controller.dirty=False; return True
    def _offer_recovery(self):
        if not self.controller.has_autosave_recovery:return
        dialog=wx.MessageDialog(self,"Найден автоматически сохранённый черновик после предыдущего сеанса. Восстановить его?","Восстановление черновика",wx.YES_NO|wx.CANCEL|wx.ICON_QUESTION)
        answer=dialog.ShowModal(); dialog.Destroy()
        if answer==wx.ID_YES:self._show_loaded_draft(self.controller.recover_autosave())
        elif answer==wx.ID_NO:self.controller.discard_autosave()
    def on_close(self,event):
        if not self._confirm_dirty():event.Veto(); return
        self.autosave_timer.Stop(); self.controller.mark_clean_close(); event.Skip()
    def _clear_issues(self):self.validation_summary.SetLabel("");self._validation_issues=();self.issue_list.DeleteAllItems();self.issue_list.Hide();self.issue_info.Hide();self.issue_info.Disable();self.data_tab.Layout()
    def _sync_buttons(self):
        self.buttons["Сформировать XML"].Enable(self.controller.generation_enabled); enabled=self.controller.save_enabled; self.buttons["Сохранить XML"].Enable(enabled); self.buttons["Копировать XML"].Enable(enabled)
        self._refresh_session_ui()
