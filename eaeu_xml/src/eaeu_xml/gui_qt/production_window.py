"""Production QWidget host for QML pages plus native XML editors."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QPalette
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from .base64_model import Base64UtilityModel
from .fonts import fixed_font_family
from .native_xml_editor import (
    NativeFormatterEditorBinding,
    NativeXmlEditor,
    NativeXmlEditorBinding,
)


QML_ROOT = Path(__file__).with_name("qml")
APP_BACKGROUND = QColor("#f5f7fa")
SURFACE_BACKGROUND = QColor("#ffffff")


def _set_widget_background(widget: QWidget, color: QColor) -> None:
    """Make layout gaps deterministic instead of inheriting the OS palette."""
    palette = widget.palette()
    palette.setColor(QPalette.ColorRole.Window, color)
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)


def _qml_widget(
    source: Path,
    *,
    parent=None,
    context: dict[str, object] | None = None,
    clear_color: QColor = APP_BACKGROUND,
) -> QQuickWidget:
    widget = QQuickWidget(parent)
    widget.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
    widget.setClearColor(clear_color)
    _set_widget_background(widget, clear_color)
    for name, value in (context or {}).items():
        widget.rootContext().setContextProperty(name, value)
    widget.setSource(QUrl.fromLocalFile(str(source)))
    if widget.status() != QQuickWidget.Status.Ready:
        raise RuntimeError("; ".join(error.toString() for error in widget.errors()))
    return widget


class NativeEditorPage(QWidget):
    """A QML toolbar and a persistent QPlainTextEdit in one supported hierarchy."""

    def __init__(self, binding, toolbar_qml: Path, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("nativeEditorPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(
            "QWidget#nativeEditorPage { background: #ffffff; border: 1px solid #e1e6ed; border-radius: 8px; }"
            "QPlainTextEdit { background: #fbfcff; color: #20242b; border: 1px solid #d9dfe7; "
            "border-radius: 5px; padding: 6px; selection-background-color: #0a6cff; }"
        )
        _set_widget_background(self, SURFACE_BACKGROUND)
        self.binding = binding
        self.editor = binding.editor
        self.editor.setParent(self)
        self.toolbar = _qml_widget(
            toolbar_qml,
            parent=self,
            context={"nativeBridge": binding},
            clear_color=SURFACE_BACKGROUND,
        )
        self.toolbar.setFixedHeight(42)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.editor, 1)


class ProductionMainWindow(QWidget):
    """Hybrid production shell: QML navigation/pages + native large-text editors."""

    QML_PAGE_INDEX = 0
    XML_PAGE_INDEX = 1
    FORMATTER_PAGE_INDEX = 2

    def __init__(self, view_model, parent=None) -> None:
        super().__init__(parent)
        self.view_model = view_model
        self.current_index = 0
        self.setWindowTitle("ГИС_xml")
        self.resize(1440, 900)
        self.setMinimumSize(980, 640)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        _set_widget_background(self, APP_BACKGROUND)

        font_family = fixed_font_family()
        self.base64_model = Base64UtilityModel(self)
        qml_context = {
            "viewModel": view_model,
            "base64Model": self.base64_model,
            "fixedFontFamily": font_family,
        }

        self.navigation = _qml_widget(QML_ROOT / "components" / "TopNavigation.qml", parent=self)
        self.navigation.setFixedHeight(42)
        navigation_root = self.navigation.rootObject()
        navigation_root.selected.connect(self.select_page)

        self.qml_pages = _qml_widget(QML_ROOT / "Main.qml", parent=self, context=qml_context)

        self.xml_editor = NativeXmlEditor(self, font_family=font_family)
        self.xml_binding = NativeXmlEditorBinding(
            self.xml_editor,
            view_model,
            self,
            connect_navigation=False,
        )
        self.xml_page = NativeEditorPage(
            self.xml_binding,
            QML_ROOT / "native" / "XmlNativeToolbar.qml",
            self,
        )

        self.formatter_editor = NativeXmlEditor(self, font_family=font_family)
        self.formatter_binding = NativeFormatterEditorBinding(
            self.formatter_editor,
            view_model,
            self,
        )
        self.formatter_page = NativeEditorPage(
            self.formatter_binding,
            QML_ROOT / "native" / "FormatterNativeToolbar.qml",
            self,
        )

        self.pages = QStackedWidget(self)
        _set_widget_background(self.pages, APP_BACKGROUND)
        self.pages.addWidget(self.qml_pages)
        self.pages.addWidget(self.xml_page)
        self.pages.addWidget(self.formatter_page)

        self.notice = _qml_widget(QML_ROOT / "NoticeBar.qml", parent=self, context=qml_context)
        self.notice.setFixedHeight(22)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        layout.addWidget(self.navigation)
        layout.addWidget(self.pages, 1)
        layout.addWidget(self.notice)

        view_model.navigateToXmlPosition.connect(self._navigate_to_diagnostic)
        self.select_page(0)

    def _set_qml_index(self, index: int) -> None:
        root = self.qml_pages.rootObject()
        if root is not None:
            root.setProperty("currentIndex", index)

    def _set_navigation_index(self, index: int) -> None:
        root = self.navigation.rootObject()
        if root is not None:
            root.setProperty("currentIndex", index)

    def select_page(self, index: int) -> None:
        index = int(index)
        if index < 0 or index > 6:
            return

        if index == 2:
            # The validation page must always see the latest editor text even
            # when its 300 ms debounce has not fired yet.
            self.xml_binding.flush()

        self.current_index = index
        self._set_navigation_index(index)
        self._set_qml_index(index)

        if index == 1:
            self.pages.setCurrentIndex(self.XML_PAGE_INDEX)
        elif index == 3:
            self.pages.setCurrentIndex(self.FORMATTER_PAGE_INDEX)
        else:
            self.pages.setCurrentIndex(self.QML_PAGE_INDEX)

    def _navigate_to_diagnostic(self, line: int, column: int) -> None:
        if line <= 0:
            return
        self.select_page(1)
        self.xml_binding.goToFullPosition(line, column)
