import logging
from datetime import datetime
from pathlib import Path
import traceback
from dataclasses import replace

import wx

from eaeu_xml.application import FormDisplayMode
from eaeu_xml.gui.controller import GuiController, GuiSettings
from eaeu_xml.gui.dialogs import DateSelectionDialog, ProcessIssuesDialog, SettingsDialog, TextInfoDialog, TimezoneDialog, issue_text, show_error
from eaeu_xml.gui.form_panel import FormPanel
from eaeu_xml.gui.xml_panel import XmlPanel
from eaeu_xml.gui.guide_dialog import GuideDialog
from eaeu_xml.gui.theme import GuiTheme

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
        super().__init__(None,title="ГИС_xml",size=size); self.SetMinSize((700,560)); self.controller=GuiController(application); self._synchronizing_form=False; self._test_data_loaded=False; self._layout_pending=False
        self.Bind(wx.EVT_SIZE,self._on_frame_size)
        config=wx.Config("EAEU XML Creator");saved_timezone=config.Read("default_timezone","System")
        self.controller.settings=replace(self.controller.settings,default_timezone=saved_timezone)
        self._build_menu(); self.Bind(wx.EVT_CLOSE,self._safe(self.on_close))
        self.CreateStatusBar()
        root = wx.Panel(self)
        root.SetBackgroundColour(GuiTheme.colour("background"))
        outer = wx.BoxSizer(wx.HORIZONTAL)
        root.SetSizer(outer)

        self._build_sidebar(root, outer)
        workspace = wx.Panel(root)
        workspace.SetBackgroundColour(GuiTheme.colour("background"))
        workspace_sizer = wx.BoxSizer(wx.VERTICAL)
        workspace.SetSizer(workspace_sizer)
        outer.Add(workspace, 1, wx.EXPAND)

        self.page_book = wx.Simplebook(workspace)
        workspace_sizer.Add(self.page_book, 1, wx.EXPAND)
        self.home_page = wx.Panel(self.page_book)
        self.creation_page = wx.Panel(self.page_book)
        self.transactions_page = wx.Panel(self.page_book)
        self.drafts_page = wx.Panel(self.page_book)
        self.history_page = wx.Panel(self.page_book)
        self.help_page = wx.Panel(self.page_book)
        self.settings_page = wx.Panel(self.page_book)
        for page, label in (
            (self.home_page, "Главная"),
            (self.creation_page, "Создание XML"),
            (self.transactions_page, "Транзакции"),
            (self.drafts_page, "Черновики"),
            (self.history_page, "История"),
            (self.help_page, "Справка"),
            (self.settings_page, "Настройки"),
        ):
            self.page_book.AddPage(page, label)

        creation_sizer = wx.BoxSizer(wx.VERTICAL)
        self.creation_page.SetSizer(creation_sizer)
        self._build_selection_header(self.creation_page, creation_sizer)
        self._build_tab_bar(self.creation_page, creation_sizer)
        self.notebook = wx.Simplebook(self.creation_page)
        self.data_tab = wx.Panel(self.notebook)
        self.xml_tab = wx.Panel(self.notebook)
        self.validation_tab = wx.Panel(self.notebook)
        self.info_tab = wx.Panel(self.notebook)
        self.notebook.AddPage(self.data_tab, "Заполнение полей")
        self.notebook.AddPage(self.xml_tab, "XML")
        self.notebook.AddPage(self.validation_tab, "Проверка")
        self.notebook.AddPage(self.info_tab, "Информация")
        self.notebook.Bind(wx.EVT_BOOKCTRL_PAGE_CHANGED, self._on_tab_changed)
        creation_sizer.Add(self.notebook, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        self._build_data_tab()
        self._build_xml_tab()
        self._build_validation_tab()
        self._build_info_tab()
        self._build_home_page()
        self._build_transactions_page()
        self._build_drafts_page()
        self._build_history_page()
        self._build_help_page()
        self._build_settings_page()
        self._load_processes()
        self._show_page("Создание XML")
        # No persisted window position exists yet; if one is added, restore it
        # instead of applying this default launch position.
        self.CentreOnScreen()
        self.autosave_timer=wx.Timer(self); self.Bind(wx.EVT_TIMER,self._safe(self.on_autosave_timer),self.autosave_timer); self.autosave_timer.Start(750)
        wx.CallAfter(self._offer_recovery)

    def _build_sidebar(self, root, outer):
        sidebar = wx.Panel(root)
        sidebar.SetMinSize((190, -1))
        sidebar.SetBackgroundColour(GuiTheme.colour("sidebar"))
        sidebar_sizer = wx.BoxSizer(wx.VERTICAL)
        sidebar.SetSizer(sidebar_sizer)
        outer.Add(sidebar, 0, wx.EXPAND | wx.RIGHT, 1)

        brand = wx.StaticText(sidebar, label="ГИС_xml")
        GuiTheme.apply_heading(brand)
        subtitle = wx.StaticText(sidebar, label="ЕАЭС · XML")
        GuiTheme.apply_secondary_text(subtitle)
        sidebar_sizer.Add(brand, 0, wx.ALL, 18)
        sidebar_sizer.Add(subtitle, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 18)

        self.sidebar_buttons = {}
        for label, handler in (
            ("Главная", self._show_home),
            ("Создание XML", self._show_creation),
            ("Транзакции", self._show_transactions),
            ("Черновики", self._show_drafts),
            ("История", self._show_history),
        ):
            button = wx.Button(sidebar, label=label, style=wx.BU_LEFT)
            button.SetMinSize((165, 34))
            button.Bind(wx.EVT_BUTTON, self._safe(handler))
            GuiTheme.apply_sidebar_button(button, selected=label == "Создание XML")
            sidebar_sizer.Add(button, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 4)
            self.sidebar_buttons[label] = button

        sidebar_sizer.AddStretchSpacer()
        for label, handler in (("Справка", self._show_help), ("Настройки", self._show_settings)):
            button = wx.Button(sidebar, label=label, style=wx.BU_LEFT)
            button.Bind(wx.EVT_BUTTON, self._safe(handler))
            GuiTheme.apply_sidebar_button(button)
            sidebar_sizer.Add(button, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 6)
            self.sidebar_buttons[label] = button

    def _build_selection_header(self, parent, outer):
        card = wx.Panel(parent)
        GuiTheme.apply_surface(card)
        card_sizer = wx.BoxSizer(wx.HORIZONTAL)
        card.SetSizer(card_sizer)
        outer.Add(card, 0, wx.EXPAND | wx.ALL, 12)

        self.process_choice = wx.ComboBox(card, style=wx.CB_READONLY)
        self.transaction_choice = wx.ComboBox(card, style=wx.CB_READONLY)
        self.message_choice = wx.ComboBox(card, style=wx.CB_READONLY)
        self.selector_info_buttons = {}
        self._selector_info = {}
        for key, label, choice in (
            ("process", "Общий процесс", self.process_choice),
            ("transaction", "Транзакция", self.transaction_choice),
            ("message", "Сообщение", self.message_choice),
        ):
            section = wx.BoxSizer(wx.VERTICAL)
            label_control = wx.StaticText(card, label=label)
            GuiTheme.apply_secondary_text(label_control)
            section.Add(label_control, 0, wx.BOTTOM, 4)
            row = wx.BoxSizer(wx.HORIZONTAL)
            row.Add(choice, 1, wx.EXPAND)
            info = wx.Button(card, label="ⓘ", size=(34, -1))
            GuiTheme.apply_secondary_button(info)
            info.Bind(wx.EVT_BUTTON, lambda event, item=key: self._show_selector_info(item))
            row.Add(info, 0, wx.LEFT, 4)
            section.Add(row, 0, wx.EXPAND)
            card_sizer.Add(section, 1, wx.EXPAND | wx.ALL, 10)
            self.selector_info_buttons[key] = info

        problems = wx.Button(card, label="Проблемы")
        problems.Bind(wx.EVT_BUTTON, self._safe(self.on_process_issues))
        settings = wx.Button(card, label="Настройки")
        settings.Bind(wx.EVT_BUTTON, self._safe(self._show_settings))
        GuiTheme.apply_secondary_button(problems)
        GuiTheme.apply_secondary_button(settings)
        card_sizer.Add(problems, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        card_sizer.Add(settings, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)

        self.process_choice.Bind(wx.EVT_COMBOBOX, self._safe(self.on_process))
        self.transaction_choice.Bind(wx.EVT_COMBOBOX, self._safe(self.on_transaction))
        self.message_choice.Bind(wx.EVT_COMBOBOX, self._safe(self.on_message))

    def _build_tab_bar(self, parent, outer):
        tab_bar = wx.Panel(parent)
        tab_bar.SetBackgroundColour(GuiTheme.colour("surface"))
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tab_bar.SetSizer(tab_sizer)
        outer.Add(tab_bar, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 12)
        self.tab_buttons = []
        for index, label in enumerate(("Заполнение полей", "XML", "Проверка", "Информация")):
            button = wx.Button(tab_bar, label=label, style=wx.BORDER_NONE)
            button.Bind(wx.EVT_BUTTON, lambda event, page=index: self._select_tab(page))
            tab_sizer.Add(button, 0, wx.ALL, 4)
            self.tab_buttons.append(button)
        self._sync_tab_bar()

    def _select_tab(self, index):
        self.notebook.SetSelection(index)
        self._sync_tab_bar()

    def _sync_tab_bar(self):
        selected = self.notebook.GetSelection() if hasattr(self, "notebook") else 0
        for index, button in enumerate(getattr(self, "tab_buttons", ())):
            if index == selected:
                button.SetBackgroundColour(GuiTheme.colour("accent_soft"))
                button.SetForegroundColour(GuiTheme.colour("accent"))
            else:
                GuiTheme.apply_secondary_button(button)

    def _on_tab_changed(self, event):
        self._sync_tab_bar()
        event.Skip()

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
        GuiTheme.apply_surface(self.data_tab)
        self.status_block=wx.StaticText(self.data_tab)
        GuiTheme.apply_secondary_text(self.status_block)
        outer.Add(self.status_block,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,12)
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
        self.form_area = wx.BoxSizer(wx.HORIZONTAL)
        self.form_panel=FormPanel(self.data_tab,self.on_field_guide,self.on_form_value_changed,self.on_assisted_input)
        self.form_area.Add(self.form_panel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        self.inspector_panel = wx.Panel(self.data_tab)
        GuiTheme.apply_surface(self.inspector_panel)
        self.inspector_panel.SetMinSize((220, -1))
        inspector_sizer = wx.BoxSizer(wx.VERTICAL)
        self.inspector_panel.SetSizer(inspector_sizer)
        inspector_title = wx.StaticText(self.inspector_panel, label="Сведения о поле")
        GuiTheme.apply_heading(inspector_title, level=2)
        self.inspector_toggle = wx.Button(self.inspector_panel, label="Скрыть")
        self.inspector_toggle.Bind(wx.EVT_BUTTON, self._toggle_inspector)
        GuiTheme.apply_secondary_button(self.inspector_toggle)
        inspector_header = wx.BoxSizer(wx.HORIZONTAL)
        inspector_header.Add(inspector_title, 1, wx.ALIGN_CENTER_VERTICAL)
        inspector_header.Add(self.inspector_toggle, 0)
        self.inspector_text = wx.TextCtrl(
            self.inspector_panel,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP,
        )
        self.inspector_text.SetValue("Выберите поле или нажмите ⓘ рядом с реквизитом.")
        inspector_sizer.Add(inspector_header, 0, wx.EXPAND | wx.ALL, 8)
        inspector_sizer.Add(self.inspector_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        self.form_area.Add(self.inspector_panel, 0, wx.EXPAND | wx.RIGHT, 8)
        outer.Add(self.form_area,1,wx.EXPAND)
        self.show_inspector_button = wx.Button(
            self.data_tab,
            label="Показать сведения о поле",
        )
        self.show_inspector_button.Hide()
        self.show_inspector_button.Bind(wx.EVT_BUTTON, self._toggle_inspector)
        GuiTheme.apply_secondary_button(self.show_inspector_button)
        outer.Add(
            self.show_inspector_button,
            0,
            wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            8,
        )
        buttons=wx.WrapSizer(wx.HORIZONTAL)
        for label,handler in (("Открыть черновик",self.on_open_draft),("Сохранить черновик",self.on_save_draft),("Заполнить тестовыми",self.on_test_data),("Проверить",self.on_validate),("Очистить",self.on_clear),("Начать новую транзакцию",self.on_new_session),("Сформировать XML",self.on_generate)):
            button=wx.Button(self.data_tab,label=label); button.Bind(wx.EVT_BUTTON,self._safe(handler)); buttons.Add(button,0,wx.RIGHT,6); self.buttons[label]=button
            if label == "Сформировать XML":
                GuiTheme.apply_primary_button(button)
            elif label == "Проверить":
                GuiTheme.apply_secondary_button(button)
            elif label == "Заполнить тестовыми":
                button.SetForegroundColour(GuiTheme.colour("secondary_text"))
        outer.Add(buttons,0,wx.EXPAND|wx.ALL,8)
        self.form_mode.Bind(wx.EVT_CHOICE,self._safe(self.on_form_mode));self.user_fields_toggle.Bind(wx.EVT_BUTTON,self._safe(self.on_user_fields_toggle))
        self.form_search.Bind(wx.EVT_TEXT,self._safe(self.on_form_search));self.form_search.Bind(wx.EVT_TEXT_ENTER,self._safe(self.on_form_search_now));self._search_later=None
        self._condition_later=None;self._pending_condition_sources=set()

    def _build_xml_tab(self):
        outer=wx.BoxSizer(wx.VERTICAL); self.xml_tab.SetSizer(outer); self.xml_panel=XmlPanel(self.xml_tab); outer.Add(self.xml_panel,1,wx.EXPAND|wx.ALL,6)
        buttons=wx.WrapSizer(wx.HORIZONTAL); copy=wx.Button(self.xml_tab,label="Копировать XML"); save=wx.Button(self.xml_tab,label="Сохранить XML")
        copy.Bind(wx.EVT_BUTTON,self._safe(self.on_copy)); save.Bind(wx.EVT_BUTTON,self._safe(self.on_save)); self.buttons.update({"Копировать XML":copy,"Сохранить XML":save})
        buttons.Add(copy,0,wx.RIGHT,6); buttons.Add(save,0); outer.Add(buttons,0,wx.EXPAND|wx.ALL,8)

    def _toggle_inspector(self, event):
        is_visible = self.inspector_panel.IsShown()
        self.inspector_panel.Show(not is_visible)
        self.show_inspector_button.Show(is_visible)
        self.inspector_toggle.SetLabel("Скрыть")
        self.data_tab.Layout()
        self.form_panel.Layout()
        self.form_panel.FitInside()

    def _build_validation_tab(self):
        outer = wx.BoxSizer(wx.VERTICAL)
        self.validation_tab.SetSizer(outer)
        GuiTheme.apply_surface(self.validation_tab)
        self.validation_summary = wx.StaticText(
            self.validation_tab,
            label="Проверка ещё не выполнялась.",
        )
        outer.Add(self.validation_summary, 0, wx.EXPAND | wx.ALL, 12)
        self.validation_empty = wx.StaticText(
            self.validation_tab,
            label="✓ Проверка пройдена\nОшибок не обнаружено",
        )
        GuiTheme.apply_heading(self.validation_empty)
        self.validation_empty.SetForegroundColour(GuiTheme.colour("success"))
        self.validation_empty.Hide()
        outer.Add(self.validation_empty, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
        self.issue_list = wx.ListCtrl(
            self.validation_tab,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN,
        )
        self.issue_list.InsertColumn(0, "Поле", width=260)
        self.issue_list.InsertColumn(1, "Severity", width=110)
        self.issue_list.InsertColumn(2, "Причина", width=650)
        outer.Add(self.issue_list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 12)
        self.issue_info = wx.Button(self.validation_tab, label="ⓘ Полный текст")
        self.issue_info.Disable()
        outer.Add(self.issue_info, 0, wx.ALIGN_RIGHT | wx.ALL, 12)
        self._validation_issues = ()
        self.issue_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_issue_activate)
        self.issue_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_issue_selected)
        self.issue_info.Bind(wx.EVT_BUTTON, self.on_issue_info)

    def _build_info_tab(self):
        outer = wx.BoxSizer(wx.VERTICAL)
        self.info_tab.SetSizer(outer)
        GuiTheme.apply_surface(self.info_tab)
        title = wx.StaticText(self.info_tab, label="Информация о сообщении")
        GuiTheme.apply_heading(title)
        self.message_info = wx.TextCtrl(
            self.info_tab,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP,
        )
        outer.Add(title, 0, wx.ALL, 12)
        outer.Add(self.message_info, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

    def _build_home_page(self):
        outer = wx.BoxSizer(wx.VERTICAL)
        self.home_page.SetSizer(outer)
        title = wx.StaticText(self.home_page, label="ГИС_xml")
        GuiTheme.apply_heading(title)
        description = wx.StaticText(
            self.home_page,
            label=(
                "Рабочее место для выбора общего процесса, заполнения сообщения "
                "и формирования XML."
            ),
        )
        GuiTheme.apply_secondary_text(description)
        open_creation = wx.Button(self.home_page, label="Создание XML")
        open_creation.Bind(wx.EVT_BUTTON, self._safe(self._show_creation))
        GuiTheme.apply_primary_button(open_creation)
        outer.AddStretchSpacer()
        outer.Add(title, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 16)
        outer.Add(description, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
        outer.Add(open_creation, 0, wx.LEFT | wx.RIGHT, 16)
        outer.AddStretchSpacer(2)

    def _build_transactions_page(self):
        outer = wx.BoxSizer(wx.VERTICAL)
        self.transactions_page.SetSizer(outer)
        title = wx.StaticText(self.transactions_page, label="Транзакции")
        GuiTheme.apply_heading(title)
        self.transactions_process = wx.Choice(self.transactions_page)
        self.transactions_list = wx.ListBox(self.transactions_page)
        self.transactions_details = wx.TextCtrl(
            self.transactions_page,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP,
        )
        self.transactions_process.Bind(wx.EVT_CHOICE, self._safe(self.on_transactions_process))
        self.transactions_list.Bind(wx.EVT_LISTBOX, self._safe(self.on_transactions_list))
        outer.Add(title, 0, wx.ALL, 12)
        outer.Add(self.transactions_process, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        split = wx.BoxSizer(wx.HORIZONTAL)
        split.Add(self.transactions_list, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM, 12)
        split.Add(self.transactions_details, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        outer.Add(split, 1, wx.EXPAND)

    def _build_drafts_page(self):
        outer = wx.BoxSizer(wx.VERTICAL)
        self.drafts_page.SetSizer(outer)
        title = wx.StaticText(self.drafts_page, label="Черновики")
        GuiTheme.apply_heading(title)
        self.drafts_summary = wx.StaticText(self.drafts_page)
        self.drafts_summary.Wrap(700)
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        open_button = wx.Button(self.drafts_page, label="Открыть черновик")
        save_button = wx.Button(self.drafts_page, label="Сохранить текущий черновик")
        open_button.Bind(wx.EVT_BUTTON, self._safe(self.on_open_draft))
        save_button.Bind(wx.EVT_BUTTON, self._safe(self.on_save_draft))
        buttons.Add(open_button, 0, wx.RIGHT, 8)
        buttons.Add(save_button, 0)
        outer.Add(title, 0, wx.ALL, 12)
        outer.Add(self.drafts_summary, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        outer.Add(buttons, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        outer.AddStretchSpacer()

    def _build_history_page(self):
        outer = wx.BoxSizer(wx.VERTICAL)
        self.history_page.SetSizer(outer)
        title = wx.StaticText(self.history_page, label="История")
        GuiTheme.apply_heading(title)
        self.history_text = wx.TextCtrl(
            self.history_page,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP,
        )
        outer.Add(title, 0, wx.ALL, 12)
        outer.Add(self.history_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

    def _build_help_page(self):
        outer = wx.BoxSizer(wx.HORIZONTAL)
        self.help_page.SetSizer(outer)
        self.help_sections = wx.ListBox(
            self.help_page,
            choices=["Общий процесс", "Транзакция", "Сообщение", "Поля"],
        )
        self.help_text = wx.TextCtrl(
            self.help_page,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP,
        )
        self.help_sections.Bind(wx.EVT_LISTBOX, self._safe(self.on_help_section))
        self.help_sections.SetSelection(0)
        outer.Add(self.help_sections, 0, wx.EXPAND | wx.ALL, 12)
        outer.Add(self.help_text, 1, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, 12)

    def _build_settings_page(self):
        outer = wx.BoxSizer(wx.VERTICAL)
        self.settings_page.SetSizer(outer)
        title = wx.StaticText(self.settings_page, label="Настройки")
        GuiTheme.apply_heading(title)
        grid = wx.FlexGridSizer(7, 2, 10, 8)
        grid.AddGrowableCol(1, 1)
        self.settings_root = wx.TextCtrl(self.settings_page)
        self.settings_mode = wx.Choice(self.settings_page, choices=["TEST", "STRICT"])
        self.settings_seed = wx.SpinCtrl(self.settings_page, min=0, max=2147483647)
        self.settings_autosave = wx.CheckBox(self.settings_page, label="Включено")
        self.settings_delay = wx.SpinCtrl(self.settings_page, min=2, max=30)
        self.settings_drafts = wx.TextCtrl(self.settings_page)
        self.settings_timezone = wx.TextCtrl(self.settings_page)
        for label, control in (
            ("Корень общих процессов", self.settings_root),
            ("Режим", self.settings_mode),
            ("Seed", self.settings_seed),
            ("Автосохранение", self.settings_autosave),
            ("Задержка, секунд", self.settings_delay),
            ("Папка черновиков", self.settings_drafts),
            ("Часовой пояс по умолчанию", self.settings_timezone),
        ):
            grid.Add(wx.StaticText(self.settings_page, label=label), 0, wx.ALIGN_CENTER_VERTICAL)
            grid.Add(control, 1, wx.EXPAND)
        apply_button = wx.Button(self.settings_page, label="Применить настройки")
        apply_button.Bind(wx.EVT_BUTTON, self._safe(self.on_apply_settings))
        GuiTheme.apply_primary_button(apply_button)
        outer.Add(title, 0, wx.ALL, 12)
        outer.Add(grid, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        outer.Add(apply_button, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        outer.AddStretchSpacer()

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

    def _show_page(self, label):
        index = next(
            index
            for index in range(self.page_book.GetPageCount())
            if self.page_book.GetPageText(index) == label
        )
        self.page_book.SetSelection(index)
        for name, button in self.sidebar_buttons.items():
            GuiTheme.apply_sidebar_button(button, selected=name == label)

    def _show_home(self, event):
        self._show_page("Главная")

    def _show_creation(self, event):
        self._show_page("Создание XML")
        self.notebook.SetSelection(0)

    def _show_transactions(self, event):
        self._refresh_transactions_page()
        self._show_page("Транзакции")

    def _show_drafts(self, event):
        self._refresh_drafts_page()
        self._show_page("Черновики")

    def _show_history(self, event):
        self._refresh_history_page()
        self._show_page("История")

    def _show_help(self, event):
        self._refresh_help_page()
        self._show_page("Справка")

    def _show_settings(self, event):
        self._refresh_settings_page()
        self._show_page("Настройки")

    def _refresh_transactions_page(self):
        labels = [
            self.controller.short_text(
                item.process_code,
                item.name,
                normative_document_number=item.normative_document_number,
            )
            for item in self.controller.processes
        ]
        self.transactions_process.Set(labels)
        index = next(
            (
                index
                for index, item in enumerate(self.controller.processes)
                if item.process_code == self.controller.process_code
            ),
            wx.NOT_FOUND,
        )
        self.transactions_process.SetSelection(index)
        self.transactions_list.Set(
            [self.controller.short_text(item.transaction_code, item.name) for item in self.controller.transactions]
        )
        selected = next(
            (
                index
                for index, item in enumerate(self.controller.transactions)
                if item.transaction_code == self.controller.transaction_code
            ),
            wx.NOT_FOUND,
        )
        self.transactions_list.SetSelection(selected)
        self._show_selected_transaction()

    def on_transactions_process(self, event):
        if not self._confirm_dirty():
            self._refresh_transactions_page()
            return
        process = self.controller.processes[self.transactions_process.GetSelection()]
        self.controller.select_process(process.process_code)
        self._load_processes()
        self._refresh_transactions_page()

    def on_transactions_list(self, event):
        transaction = self.controller.transactions[self.transactions_list.GetSelection()]
        self.controller.select_transaction(transaction.transaction_code)
        self._refresh_transactions()
        self._show_selected_transaction()

    def _show_selected_transaction(self):
        if not self.controller.transaction_code:
            self.transactions_details.SetValue("Транзакция не выбрана.")
            return
        transaction = next(
            (
                item
                for item in self.controller.transactions
                if item.transaction_code == self.controller.transaction_code
            ),
            None,
        )
        if transaction is None:
            self.transactions_details.SetValue("Транзакция не найдена.")
            return
        sequence = "\n".join(
            f"{message.direction or 'Сообщение'}  →  {message.message_code}\n{message.name or ''}"
            for message in self.controller.messages
        )
        self.transactions_details.SetValue(
            f"Транзакция\n{transaction.transaction_code}\n{transaction.name or ''}\n\n"
            f"Процедура: {transaction.procedure_code or 'не указана'}\n"
            f"Pattern: {transaction.pattern or 'не указан'}\n"
            f"Инициирующее сообщение: {transaction.initiating_message or 'не указано'}\n"
            f"Ответные сообщения: {', '.join(transaction.response_messages) or 'не указаны'}\n\n"
            f"Последовательность сообщений\n{sequence or 'Сообщения отсутствуют.'}"
        )

    def _refresh_drafts_page(self):
        current = self.controller.current_draft_path
        drafts_root = self.controller.settings.drafts_directory
        self.drafts_summary.SetLabel(
            "Текущий черновик: "
            f"{current if current else 'не открыт'}\n\n"
            f"Папка черновиков: {drafts_root or 'не задана'}\n"
            "Открытие и сохранение используют стандартный диалог выбора файлов."
        )
        self.drafts_page.Layout()

    def _refresh_history_page(self):
        if not self.controller.session:
            self.history_text.SetValue(
                "История будет доступна после создания или восстановления сессии транзакции."
            )
            return
        snapshot = self.controller.session.create_snapshot()
        lines = [
            f"{item.sequence_number}. {item.message_kind}: {item.message_id}"
            for item in snapshot.history
        ]
        self.history_text.SetValue("История текущей сессии\n\n" + "\n".join(lines))

    def _refresh_help_page(self):
        self._show_help_section(self.help_sections.GetSelection())

    def on_help_section(self, event):
        self._show_help_section(self.help_sections.GetSelection())

    def _show_help_section(self, index):
        message = self.controller.current_message
        if index == 0:
            process = next(
                (item for item in self.controller.processes if item.process_code == self.controller.process_code),
                None,
            )
            text = f"{process.process_code if process else '—'}\n\n{process.name if process else 'Процесс не выбран.'}"
        elif index == 1:
            text = self.transactions_details.GetValue() or "Транзакция не выбрана."
        elif index == 2:
            text = self.message_info.GetValue() if message else "Сообщение не выбрано."
        else:
            text = (
                "Выберите поле на вкладке «Заполнение полей» или нажмите ⓘ рядом с реквизитом.\n\n"
                "Подробная карточка реквизита откроется во встроенном инспекторе."
            )
        self.help_text.SetValue(text)

    def _refresh_settings_page(self):
        settings = self.controller.settings
        self.settings_root.SetValue(str(settings.processes_root))
        self.settings_mode.SetStringSelection(settings.mode)
        self.settings_seed.SetValue(settings.seed)
        self.settings_autosave.SetValue(settings.autosave_enabled)
        self.settings_delay.SetValue(settings.autosave_delay_seconds)
        self.settings_drafts.SetValue(str(settings.drafts_directory or ""))
        self.settings_timezone.SetValue(settings.default_timezone)

    def on_apply_settings(self, event):
        settings = GuiSettings(
            Path(self.settings_root.GetValue()),
            self.settings_mode.GetStringSelection(),
            self.settings_seed.GetValue(),
            self.settings_autosave.GetValue(),
            self.settings_delay.GetValue(),
            Path(self.settings_drafts.GetValue()) if self.settings_drafts.GetValue() else None,
            self.settings_timezone.GetValue().strip() or "System",
        )
        self.controller.apply_settings(settings)
        config = wx.Config("EAEU XML Creator")
        config.Write("default_timezone", settings.default_timezone)
        config.Flush()
        self._load_processes()
        self.SetStatusText("Настройки применены.")

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
        self._test_data_loaded = False
        self.status_block.SetLabel(f"Структура: {m.structure_id}    Версия: {m.active_version or 'не задана'}    Статус: {m.generation_status}    Режим: {self.controller.settings.mode}")
        self.form_search.ChangeValue(self.controller.search_query);self._sync_form_mode();self._refresh_visible_form()
        self.xml_panel.set_filename(m.message_code)
        self.xml_panel.clear(); self._clear_issues(); self._refresh_message_info(); self._sync_buttons(); self.notebook.SetSelection(0); self._update_title()
        self.SetStatusText(f"Process: {self.controller.process_code} | TRN: {self.controller.transaction_code} | Status: {m.generation_status}")

    def _refresh_message_info(self):
        message = self.controller.current_message
        if not message:
            self.message_info.SetValue("Сообщение не выбрано.")
            return
        text = (
            f"Код сообщения\n{message.message_code}\n\n"
            f"Название\n{message.name or 'не указано'}\n\n"
            f"Структура\n{message.structure_id or 'не указана'}\n\n"
            f"Версия\n{message.active_version or 'не задана'}\n\n"
            f"Статус\n{message.generation_status}\n\n"
            f"Транзакция\n{self.controller.transaction_code or 'не указана'}\n\n"
            "Встроенные структуры и нормативные источники\n"
            "Откройте «Справка» для подробной карточки сообщения и реквизитов."
        )
        self.message_info.SetValue(text)

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
        if self._synchronizing_form:
            return
        self._test_data_loaded = False
        if path not in self.controller.condition_dependency_index:
            return
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
    def on_test_data(self, event):
        values = self.controller.apply_test_data()
        self._synchronizing_form = True
        try:
            self.form_panel.set_values(values)
        finally:
            self._synchronizing_form = False
        self._test_data_loaded = True
        self.SetStatusText("Тестовые данные заполнены.")
    def on_validate(self,event):
        if not self._test_data_loaded:
            self.controller.update_visible_values(self.form_panel.get_values())
        result=self.controller.validate();self._show_validation(result)
        if self.controller.display_mode is FormDisplayMode.ERRORS:self._refresh_visible_form()
        self.SetStatusText("Проверка пройдена." if result.is_valid else "Обнаружены ошибки проверки.")
    def _show_validation(self,result):
        self.validation_summary.SetLabel(issue_text(result) if result.is_valid else f"Обнаружено ошибок: {len(result.errors)}, предупреждений: {len(result.warnings)}")
        self.issue_list.DeleteAllItems();self._validation_issues=(*result.errors,*result.warnings)
        for issue in (*result.errors,*result.warnings):
            index=self.issue_list.InsertItem(self.issue_list.GetItemCount(),issue.field_path or "—"); self.issue_list.SetItem(index,1,issue.severity); self.issue_list.SetItem(index,2,f"{issue.code}: {issue.message}")
        visible=bool(result.errors or result.warnings);self.issue_list.Show(visible);self.issue_info.Show(visible);self.issue_info.Disable();self.validation_tab.Layout()
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
        if not self._test_data_loaded:
            self.controller.update_visible_values(self.form_panel.get_values())
        result=self.controller.generate_xml(); self.xml_panel.show_generation(result)
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
        with wx.FileDialog(self,"Выберите черновик Body для новой транзакции",defaultDir=str(self.controller.settings.drafts_directory or Path.home()),wildcard="ГИС_xml draft (*.eaeudraft.json)|*.eaeudraft.json",style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal()==wx.ID_CANCEL:return
            loaded,_=self.controller.open_draft_as_new(Path(dialog.GetPath()))
        self._show_loaded_draft(loaded);self._refresh_session_ui();self.SetStatusText("Черновик Body открыт как новая транзакция с новыми ProcedureID и ConversationID.")

    def _session_filename(self):
        short=lambda value:(value or "unknown").rsplit('.',1)[-1]
        # macOS FileDialog appends the wildcard's final ".json" extension.
        # Supplying the logical stem here produces SESSION_SUFFIX exactly once.
        return f"{self.controller.process_code}_{short(self.controller.transaction_code)}.eaeusession"

    def on_save_session(self,event):
        if not self.controller.session_save_enabled:return
        with wx.FileDialog(self,"Сохранить сессию транзакции",defaultDir=str(self.controller.settings.drafts_directory or Path.home()),defaultFile=self._session_filename(),wildcard="EAEU transaction session (*.eaeusession.json)|*.eaeusession.json",style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal()==wx.ID_CANCEL:return
            path=self._save_session_path(Path(dialog.GetPath()))
        self.SetStatusText(f"Сессия сохранена: {path.name}")

    def _save_session_path(self, path):
        return self.controller.save_session(Path(path))

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
    def on_clear(self, event):
        self.controller.clear()
        self._refresh_visible_form()
        self.xml_panel.clear()
        self._clear_issues()
        self._sync_buttons()
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
    def _save_current_xml(self, path):
        xml_text = self.xml_panel.get_xml_text()
        Path(path).write_text(xml_text, encoding="utf-8")
    def on_settings(self,event):
        if not self._confirm_dirty():
            return
        self._show_settings(event)
    def on_process_issues(self,event):
        dialog=ProcessIssuesDialog(self,self.controller); dialog.ShowModal(); dialog.Destroy()
    def on_guide(self,event):
        self._show_help(event)
    def on_field_guide(self,field_path):
        if not self.controller.process_code or not self.controller.message_code:return
        field = self.controller.find_field(field_path)
        if field:
            self.inspector_text.SetValue(self.controller.field_help(field))
        if not self.inspector_panel.IsShown():
            self._toggle_inspector(None)
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
        with wx.FileDialog(self,"Сохранить черновик",defaultDir=str(self.controller.settings.drafts_directory or Path.home()),defaultFile=self._draft_filename(),wildcard="ГИС_xml draft (*.eaeudraft.json)|*.eaeudraft.json|JSON (*.json)|*.json",style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dialog:
            return None if dialog.ShowModal()==wx.ID_CANCEL else Path(dialog.GetPath())
    def on_save_draft(self, event):
        return self._save_draft(False)

    def on_save_draft_as(self, event):
        return self._save_draft(True)
    def _save_draft(self,as_new=False):
        self._capture_values(); path=None if not as_new else self._choose_draft_path()
        if as_new and path is None:return False
        if path is None:path=self.controller.current_draft_path or self._choose_draft_path()
        if path is None:return False
        self.controller.save_draft(path); self._update_title(); self.SetStatusText(f"Черновик сохранён: {path.name}"); return True
    def on_open_draft(self,event):
        if not self._confirm_dirty():return
        with wx.FileDialog(self,"Открыть черновик",defaultDir=str(self.controller.settings.drafts_directory or Path.home()),wildcard="ГИС_xml draft (*.eaeudraft.json)|*.eaeudraft.json|JSON (*.json)|*.json",style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal()==wx.ID_CANCEL:return
            result=self.controller.load_draft(Path(dialog.GetPath()))
        self._show_loaded_draft(result)
    def _show_loaded_draft(self,result):
        self._load_processes(); self._show_validation(result.validation)
        lines=[f"Черновик загружен. Совместимые поля: {result.compatible_count}; не сопоставлены: {result.unmapped_count}.",*result.warnings]
        self.validation_summary.SetLabel("\n".join(lines)); self.SetStatusText(lines[0]); self._update_title()
    def _capture_values(self):
        if not self._synchronizing_form and not self._test_data_loaded and self.controller.form:self.controller.update_visible_values(self.form_panel.get_values())
    def on_autosave_timer(self,event):
        self._capture_values(); path=self.controller.autosave_if_due()
        if path:self.SetStatusText("Черновик автоматически сохранён.")
        self._update_title()
    def _update_title(self):
        dirty_marker = " — *черновик изменён" if self.controller.dirty else ""
        self.SetTitle("ГИС_xml" + dirty_marker)
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
    def _clear_issues(self):
        self.validation_summary.SetLabel("")
        self._validation_issues = ()
        self.issue_list.DeleteAllItems()
        self.issue_list.Hide()
        self.issue_info.Hide()
        self.issue_info.Disable()
        self.data_tab.Layout()
    def _sync_buttons(self):
        self.buttons["Сформировать XML"].Enable(self.controller.generation_enabled); enabled=self.controller.save_enabled; self.buttons["Сохранить XML"].Enable(enabled); self.buttons["Копировать XML"].Enable(enabled)
        self._refresh_session_ui()
