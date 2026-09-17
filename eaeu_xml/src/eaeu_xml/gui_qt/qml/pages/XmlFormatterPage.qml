import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item {
    id: root
    signal openRequested()
    signal saveRequested()
    Card {
        anchors.fill: parent
        ColumnLayout {
            anchors.fill: parent; anchors.margins: 16; spacing: 12
            RowLayout {
                Layout.fillWidth: true
                Label { text: "Форматирование XML"; color: Theme.text; font.bold: true; font.pixelSize: 17; Layout.fillWidth: true }
                AppButton {
                    id: formatButton
                    objectName: "formatterFormatButton"
                    text: "Форматировать"; compact: true
                    onClicked: {
                        viewModel.setFormatterXml(editor.text)
                        viewModel.formatFormatterXml()
                        editor.text = viewModel.formatterXml
                    }
                }
                AppButton { text: "Очистить"; compact: true; onClicked: editor.clear() }
                AppButton { text: "Копировать"; compact: true; onClicked: viewModel.copyFormatterXml() }
                AppButton { text: "Открыть файл"; compact: true; onClicked: root.openRequested() }
                AppButton { text: "Сохранить XML"; compact: true; onClicked: root.saveRequested() }
                Label { text: (viewModel ? viewModel.formatterFontSize : 14) + " px"; color: Theme.secondary }
            }
            ScrollView {
                id: scroll; Layout.fillWidth: true; Layout.fillHeight: true; clip: true
                ScrollBar.vertical.policy: ScrollBar.AsNeeded
                ScrollBar.horizontal.policy: ScrollBar.AsNeeded
                TextArea {
                    id: editor
                    objectName: "formatterEditor"
                    text: viewModel ? viewModel.formatterXml : ""
                    width: scroll.availableWidth
                    height: Math.max(scroll.availableHeight, contentHeight + topPadding + bottomPadding)
                    wrapMode: TextArea.NoWrap
                    font.family: "monospace"; font.pixelSize: viewModel ? viewModel.formatterFontSize : 14
                    color: Theme.text; selectionColor: Theme.accent; selectedTextColor: "white"
                    background: Rectangle { color: "#fbfcff"; border.color: Theme.border; radius: 5 }
                    onTextChanged: if (viewModel && text !== viewModel.formatterXml) viewModel.setFormatterXml(text)
                    Keys.onPressed: event => {
                        const modifier = (event.modifiers & Qt.ControlModifier) || (event.modifiers & Qt.MetaModifier)
                        if (!modifier) return
                        if (event.key === Qt.Key_Plus || event.key === Qt.Key_Equal) { viewModel.changeFormatterFontSize(1); event.accepted = true }
                        else if (event.key === Qt.Key_Minus) { viewModel.changeFormatterFontSize(-1); event.accepted = true }
                        else if (event.key === Qt.Key_0) { viewModel.resetFormatterFontSize(); event.accepted = true }
                    }
                }
            }
        }
    }
}
