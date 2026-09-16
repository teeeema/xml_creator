import argparse
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.gui.controller import GuiController


class MainWindow(QMainWindow):
    def __init__(self, processes_root: Path) -> None:
        super().__init__()

        self.controller = GuiController(
            EaeuXmlApplication(processes_root)
        )

        self.setWindowTitle("ГИС_xml")
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)

        root = QWidget()
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(32, 20, 32, 24)
        layout.setSpacing(20)

        # Навигация
        navigation = QHBoxLayout()
        navigation.setSpacing(6)

        for name in (
            "Главная",
            "XML",
            "Проверка",
            "Информация",
            "Настройки",
        ):
            button = QPushButton(name)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFlat(True)
            navigation.addWidget(button)

        navigation.addStretch()
        layout.addLayout(navigation)

        # Заголовок
        title = QLabel("Создание XML")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Выберите процесс, транзакцию и сообщение."
        )
        description.setObjectName("secondaryText")

        layout.addWidget(title)
        layout.addWidget(description)

        # Селекторы
        selectors = QHBoxLayout()
        selectors.setSpacing(12)

        self.process_combo = self._selector(
            selectors,
            "Процесс",
        )

        self.transaction_combo = self._selector(
            selectors,
            "Транзакция",
        )

        self.message_combo = self._selector(
            selectors,
            "Сообщение",
        )

        layout.addLayout(selectors)

        # Основная область
        content = QHBoxLayout()
        content.setSpacing(16)

        form_card = QFrame()
        form_card.setObjectName("card")

        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(24, 24, 24, 24)

        form_title = QLabel("Данные сообщения")
        form_title.setObjectName("cardTitle")

        self.message_info = QLabel()
        self.message_info.setWordWrap(True)
        self.message_info.setObjectName("secondaryText")

        form_layout.addWidget(form_title)
        form_layout.addWidget(self.message_info)
        form_layout.addStretch()

        inspector = QFrame()
        inspector.setObjectName("card")
        inspector.setFixedWidth(320)

        inspector_layout = QVBoxLayout(inspector)
        inspector_layout.setContentsMargins(20, 24, 20, 24)

        inspector_title = QLabel("Информация")
        inspector_title.setObjectName("cardTitle")

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setObjectName("secondaryText")

        inspector_layout.addWidget(inspector_title)
        inspector_layout.addWidget(self.status_label)
        inspector_layout.addStretch()

        content.addWidget(form_card, 1)
        content.addWidget(inspector)

        layout.addLayout(content, 1)

        # Нижняя панель
        footer = QHBoxLayout()

        test_button = QPushButton("Тестовые данные")
        draft_button = QPushButton("Сохранить черновик")
        generate_button = QPushButton("Создать XML")
        generate_button.setObjectName("primaryButton")

        footer.addWidget(test_button)
        footer.addStretch()
        footer.addWidget(draft_button)
        footer.addWidget(generate_button)

        layout.addLayout(footer)

        self.process_combo.currentIndexChanged.connect(
            self.process_changed
        )
        self.transaction_combo.currentIndexChanged.connect(
            self.transaction_changed
        )
        self.message_combo.currentIndexChanged.connect(
            self.message_changed
        )

        self.apply_style()
        self.load_processes()

    def _selector(self, parent, title):
        container = QVBoxLayout()

        label = QLabel(title)
        label.setObjectName("selectorLabel")

        combo = QComboBox()
        combo.setMinimumHeight(40)

        container.addWidget(label)
        container.addWidget(combo)

        parent.addLayout(container, 1)

        return combo

    def load_processes(self):
        self.process_combo.blockSignals(True)
        self.process_combo.clear()

        for process in self.controller.processes:
            self.process_combo.addItem(
                process.process_code,
                process.process_code,
            )

        index = self.process_combo.findData(
            self.controller.process_code
        )

        if index >= 0:
            self.process_combo.setCurrentIndex(index)

        self.process_combo.blockSignals(False)

        self.load_transactions()

    def load_transactions(self):
        self.transaction_combo.blockSignals(True)
        self.transaction_combo.clear()

        for transaction in self.controller.transactions:
            self.transaction_combo.addItem(
                transaction.transaction_code,
                transaction.transaction_code,
            )

        index = self.transaction_combo.findData(
            self.controller.transaction_code
        )

        if index >= 0:
            self.transaction_combo.setCurrentIndex(index)

        self.transaction_combo.blockSignals(False)

        self.load_messages()

    def load_messages(self):
        self.message_combo.blockSignals(True)
        self.message_combo.clear()

        for message in self.controller.messages:
            self.message_combo.addItem(
                message.message_code,
                message.message_code,
            )

        index = self.message_combo.findData(
            self.controller.message_code
        )

        if index >= 0:
            self.message_combo.setCurrentIndex(index)

        self.message_combo.blockSignals(False)

        self.refresh_information()

    def process_changed(self, index):
        code = self.process_combo.itemData(index)

        if not code:
            return

        self.controller.select_process(code)
        self.load_transactions()

    def transaction_changed(self, index):
        code = self.transaction_combo.itemData(index)

        if not code:
            return

        self.controller.select_transaction(code)
        self.load_messages()

    def message_changed(self, index):
        code = self.message_combo.itemData(index)

        if not code:
            return

        self.controller.select_message(code)
        self.refresh_information()

    def refresh_information(self):
        message = self.controller.current_message

        if message is None:
            self.message_info.setText(
                "Сообщение не выбрано."
            )
            self.status_label.clear()
            return

        self.message_info.setText(
            f"{message.message_code}\n\n"
            f"Структура: {message.structure_id}"
        )

        presentation = self.controller.message_presentation()

        if presentation:
            self.status_label.setText(
                f"{presentation.title}\n\n"
                f"{presentation.description}"
            )

    def apply_style(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background: #f5f5f7;
            }

            QWidget {
                font-family: "SF Pro Display";
                font-size: 14px;
                color: #1d1d1f;
            }

            QPushButton {
                border: none;
                border-radius: 9px;
                padding: 9px 14px;
                background: transparent;
            }

            QPushButton:hover {
                background: #e8e8ed;
            }

            QPushButton#primaryButton {
                background: #0071e3;
                color: white;
                padding: 10px 20px;
            }

            QLabel#pageTitle {
                font-size: 28px;
                font-weight: 600;
            }

            QLabel#cardTitle {
                font-size: 17px;
                font-weight: 600;
            }

            QLabel#secondaryText {
                color: #6e6e73;
            }

            QLabel#selectorLabel {
                color: #6e6e73;
                font-size: 12px;
            }

            QFrame#card {
                background: white;
                border: 1px solid #dedede;
                border-radius: 14px;
            }

            QComboBox {
                background: white;
                border: 1px solid #d2d2d7;
                border-radius: 9px;
                padding: 7px 12px;
            }

            QComboBox:hover {
                border-color: #86868b;
            }
            """
        )


def choose_root() -> Path | None:
    path = QFileDialog.getExistingDirectory(
        None,
        "Выберите корневую папку общих процессов",
    )

    return Path(path) if path else None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "processes_root",
        nargs="?",
        type=Path,
    )

    args = parser.parse_args(argv)

    app = QApplication(sys.argv)
    app.setApplicationName("ГИС_xml")

    root = args.processes_root

    if root is None:
        root = choose_root()

    if root is None:
        return 0

    window = MainWindow(root)
    window.show()

    return app.exec()