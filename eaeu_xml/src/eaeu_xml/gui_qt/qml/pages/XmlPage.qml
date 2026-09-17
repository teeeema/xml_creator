import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
import "../components/XmlPosition.js" as XmlPosition
Item { id: root; signal saveXmlRequested()
    property bool localEdit: false
    property bool updatingFromModel: false
    function syncNow() {
        if (localEdit) { viewModel.setXml(xml.text); localEdit = false }
    }
    function goToPosition(line, column) {
        const start = XmlPosition.offsetFor(xml.text, line, column)
        if (start < 0) return
        const end = xml.text.indexOf("\n", start)
        xml.cursorPosition = start
        xml.select(start, end < 0 ? xml.text.length : end)
        const lineHeight = xml.font.pixelSize * 1.35
        editorScroll.contentItem.contentY = Math.max(0, (line - 1) * lineHeight - editorScroll.availableHeight / 2)
        highlightTimer.restart()
    }
    Timer { id: highlightTimer; interval: 1800; onTriggered: xml.deselect() }
    Card { anchors.fill: parent
        ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 12
            RowLayout { Layout.fillWidth: true
                Label { text: "Сформированный XML"; color: Theme.text; font.bold: true; font.pixelSize: 17; Layout.fillWidth: true }
                AppButton {
                    text: "Форматировать"; compact: true
                    onClicked: {
                        const formatted = viewModel.formattedXml(xml.text)
                        if (formatted !== "" && formatted !== xml.text) { updatingFromModel = true; xml.text = formatted; updatingFromModel = false; localEdit = true; syncNow() }
                    }
                }
                AppButton { text: "Отменить"; compact: true; enabled: xml.canUndo; onClicked: xml.undo() }
                AppButton { text: "Повторить"; compact: true; enabled: xml.canRedo; onClicked: xml.redo() }
                AppButton { text: "Копировать"; compact: true; onClicked: { root.syncNow(); viewModel.copyXml() } }
                AppButton { text: "Сохранить XML"; compact: true; onClicked: { root.syncNow(); root.saveXmlRequested() } }
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
                    objectName: "mainXmlEditor"
                    text: ""
                    width: editorScroll.availableWidth
                    height: Math.max(editorScroll.availableHeight, contentHeight + topPadding + bottomPadding)
                    wrapMode: TextArea.NoWrap
                    font.family: "monospace"; font.pixelSize: (viewModel ? viewModel.xmlFontSize : 14); color: Theme.text; selectionColor: Theme.accent; selectedTextColor: "white"
                    background: Rectangle { color: "#fbfcff"; border.color: Theme.border; radius: 5 }
                    Component.onCompleted: { updatingFromModel = true; text = viewModel ? viewModel.xml : ""; updatingFromModel = false }
                    onTextChanged: if (!updatingFromModel) { localEdit = true; syncTimer.restart() }
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
    Timer { id: syncTimer; interval: 300; repeat: false; onTriggered: root.syncNow() }
    Connections { target: viewModel; function onChanged() { if (!root.localEdit && xml.text !== viewModel.xml) { root.updatingFromModel = true; xml.text = viewModel.xml; root.updatingFromModel = false } } }
}
