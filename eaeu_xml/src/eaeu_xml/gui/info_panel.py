"""Read-only presentation of the existing catalog and guide API."""

import wx

from eaeu_xml.gui.components import ActionButton, Card, heading
from eaeu_xml.gui.guide_details import build_guide_node_details
from eaeu_xml.gui.theme import GuiTheme


class InfoPanel(wx.Panel):
    SECTIONS = ("Общие сведения", "Участники", "Структура сообщения",
                "Правила и ограничения", "Связанные сообщения", "Примеры",
                "Техническая информация")

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.section = 0
        self.guide = None
        self.context = None
        self._wrapping = []
        outer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(outer)
        self.menu = wx.Panel(self)
        self.menu.SetBackgroundColour(GuiTheme.colour("background"))
        menu_sizer = wx.BoxSizer(wx.VERTICAL)
        self.menu.SetSizer(menu_sizer)
        self.menu_buttons = []
        for index, title in enumerate(self.SECTIONS):
            button = ActionButton(self.menu, title, lambda event, page=index: self.select_section(page), flat=True)
            button.SetMinSize((190, 36))
            menu_sizer.Add(button, 0, wx.EXPAND | wx.BOTTOM, 4)
            self.menu_buttons.append(button)
        outer.Add(self.menu, 0, wx.EXPAND | wx.RIGHT, 12)
        self.content = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.content.SetScrollRate(0, 12)
        self.content.SetBackgroundColour(GuiTheme.colour("background"))
        self.content.SetSizer(wx.BoxSizer(wx.VERTICAL))
        outer.Add(self.content, 1, wx.EXPAND)
        self.content.Bind(wx.EVT_SIZE, self._on_size)

    def refresh_context(self):
        controller = self.controller
        context = (id(controller.application), controller.process_code, controller.transaction_code, controller.message_code)
        if context != self.context:
            self.context = context
            self.guide = None
        self.select_section(self.section)

    def select_section(self, index):
        self.section = index
        for page, button in enumerate(self.menu_buttons):
            GuiTheme.apply_sidebar_button(button, selected=page == index)
            button.Refresh()
        self.content.Freeze()
        try:
            self._wrapping = []
            self.content.GetSizer().Clear(delete_windows=True)
            controller = self.controller
            message = controller.current_message
            if message is None:
                self._card("Общие сведения", (("Сообщение", "Не выбрано"),))
                return
            process = next((item for item in controller.processes if item.process_code == controller.process_code), None)
            transaction = next((item for item in controller.transactions if item.transaction_code == controller.transaction_code), None)
            if index == 0:
                self._card("Общие сведения", (("Код процесса", process.process_code), ("Наименование", process.name),
                           ("Номер нормативного документа", process.normative_document_number),
                           ("Версия ОП", process.version), ("Статус", process.status)))
                if transaction:
                    self._card("Транзакция", (("Код транзакции", transaction.transaction_code), ("Наименование", transaction.name),
                               ("Процедура", transaction.procedure_code), ("Шаблон взаимодействия", transaction.pattern)))
                self._card("Сообщение", (("Код сообщения", message.message_code), ("Наименование", message.name),
                           ("Направление", message.direction), ("Структура", message.structure_id),
                           ("Статус", message.generation_status)))
                return
            if self.guide is None:
                self.guide = controller.application.get_message_guide(controller.process_code, controller.message_code)
            guide = self.guide
            if index == 1:
                usages = [usage for usage in guide.usages if usage.transaction_code == controller.transaction_code]
                for usage in usages:
                    self._card("Участники транзакции", (("Транзакция", usage.transaction_code),
                               ("Инициатор", usage.initiating_participant), ("Ответчик", usage.responding_participant), ("Роль сообщения", usage.role)))
                if not usages:self._card("Участники", (("Сведения", "Участники не указаны в модели."),))
            elif index == 2:
                self._structure(guide)
            elif index == 3:
                self._card("Правила и ограничения", (("Статус правил", guide.message_rules_status_display),
                           ("Статус генерации", message.generation_status), ("Ограничение", message.blocking_reason)))
                for conflict in guide.conflicts:
                    self._card(conflict.conflict_id, (("Описание", conflict.description), ("Поля", ", ".join(conflict.referenced_fields))))
                for issue in controller.process_issues:
                    if message.message_code in issue.affected_messages:
                        self._card(issue.title, (("Описание", issue.description), ("Действие", issue.suggested_action)))
                for field in self._walk(guide.fields):
                    if field.condition or field.classifier:
                        self._card(field.display_name, (("Путь", field.path), ("Условие", field.condition), ("Классификатор", field.classifier)))
            elif index == 4:
                if transaction:
                    self._card("Сообщения выбранной транзакции", (("Инициирующее", transaction.initiating_message),
                               ("Ответные", ", ".join(transaction.response_messages))))
                for usage in guide.usages:
                    self._card(usage.transaction_code, (("Процедура", usage.procedure_code), ("Роль сообщения", usage.role)))
            elif index == 5:
                self._card("Пример сообщения", (("Статус примера", guide.body_example_status),))
                example = wx.TextCtrl(self.content, value=guide.body_example or "Пример для выбранного сообщения недоступен.",
                                      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
                example.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                example.SetMinSize((-1, 340))
                self.content.GetSizer().Add(example, 1, wx.EXPAND | wx.BOTTOM, 12)
            else:
                self._card("Техническая информация", (("PROCESS", controller.process_code), ("TRN", controller.transaction_code),
                           ("MSG", guide.message_code), ("Структура", guide.structure_id), ("Корневой элемент", guide.root_element),
                           ("Версия структуры", guide.version_description), ("Реквизитов", guide.total_fields),
                           ("Формируется автоматически", guide.automatic), ("Внешние источники", guide.external_system)))
        finally:
            self.content.Thaw()
            self._layout_content()
            self.content.Scroll(0, 0)

    @staticmethod
    def _walk(fields):
        for field in fields:
            yield field
            yield from InfoPanel._walk(field.children)

    def _card(self, title, rows):
        card = Card(self.content)
        outer = wx.BoxSizer(wx.VERTICAL)
        card.SetSizer(outer)
        outer.Add(heading(card, title), 0, wx.EXPAND | wx.ALL, 12)
        grid = wx.FlexGridSizer(cols=2, vgap=8, hgap=16)
        grid.AddGrowableCol(1, 1)
        for key, value in rows:
            label = wx.StaticText(card, label=key)
            label.Wrap(155)
            label.SetMinSize((155, -1))
            GuiTheme.apply_secondary_text(label)
            text = str(value) if value is not None and value != "" else "Не указано"
            control = wx.StaticText(card, label=text)
            control.SetMinSize((60, -1))
            self._wrapping.append((control, text, card))
            grid.Add(label, 0, wx.ALIGN_TOP)
            grid.Add(control, 1, wx.EXPAND)
        outer.Add(grid, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        self.content.GetSizer().Add(card, 0, wx.EXPAND | wx.BOTTOM, 12)

    def _structure(self, guide):
        self._card("Структура сообщения", (("Корневой элемент", guide.root_element), ("Реквизитов", guide.total_fields)))
        tree = wx.TreeCtrl(self.content, style=wx.TR_HAS_BUTTONS | wx.TR_SINGLE | wx.BORDER_NONE)
        root = tree.AddRoot(guide.root_element or guide.structure_id)
        def add(parent, field):
            item = tree.AppendItem(parent, field.display_name)
            tree.SetItemData(item, field)
            for child in field.children:add(item, child)
        for field in guide.fields:add(root, field)
        tree.Expand(root)
        tree.SetMinSize((-1, 240))
        self.content.GetSizer().Add(tree, 0, wx.EXPAND | wx.BOTTOM, 12)
        details = wx.TextCtrl(self.content, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)
        details.SetMinSize((-1, 220))
        self.content.GetSizer().Add(details, 0, wx.EXPAND | wx.BOTTOM, 12)
        def selected(event):
            field = tree.GetItemData(event.GetItem())
            details.SetValue(build_guide_node_details(field) if field else "Выберите реквизит в дереве.")
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, selected)

    def _on_size(self, event):
        event.Skip()
        self._layout_content()

    def _layout_content(self):
        width = max(100, self.content.GetClientSize().width - 215)
        for control, text, card in self._wrapping:
            control.SetLabel(text)
            control.Wrap(width)
            card.Layout()
        self.content.Layout()
        self.content.FitInside()
