import wx

from eaeu_xml.gui.guide_details import GuideNodeKey, build_guide_node_details, resolve_guide_node


class GuideDialog(wx.Dialog):
    """Structured guide reader; it never renders the generated Markdown file."""

    def __init__(self, parent, application, process_code, message_code=None, field_path=None):
        super().__init__(parent, title="Сводка по общему процессу", size=(1180, 780),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.application = application; self.process_code = process_code
        self.process_guide = application.get_process_guide(process_code); self.message_guides = self.process_guide.messages
        self.current_message = None; self._tree_fields = {}
        outer = wx.BoxSizer(wx.VERTICAL); self.SetSizer(outer)
        splitter = wx.SplitterWindow(self); left = wx.Panel(splitter); right = wx.Panel(splitter)
        splitter.SplitVertically(left, right, 310); splitter.SetMinimumPaneSize(240); outer.Add(splitter, 1, wx.EXPAND | wx.ALL, 8)
        ls = wx.BoxSizer(wx.VERTICAL); left.SetSizer(ls)
        heading = wx.StaticText(left, label=f"{self.process_guide.process_code}\n{self.process_guide.name}"); font=heading.GetFont();font.MakeBold();heading.SetFont(font)
        ls.Add(heading,0,wx.EXPAND|wx.ALL,6); self.search=wx.SearchCtrl(left,style=wx.TE_PROCESS_ENTER);self.search.ShowCancelButton(True);ls.Add(self.search,0,wx.EXPAND|wx.ALL,6)
        self.field_filter=wx.Choice(left,choices=["Все реквизиты","Только пользовательские","Только обязательные","Только unresolved"]);self.field_filter.SetSelection(0);ls.Add(self.field_filter,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,6)
        self.messages=wx.ListBox(left);ls.Add(self.messages,1,wx.EXPAND|wx.ALL,6)
        rs=wx.BoxSizer(wx.VERTICAL);right.SetSizer(rs);self.title=wx.StaticText(right);font=self.title.GetFont();font.MakeBold();font.SetPointSize(font.GetPointSize()+2);self.title.SetFont(font);rs.Add(self.title,0,wx.EXPAND|wx.ALL,8)
        self.summary=wx.TextCtrl(right,style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP);self.summary.SetMinSize((-1,190));rs.Add(self.summary,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8)
        self.tree=wx.TreeCtrl(right,style=wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT|wx.TR_SINGLE);rs.Add(self.tree,1,wx.EXPAND|wx.LEFT|wx.RIGHT,8)
        self.details=wx.TextCtrl(right,style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP);self.details.SetMinSize((-1,210));rs.Add(self.details,0,wx.EXPAND|wx.ALL,8)
        outer.Add(self.CreateButtonSizer(wx.CLOSE),0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8)
        self.search.Bind(wx.EVT_TEXT,self.on_search);self.search.Bind(wx.EVT_TEXT_ENTER,self.on_search);self.field_filter.Bind(wx.EVT_CHOICE,self.on_filter);self.messages.Bind(wx.EVT_LISTBOX,self.on_message);self.tree.Bind(wx.EVT_TREE_SEL_CHANGED,self.on_field)
        self._set_message_list(self.message_guides)
        self.open_context(message_code or self.message_guides[0].message_code, field_path)

    def _set_message_list(self, guides):
        self.message_guides=tuple(guides);self.messages.Set([f"{item.message_code} — {item.name}" for item in self.message_guides])

    def open_context(self,message_code,field_path=None):
        guide=self.application.get_message_guide(self.process_code,message_code);self.current_message=guide
        index=next((i for i,item in enumerate(self.message_guides) if item.message_code==message_code),wx.NOT_FOUND)
        if index!=wx.NOT_FOUND:self.messages.SetSelection(index)
        self._show_message(guide,field_path)

    def _show_message(self,guide,field_path=None):
        self.title.SetLabel(f"{guide.message_code} — {guide.name}")
        usages="\n".join(f"{u.transaction_code} / {u.procedure_code}: {u.role}" for u in guide.usages)
        conflicts="\n".join(f"В нормативном источнике обнаружено внутреннее несоответствие: {c.conflict_id}. {c.description}" for c in guide.conflicts)
        self.summary.SetValue("\n".join(filter(None,(guide.purpose,f"Структура: {guide.structure_id}",f"Версия: {guide.version_description}",f"Правила сообщения: {guide.message_rules_status_display}",f"Корневой элемент: {guide.root_element}",usages,
            f"Всего реквизитов: {guide.total_fields}; пользователь заполняет: {guide.user_input}; выбирает: {guide.user_select}; автоматически: {guide.automatic}; классификаторы: {guide.classifier_fields}; условные: {guide.conditional}; внешние источники: {guide.external_system}; не определено: {guide.unresolved}",conflicts))))
        self.tree.DeleteAllItems();self._tree_fields={};self.show_guide_node_details(None);root=self.tree.AddRoot(guide.root_element or guide.structure_id)
        context_field=None;context_item=None
        def add(parent,field):
            nonlocal context_field,context_item
            label=("@" if field.xml_kind=="XML-атрибут" else "")+field.display_name
            item=self.tree.AppendItem(parent,label);key=GuideNodeKey(guide.message_code,field.path);self.tree.SetItemData(item,key);self._tree_fields[key]=field
            for child in field.children:add(item,child)
            if field.path==field_path:context_field=field;context_item=item
        fields=self._filtered_fields(guide.fields,self.search.GetValue().strip())
        for field in fields:add(root,field)
        self.tree.Expand(root)
        if not fields:self.show_guide_node_details(None,"В выбранном режиме реквизиты не найдены.")
        elif context_field is not None:
            parent=self.tree.GetItemParent(context_item)
            while parent.IsOk():self.tree.Expand(parent);parent=self.tree.GetItemParent(parent)
            self.tree.SelectItem(context_item);self.tree.EnsureVisible(context_item);self.show_guide_node_details(context_field)

    def _filtered_fields(self,fields,query=""):
        mode=self.field_filter.GetSelection();needle=query.casefold()
        def direct(field):
            policy_ok=(mode==0 or (mode==1 and field.ui_input_policy in {"USER_INPUT","USER_SELECT","EXTERNAL_SYSTEM","CONDITIONAL","UNRESOLVED_UI_POLICY"}) or
                       (mode==2 and field.requirement=="Обязательно") or (mode==3 and field.ui_input_policy=="UNRESOLVED_UI_POLICY"))
            haystack=" ".join(filter(None,(field.display_name,field.xml_name,field.path,field.description,field.what_to_enter)))
            return policy_ok and (not needle or needle in haystack.casefold())
        def visit(field):
            children=tuple(item for child in field.children if (item:=visit(child)) is not None)
            if direct(field) or children:return type(field)(**{**field.__dict__,"children":children})
            return None
        return tuple(item for field in fields if (item:=visit(field)) is not None)

    def on_search(self,event):
        query=self.search.GetValue().strip()
        if not query:
            self._set_message_list(self.process_guide.messages)
            if self.current_message:self._show_message(self.current_message)
            return
        hits=self.application.search_guide(self.process_code,query);codes=[]
        for hit in hits:
            if hit.message_code not in codes:codes.append(hit.message_code)
        guides=[next(item for item in self.process_guide.messages if item.message_code==code) for code in codes]
        self._set_message_list(guides)
        if hits:
            self.open_context(hits[0].message_code,hits[0].field_path)
        elif self.current_message:self._show_message(self.current_message)

    def on_filter(self,event):
        if self.current_message:self._show_message(self.current_message)

    def on_message(self,event):
        if self.messages.GetSelection()!=wx.NOT_FOUND:self.open_context(self.message_guides[self.messages.GetSelection()].message_code)

    def on_field(self,event):
        item=event.GetItem()
        if not item.IsOk():self.show_guide_node_details(None);return
        field=resolve_guide_node(self.tree.GetItemData(item),self._tree_fields)
        self.show_guide_node_details(field)

    def show_guide_node_details(self,field,message="Выберите реквизит в дереве для просмотра подробной информации."):
        self.details.SetValue(build_guide_node_details(field) if field is not None else message)
        self.details.SetInsertionPoint(0);self.details.ShowPosition(0);self.details.Layout();self.details.Refresh();self.Layout();self.Refresh()
