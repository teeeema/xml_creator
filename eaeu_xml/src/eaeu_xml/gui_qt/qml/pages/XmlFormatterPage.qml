import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item {
    id: root
    signal openRequested()
    signal saveRequested()
    function syncNow() { editor.flush() }
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
                        root.syncNow()
                        viewModel.formatFormatterXml()
                        editor.setTextFromModel(viewModel.formatterXml)
                    }
                }
                AppButton { text: "Очистить"; compact: true; onClicked: { editor.setTextFromModel(""); viewModel.clearFormatterXml() } }
                AppButton { text: "Копировать"; compact: true; onClicked: { root.syncNow(); viewModel.copyFormatterXml() } }
                AppButton { text: "Открыть файл"; compact: true; onClicked: { root.syncNow(); root.openRequested() } }
                AppButton { text: "Сохранить XML"; compact: true; onClicked: { root.syncNow(); root.saveRequested() } }
                Label { text: (viewModel ? viewModel.formatterFontSize : 14) + " px"; color: Theme.secondary }
            }
            XmlTextEditor {
                id: editor
                Layout.fillWidth: true; Layout.fillHeight: true
                editorObjectName: "formatterEditor"
                viewportObjectName: "formatterEditorViewport"
                fontSize: viewModel ? viewModel.formatterFontSize : 14
                Component.onCompleted: setTextFromModel(viewModel ? viewModel.formatterXml : "")
                onTextCommitted: text => viewModel.setFormatterXml(text)
                onZoomRequested: delta => viewModel.changeFormatterFontSize(delta)
                onZoomResetRequested: viewModel.resetFormatterFontSize()
            }
        }
    }
    Connections { target: viewModel; function onChanged() { if (!editor.syncPending && editor.text !== viewModel.formatterXml) editor.setTextFromModel(viewModel.formatterXml) } }
}
