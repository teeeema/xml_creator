import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
import "../components/XmlPosition.js" as XmlPosition
Item { id: root; signal saveXmlRequested()
    function syncNow() {
        xml.flush()
    }
    function goToPosition(line, column) {
        const start = XmlPosition.offsetFor(xml.text, line, column)
        if (start < 0) return
        const end = xml.text.indexOf("\n", start)
        xml.selectRangeAndReveal(start, end < 0 ? xml.text.length : end)
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
                        if (formatted !== "" && formatted !== xml.text) { xml.setTextFromModel(formatted); viewModel.setXml(formatted) }
                    }
                }
                AppButton { text: "Отменить"; compact: true; enabled: xml.canUndo; onClicked: xml.undo() }
                AppButton { text: "Повторить"; compact: true; enabled: xml.canRedo; onClicked: xml.redo() }
                AppButton { text: "Копировать"; compact: true; onClicked: { root.syncNow(); viewModel.copyXml() } }
                AppButton { text: "Сохранить XML"; compact: true; onClicked: { root.syncNow(); root.saveXmlRequested() } }
                Label { text: (viewModel ? viewModel.xmlFontSize : 14) + " px"; color: Theme.secondary; Layout.leftMargin: 4 }
            }
            XmlTextEditor {
                id: xml
                Layout.fillWidth: true; Layout.fillHeight: true
                editorObjectName: "mainXmlEditor"
                viewportObjectName: "mainXmlEditorViewport"
                fontSize: viewModel ? viewModel.xmlFontSize : 14
                Component.onCompleted: setTextFromModel(viewModel ? viewModel.xml : "")
                onTextCommitted: text => viewModel.setXml(text)
                onZoomRequested: delta => viewModel.changeXmlFontSize(delta)
                onZoomResetRequested: viewModel.resetXmlFontSize()
            }
        }
    }
    Connections { target: viewModel; function onChanged() { if (!xml.syncPending && xml.text !== viewModel.xml) xml.setTextFromModel(viewModel.xml) } }
}
