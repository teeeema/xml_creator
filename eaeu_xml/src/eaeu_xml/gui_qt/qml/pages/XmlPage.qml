import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
Item { id: root; signal saveXmlRequested()
    Card { anchors.fill: parent
        ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 12
            RowLayout { Layout.fillWidth: true
                Label { text: "Сформированный XML"; color: Theme.text; font.bold: true; font.pixelSize: 17; Layout.fillWidth: true }
                AppButton {
                    text: "Форматировать"; compact: true
                    onClicked: {
                        const formatted = viewModel.formattedXml(xml.text)
                        if (formatted !== "" && formatted !== xml.text) { xml.selectAll(); xml.insert(formatted) }
                    }
                }
                AppButton { text: "Отменить"; compact: true; enabled: xml.canUndo; onClicked: xml.undo() }
                AppButton { text: "Повторить"; compact: true; enabled: xml.canRedo; onClicked: xml.redo() }
                AppButton { text: "Копировать"; compact: true; onClicked: viewModel.copyXml() }
                AppButton { text: "Сохранить XML"; compact: true; onClicked: root.saveXmlRequested() }
                Label { text: (viewModel ? viewModel.xmlFontSize : 14) + " px"; color: Theme.secondary; Layout.leftMargin: 4 }
            }
            ScrollView {
                id: editorScroll
                Layout.fillWidth: true; Layout.fillHeight: true; clip: true
                ScrollBar.vertical.policy: ScrollBar.AsNeeded
                ScrollBar.horizontal.policy: ScrollBar.AsNeeded
                ScrollBar.vertical.interactive: true
                TextArea {
                    id: xml
                    text: (viewModel ? viewModel.xml : "")
                    width: editorScroll.availableWidth
                    height: Math.max(editorScroll.availableHeight, contentHeight + topPadding + bottomPadding)
                    wrapMode: TextArea.NoWrap
                    font.family: "monospace"; font.pixelSize: (viewModel ? viewModel.xmlFontSize : 14); color: Theme.text; selectionColor: Theme.accent; selectedTextColor: "white"
                    background: Rectangle { color: "#fbfcff"; border.color: Theme.border; radius: 5 }
                    onTextChanged: if (text !== (viewModel ? viewModel.xml : "")) viewModel.setXml(text)
                    Keys.onPressed: event => {
                        const modifier = (event.modifiers & Qt.ControlModifier) || (event.modifiers & Qt.MetaModifier)
                        if (!modifier) return
                        if (event.key === Qt.Key_Plus || event.key === Qt.Key_Equal) { viewModel.changeXmlFontSize(1); event.accepted = true }
                        else if (event.key === Qt.Key_Minus) { viewModel.changeXmlFontSize(-1); event.accepted = true }
                        else if (event.key === Qt.Key_0) { viewModel.resetXmlFontSize(); event.accepted = true }
                    }
                }
            }
        }
    }
}
