"""Isolated QPlainTextEdit prototype for large XML documents.

The widget owns presentation concerns only.  Domain work remains in the
existing Qt ViewModel and application services.
"""

from __future__ import annotations

from PySide6.QtCore import QObject, Property, Qt, QTimer, Signal, Slot
from PySide6.QtGui import (
    QColor,
    QFont,
    QKeySequence,
    QShortcut,
    QTextCharFormat,
    QTextCursor,
    QTextFormat,
)
from PySide6.QtWidgets import QPlainTextEdit, QTextEdit

from .fonts import fixed_font_family
from .xml_display_document import (
    CompactSyncError,
    HiddenTextNode,
    ProtectedMarker,
    XmlDisplayDocument,
)


HIDDEN_NODE_ID_PROPERTY = QTextFormat.Property.UserProperty.value + 101


class NativeXmlEditor(QPlainTextEdit):
    """Large plain-text XML editor with local/debounced edit state."""

    commitRequested = Signal(str)
    fontSizeChanged = Signal(int)
    protectedEditRejected = Signal(str)

    DEFAULT_FONT_SIZE = 14
    MIN_FONT_SIZE = 9
    MAX_FONT_SIZE = 32

    def __init__(
        self,
        parent=None,
        *,
        debounce_ms: int = 300,
        font_family: str | None = None,
    ) -> None:
        super().__init__(parent)
        self._font_size = self.DEFAULT_FONT_SIZE
        self._programmatic_change = False
        self._commit_failed = False
        self._cursor_guard_active = False
        self._last_cursor_position = 0

        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setUndoRedoEnabled(True)
        font = QFont(font_family or fixed_font_family())
        font.setFixedPitch(True)
        font.setPixelSize(self._font_size)
        self.setFont(font)

        self._sync_timer = QTimer(self)
        self._sync_timer.setSingleShot(True)
        self._sync_timer.setInterval(debounce_ms)
        self._sync_timer.timeout.connect(self.flush)

        self._diagnostic_timer = QTimer(self)
        self._diagnostic_timer.setSingleShot(True)
        self._diagnostic_timer.setInterval(1800)
        self._diagnostic_timer.timeout.connect(self.clear_diagnostic_highlight)

        # Signal-to-Qt-slot connection keeps per-character debounce work in C++.
        # Python is entered only when the debounce expires or an action flushes.
        self.textChanged.connect(self._sync_timer.start)
        self.cursorPositionChanged.connect(self._guard_cursor_position)

        self._shortcuts = []
        for sequence, callback in (
            (QKeySequence(QKeySequence.StandardKey.ZoomIn), lambda: self.zoom_by(1)),
            (QKeySequence(QKeySequence.StandardKey.ZoomOut), lambda: self.zoom_by(-1)),
            (QKeySequence("Ctrl+0"), self.reset_zoom),
            (QKeySequence("Meta+0"), self.reset_zoom),
        ):
            shortcut = QShortcut(sequence, self)
            shortcut.activated.connect(callback)
            self._shortcuts.append(shortcut)

    @property
    def dirty(self) -> bool:
        return self.document().isModified()

    @property
    def font_size(self) -> int:
        return self._font_size

    def xml(self) -> str:
        return self.toPlainText()

    @staticmethod
    def _python_to_qt_position(text: str, position: int) -> int:
        position = max(0, min(int(position), len(text)))
        return len(text[:position].encode("utf-16-le")) // 2

    @staticmethod
    def _qt_to_python_position(text: str, position: int) -> int:
        target = max(0, int(position))
        units = 0
        for index, char in enumerate(text):
            if units >= target:
                return index
            units += 2 if ord(char) > 0xFFFF else 1
            if units > target:
                return index
        return len(text)

    def _protected_ranges_qt(self) -> tuple[tuple[str, int, int], ...]:
        ranges: list[tuple[str, int, int]] = []
        block = self.document().begin()
        while block.isValid():
            iterator = block.begin()
            while not iterator.atEnd():
                fragment = iterator.fragment()
                if fragment.isValid():
                    node_id = fragment.charFormat().property(HIDDEN_NODE_ID_PROPERTY)
                    if node_id:
                        start = fragment.position()
                        end = start + fragment.length()
                        node_id = str(node_id)
                        if ranges and ranges[-1][0] == node_id and ranges[-1][2] == start:
                            previous = ranges[-1]
                            ranges[-1] = (node_id, previous[1], end)
                        else:
                            ranges.append((node_id, start, end))
                iterator += 1
            block = block.next()
        return tuple(ranges)

    def protected_marker_ranges(self) -> tuple[ProtectedMarker, ...]:
        """Return protected marker ranges as Python-string character offsets."""

        text = self.toPlainText()
        return tuple(
            ProtectedMarker(
                node_id,
                self._qt_to_python_position(text, start),
                self._qt_to_python_position(text, end),
            )
            for node_id, start, end in self._protected_ranges_qt()
        )

    def _hidden_format(self, node_id: str) -> QTextCharFormat:
        char_format = QTextCharFormat()
        char_format.setProperty(HIDDEN_NODE_ID_PROPERTY, node_id)
        char_format.setBackground(QColor("#eef2f7"))
        char_format.setForeground(QColor("#52606d"))
        return char_format

    def _apply_hidden_formats(self, text: str, nodes: tuple[HiddenTextNode, ...]) -> None:
        for node in nodes:
            cursor = QTextCursor(self.document())
            cursor.setPosition(self._python_to_qt_position(text, node.display_start))
            cursor.setPosition(
                self._python_to_qt_position(text, node.display_end),
                QTextCursor.MoveMode.KeepAnchor,
            )
            cursor.setCharFormat(self._hidden_format(node.node_id))

    def _clear_undo_stack(self) -> None:
        self.document().clearUndoRedoStacks()

    def set_display_document(
        self,
        text: str,
        nodes: tuple[HiddenTextNode, ...] = (),
        *,
        reset_undo: bool = True,
    ) -> None:
        """Load display-only text and protected metadata without committing it."""

        text = str(text)
        self._programmatic_change = True
        try:
            self.setPlainText(text)
            self._apply_hidden_formats(text, tuple(nodes))
            if reset_undo:
                self._clear_undo_stack()
            self.document().setModified(False)
            self._sync_timer.stop()
        finally:
            self._programmatic_change = False

    def replace_display_document(
        self,
        text: str,
        nodes: tuple[HiddenTextNode, ...] = (),
    ) -> bool:
        """Replace display text as one undoable edit and attach marker metadata."""

        text = str(text)
        if text == self.toPlainText():
            return False
        old_position = self.textCursor().position()
        vertical = self.verticalScrollBar().value()
        horizontal = self.horizontalScrollBar().value()

        self._programmatic_change = True
        try:
            edit_cursor = self.textCursor()
            edit_cursor.beginEditBlock()
            edit_cursor.select(QTextCursor.SelectionType.Document)
            edit_cursor.insertText(text, QTextCharFormat())
            self._apply_hidden_formats(text, tuple(nodes))
            edit_cursor.endEditBlock()
        finally:
            self._programmatic_change = False

        cursor = self.textCursor()
        cursor.setPosition(min(old_position, max(0, self.document().characterCount() - 1)))
        self.setTextCursor(cursor)
        self.verticalScrollBar().setValue(vertical)
        self.horizontalScrollBar().setValue(horizontal)
        return True

    def set_xml(self, value: str) -> None:
        """Load model text without creating an edit/commit cycle."""
        value = str(value)
        if value == self.toPlainText():
            self.document().setModified(False)
            self._sync_timer.stop()
            return
        self.set_display_document(value)

    def replace_xml(self, value: str) -> bool:
        """Replace the document once while keeping the replacement undoable."""
        return self.replace_display_document(str(value))

    def reject_current_commit(self) -> None:
        self._commit_failed = True

    @property
    def last_commit_succeeded(self) -> bool:
        return not self._commit_failed

    @Slot(result=bool)
    def flush(self) -> bool:
        if not self.document().isModified():
            return True
        self._sync_timer.stop()
        self._commit_failed = False
        # Keep modified=True while the signal is delivered so a synchronous
        # ViewModel changed signal cannot reload the same large document.
        self.commitRequested.emit(self.toPlainText())
        if self._commit_failed:
            return False
        self.document().setModified(False)
        return True

    def _selection_intersects_protected(self, cursor: QTextCursor) -> bool:
        if not cursor.hasSelection():
            return False
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        return any(start < protected_end and end > protected_start for _, protected_start, protected_end in self._protected_ranges_qt())

    def _insertion_is_protected(self, cursor: QTextCursor) -> bool:
        if self._selection_intersects_protected(cursor):
            return True
        position = cursor.position()
        return any(start <= position <= end for _, start, end in self._protected_ranges_qt())

    def _deletion_is_protected(self, cursor: QTextCursor, *, backward: bool) -> bool:
        if self._selection_intersects_protected(cursor):
            return True
        position = cursor.position()
        target_start = position - 1 if backward else position
        target_end = position if backward else position + 1
        return any(target_start < end and target_end > start for _, start, end in self._protected_ranges_qt())

    def _reject_protected_edit(self) -> None:
        self.protectedEditRejected.emit(
            "Скрытый большой объект защищён. Для его изменения нажмите «Показать оригинал»."
        )

    def keyPressEvent(self, event) -> None:  # noqa: N802 - Qt virtual
        if not self._protected_ranges_qt():
            super().keyPressEvent(event)
            return
        if event.matches(QKeySequence.StandardKey.Copy) or event.matches(QKeySequence.StandardKey.SelectAll):
            super().keyPressEvent(event)
            return
        if event.matches(QKeySequence.StandardKey.Cut):
            self.cut()
            return
        if event.matches(QKeySequence.StandardKey.Paste):
            self.paste()
            return
        if event.matches(QKeySequence.StandardKey.Undo) or event.matches(QKeySequence.StandardKey.Redo):
            super().keyPressEvent(event)
            return

        cursor = self.textCursor()
        if not cursor.hasSelection() and event.key() in {Qt.Key.Key_Right, Qt.Key.Key_Left}:
            position = cursor.position()
            for _, start, end in self._protected_ranges_qt():
                if event.key() == Qt.Key.Key_Right and position == start:
                    cursor.setPosition(end)
                    self.setTextCursor(cursor)
                    return
                if event.key() == Qt.Key.Key_Left and position == end:
                    cursor.setPosition(start)
                    self.setTextCursor(cursor)
                    return

        if event.key() == Qt.Key.Key_Backspace and self._deletion_is_protected(cursor, backward=True):
            self._reject_protected_edit()
            return
        if event.key() == Qt.Key.Key_Delete and self._deletion_is_protected(cursor, backward=False):
            self._reject_protected_edit()
            return
        if (event.text() or event.key() in {Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Tab}) and self._insertion_is_protected(cursor):
            self._reject_protected_edit()
            return
        super().keyPressEvent(event)

    def insertPlainText(self, text: str) -> None:  # noqa: N802 - Qt API
        if not self._programmatic_change and self._insertion_is_protected(self.textCursor()):
            self._reject_protected_edit()
            return
        super().insertPlainText(text)

    def insertFromMimeData(self, source) -> None:  # noqa: N802 - Qt virtual
        if self._insertion_is_protected(self.textCursor()):
            self._reject_protected_edit()
            return
        super().insertFromMimeData(source)

    def cut(self) -> None:
        if self._selection_intersects_protected(self.textCursor()):
            self._reject_protected_edit()
            return
        super().cut()

    def paste(self) -> None:
        if self._insertion_is_protected(self.textCursor()):
            self._reject_protected_edit()
            return
        super().paste()

    def dropEvent(self, event) -> None:  # noqa: N802 - Qt virtual
        if self._protected_ranges_qt():
            event.ignore()
            self._reject_protected_edit()
            return
        super().dropEvent(event)

    def _guard_cursor_position(self) -> None:
        if self._cursor_guard_active:
            return
        cursor = self.textCursor()
        position = cursor.position()
        if cursor.hasSelection():
            self._last_cursor_position = position
            return
        for _, start, end in self._protected_ranges_qt():
            if start < position < end:
                target = end if position >= self._last_cursor_position else start
                self._cursor_guard_active = True
                try:
                    cursor.setPosition(target)
                    self.setTextCursor(cursor)
                finally:
                    self._cursor_guard_active = False
                position = target
                break
        self._last_cursor_position = position

    @Slot(int)
    def zoom_by(self, delta: int) -> None:
        new_size = max(self.MIN_FONT_SIZE, min(self.MAX_FONT_SIZE, self._font_size + int(delta)))
        if new_size == self._font_size:
            return
        self._font_size = new_size
        font = self.font()
        font.setPixelSize(new_size)
        self.setFont(font)
        self.fontSizeChanged.emit(new_size)

    @Slot()
    def reset_zoom(self) -> None:
        if self._font_size == self.DEFAULT_FONT_SIZE:
            return
        self._font_size = self.DEFAULT_FONT_SIZE
        font = self.font()
        font.setPixelSize(self._font_size)
        self.setFont(font)
        self.fontSizeChanged.emit(self._font_size)

    @Slot(int, int, result=bool)
    def go_to_position(self, line: int, column: int = 0) -> bool:
        """Move to a 1-based line/column and highlight its line without edits."""
        if line < 1:
            return False
        block = self.document().findBlockByNumber(line - 1)
        if not block.isValid():
            return False

        zero_based_column = max(0, column - 1) if column > 0 else 0
        zero_based_column = min(zero_based_column, max(0, block.length() - 1))
        cursor = QTextCursor(block)
        cursor.setPosition(block.position() + zero_based_column)
        self.setTextCursor(cursor)
        self.centerCursor()

        line_cursor = QTextCursor(block)
        selection = QTextEdit.ExtraSelection()
        selection.cursor = line_cursor
        selection.format.setBackground(QColor("#dbeafe"))
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        self.setExtraSelections([selection])
        self._diagnostic_timer.start()
        return True

    @Slot()
    def clear_diagnostic_highlight(self) -> None:
        self.setExtraSelections([])

class _NativeEditorBindingBase(QObject):
    """Shared presentation-only controls exposed to the QML toolbar."""

    stateChanged = Signal()

    def __init__(self, editor: NativeXmlEditor, view_model, parent=None) -> None:
        super().__init__(parent)
        self.editor = editor
        self.view_model = view_model
        self.display_document = XmlDisplayDocument()
        self._showing_original = False
        editor.undoAvailable.connect(self.stateChanged)
        editor.redoAvailable.connect(self.stateChanged)
        editor.fontSizeChanged.connect(self.stateChanged)
        editor.protectedEditRejected.connect(self._set_notice)

    @Property(int, notify=stateChanged)
    def fontSize(self) -> int:  # noqa: N802 - exposed to QML
        return self.editor.font_size

    @Property(bool, notify=stateChanged)
    def canUndo(self) -> bool:  # noqa: N802 - exposed to QML
        return self.editor.document().isUndoAvailable()

    @Property(bool, notify=stateChanged)
    def canRedo(self) -> bool:  # noqa: N802 - exposed to QML
        return self.editor.document().isRedoAvailable()

    @Property(bool, notify=stateChanged)
    def hasLargeNodes(self) -> bool:  # noqa: N802 - exposed to QML
        return self.display_document.has_large_nodes

    @Property(bool, notify=stateChanged)
    def showingOriginal(self) -> bool:  # noqa: N802 - exposed to QML
        return self._showing_original and self.display_document.has_large_nodes

    def _set_notice(self, message: str) -> None:
        refresh = getattr(self.view_model, "_refresh", None)
        if callable(refresh):
            refresh(str(message))

    def _full_xml_from_model(self) -> str:
        raise NotImplementedError

    def _set_full_xml_on_model(self, value: str) -> None:
        raise NotImplementedError

    def _render_current_document(self, *, reset_undo: bool = True) -> None:
        if self._showing_original or not self.display_document.has_large_nodes:
            self.editor.set_display_document(
                self.display_document.full_xml,
                reset_undo=reset_undo,
            )
        else:
            self.editor.set_display_document(
                self.display_document.compact_xml,
                self.display_document.hidden_nodes,
                reset_undo=reset_undo,
            )
        self.stateChanged.emit()

    def _load_full_xml(self, value: str, *, reset_mode: bool = True) -> None:
        self.display_document.set_full_xml(str(value))
        if reset_mode or not self.display_document.has_large_nodes:
            self._showing_original = False
        self._render_current_document(reset_undo=True)

    def _commit_editor_text(self, value: str) -> str | None:
        """Commit the visible representation without ever exposing it as full XML."""

        value = str(value)
        if self._showing_original or not self.display_document.has_large_nodes:
            had_large_nodes = self.display_document.has_large_nodes
            self.display_document.set_full_xml(value)
            if not self.display_document.has_large_nodes:
                self._showing_original = False
            elif not had_large_nodes:
                # The editor currently contains the full value which just grew
                # beyond the threshold, so its actual representation is Original.
                self._showing_original = True
            full_xml = self.display_document.full_xml
        else:
            try:
                full_xml = self.display_document.commit_compact(
                    value,
                    self.editor.protected_marker_ranges(),
                )
            except CompactSyncError as error:
                self.editor.reject_current_commit()
                self._set_notice(str(error))
                return None

        self._set_full_xml_on_model(full_xml)
        self.stateChanged.emit()
        return full_xml

    def _replace_full_xml(self, value: str, *, undoable: bool) -> None:
        """Replace authoritative XML and rebuild the current representation."""

        self.display_document.set_full_xml(str(value))
        if not self.display_document.has_large_nodes:
            self._showing_original = False

        if self._showing_original or not self.display_document.has_large_nodes:
            display_text = self.display_document.full_xml
            nodes: tuple[HiddenTextNode, ...] = ()
        else:
            display_text = self.display_document.compact_xml
            nodes = self.display_document.hidden_nodes

        if undoable:
            self.editor.replace_display_document(display_text, nodes)
        else:
            self.editor.set_display_document(display_text, nodes, reset_undo=True)
        self._set_full_xml_on_model(self.display_document.full_xml)
        self.stateChanged.emit()

    def _sync_from_model_if_needed(self) -> None:
        value = str(self._full_xml_from_model())
        if value == self.display_document.full_xml:
            return
        if self.editor.dirty:
            return
        self._load_full_xml(value, reset_mode=True)

    @Slot(result=bool)
    def flush(self) -> bool:
        return self.editor.flush()

    @Slot(result=bool)
    def toggleLargeText(self) -> bool:  # noqa: N802 - exposed to QML
        if not self.display_document.has_large_nodes:
            return False
        if not self.editor.flush():
            return False
        if not self.display_document.has_large_nodes:
            self._showing_original = False
            self._render_current_document(reset_undo=True)
            return True

        if self._showing_original:
            # flush() above re-scans the edited original and refreshes the
            # authoritative document before compacting it again.
            self._showing_original = False
            self._render_current_document(reset_undo=True)
        else:
            self._showing_original = True
            self.editor.set_display_document(
                self.display_document.full_xml,
                reset_undo=True,
            )
            self.stateChanged.emit()
        return True

    @Slot(int, int, result=bool)
    def goToFullPosition(self, line: int, column: int = 0) -> bool:  # noqa: N802
        if self._showing_original or not self.display_document.has_large_nodes:
            return self.editor.go_to_position(line, column)
        mapped_line, mapped_column = self.display_document.full_line_column_to_display(
            line,
            column,
        )
        return self.editor.go_to_position(mapped_line, mapped_column)

    @Slot()
    def undo(self) -> None:
        self.editor.undo()

    @Slot()
    def redo(self) -> None:
        self.editor.redo()

    @Slot()
    def cut(self) -> None:
        self.editor.cut()

    @Slot()
    def copy(self) -> None:
        self.editor.copy()

    @Slot()
    def paste(self) -> None:
        self.editor.paste()

    @Slot()
    def selectAll(self) -> None:  # noqa: N802 - exposed to QML
        self.editor.selectAll()

    @Slot()
    def zoomIn(self) -> None:  # noqa: N802 - exposed to QML
        self.editor.zoom_by(1)

    @Slot()
    def zoomOut(self) -> None:  # noqa: N802 - exposed to QML
        self.editor.zoom_by(-1)

    @Slot()
    def resetZoom(self) -> None:  # noqa: N802 - exposed to QML
        self.editor.reset_zoom()


class NativeXmlEditorBinding(_NativeEditorBindingBase):
    """Presentation adapter between the main XML editor and GuiViewModel."""

    def __init__(
        self,
        editor: NativeXmlEditor,
        view_model,
        parent=None,
        *,
        connect_navigation: bool = True,
    ) -> None:
        super().__init__(editor, view_model, parent)
        editor.commitRequested.connect(self._commit)
        view_model.changed.connect(self._on_model_changed)
        if connect_navigation:
            view_model.navigateToXmlPosition.connect(self.goToFullPosition)
        self.load_from_model()

    def _full_xml_from_model(self) -> str:
        return self.view_model.xml

    def _set_full_xml_on_model(self, value: str) -> None:
        self.view_model.setXml(value)

    @Slot()
    def load_from_model(self) -> None:
        self._load_full_xml(self.view_model.xml, reset_mode=True)

    @Slot(str)
    def _commit(self, value: str) -> None:
        self._commit_editor_text(value)

    @Slot(result=bool)
    def formatXml(self) -> bool:  # noqa: N802 - exposed to QML prototype
        if not self.editor.flush():
            return False
        formatted = self.view_model.formattedXml(self.display_document.full_xml)
        if not formatted:
            return False
        self._replace_full_xml(formatted, undoable=True)
        return True

    @Slot()
    def validateXml(self) -> None:  # noqa: N802 - exposed to QML prototype
        if not self.editor.flush():
            return
        self.view_model.validate()

    @Slot(str)
    def saveXml(self, path: str) -> None:  # noqa: N802 - exposed to QML prototype
        if not self.editor.flush():
            return
        self.view_model.saveXml(path)

    @Slot()
    def copyXml(self) -> None:  # noqa: N802 - exposed to QML prototype
        if not self.editor.flush():
            return
        self.view_model.copyXml()

    def _on_model_changed(self) -> None:
        self._sync_from_model_if_needed()


class NativeFormatterEditorBinding(_NativeEditorBindingBase):
    """Independent adapter for the formatter document."""

    def __init__(self, editor: NativeXmlEditor, view_model, parent=None) -> None:
        super().__init__(editor, view_model, parent)
        editor.commitRequested.connect(self._commit)
        view_model.changed.connect(self._on_model_changed)
        self.load_from_model()

    def _full_xml_from_model(self) -> str:
        return self.view_model.formatterXml

    def _set_full_xml_on_model(self, value: str) -> None:
        self.view_model.setFormatterXml(value)

    @Slot()
    def load_from_model(self) -> None:
        self._load_full_xml(self.view_model.formatterXml, reset_mode=True)

    @Slot(str)
    def _commit(self, value: str) -> None:
        self._commit_editor_text(value)

    @Slot(result=bool)
    def formatXml(self) -> bool:  # noqa: N802 - exposed to QML
        if not self.editor.flush():
            return False
        formatted = self.view_model.formattedFormatterXml(self.display_document.full_xml)
        if not formatted:
            return False
        self._replace_full_xml(formatted, undoable=True)
        return True

    @Slot()
    def clearXml(self) -> None:  # noqa: N802 - exposed to QML
        self._showing_original = False
        self._replace_full_xml("", undoable=False)

    @Slot()
    def copyXml(self) -> None:  # noqa: N802 - exposed to QML
        if not self.editor.flush():
            return
        self.view_model.copyFormatterXml()

    @Slot(str)
    def loadXml(self, path: str) -> None:  # noqa: N802 - exposed to QML
        if not self.editor.flush():
            return
        self.view_model.loadFormatterXml(path)

    @Slot(str)
    def saveXml(self, path: str) -> None:  # noqa: N802 - exposed to QML
        if not self.editor.flush():
            return
        self.view_model.saveFormatterXml(path)

    def _on_model_changed(self) -> None:
        self._sync_from_model_if_needed()
