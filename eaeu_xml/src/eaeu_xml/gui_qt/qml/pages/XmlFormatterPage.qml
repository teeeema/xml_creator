import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item {
    id: root
    property bool localEdit: false
    property bool updatingFromModel: false
    signal openRequested()
    signal saveRequested()
    function syncNow() { if (localEdit) { viewModel.setFormatterXml(editor.text); localEdit = false } }
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
                        root.updatingFromModel = true
                        editor.text = viewModel.formatterXml
                        root.updatingFromModel = false
                    }
                }
                AppButton { text: "Очистить"; compact: true; onClicked: { editor.clear(); root.syncNow() } }
                AppButton { text: "Копировать"; compact: true; onClicked: { root.syncNow(); viewModel.copyFormatterXml() } }
                AppButton { text: "Открыть файл"; compact: true; onClicked: { root.syncNow(); root.openRequested() } }
                AppButton { text: "Сохранить XML"; compact: true; onClicked: { root.syncNow(); root.saveRequested() } }
                Label { text: (viewModel ? viewModel.formatterFontSize : 14) + " px"; color: Theme.secondary }
            }
            ScrollView {
                id: scroll; Layout.fillWidth: true; Layout.fillHeight: true; clip: true
                ScrollBar.vertical.policy: ScrollBar.AsNeeded
                ScrollBar.horizontal.policy: ScrollBar.AsNeeded
                TextArea {
                    id: editor
                    objectName: "formatterEditor"
                    text: ""
                    width: scroll.availableWidth
                    height: Math.max(scroll.availableHeight, contentHeight + topPadding + bottomPadding)
                    wrapMode: TextArea.NoWrap
                    font.family: "monospace"; font.pixelSize: viewModel ? viewModel.formatterFontSize : 14
                    color: Theme.text; selectionColor: Theme.accent; selectedTextColor: "white"
                    background: Rectangle { color: "#fbfcff"; border.color: Theme.border; radius: 5 }
                    Component.onCompleted: { root.updatingFromModel = true; text = viewModel ? viewModel.formatterXml : ""; root.updatingFromModel = false }
                    onTextChanged: if (!root.updatingFromModel) { root.localEdit = true; formatterSync.restart() }
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
    Timer { id: formatterSync; interval: 300; repeat: false; onTriggered: root.syncNow() }
    Connections { target: viewModel; function onChanged() { if (!root.localEdit && editor.text !== viewModel.formatterXml) { root.updatingFromModel = true; editor.text = viewModel.formatterXml; root.updatingFromModel = false } } }
}
