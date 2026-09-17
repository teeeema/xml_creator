import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../components"

Item {
    id: root
    property int mode: 0
    property var utilityModel: null
    readonly property bool modelReady: utilityModel !== null && utilityModel !== undefined

    FileDialog { id: encodeOpen; title: "Выбрать файл"; fileMode: FileDialog.OpenFile; onAccepted: if (root.modelReady) root.utilityModel.encodeFile(selectedFile.toLocalFile()) }
    FileDialog { id: encodeSave; title: "Сохранить Base64"; fileMode: FileDialog.SaveFile; nameFilters: ["Text (*.txt)"]; onAccepted: if (root.modelReady) root.utilityModel.saveBase64(selectedFile.toLocalFile()) }
    FileDialog { id: decodeOpen; title: "Открыть Base64"; fileMode: FileDialog.OpenFile; nameFilters: ["Text (*.txt)", "Все файлы (*)"]; onAccepted: if (root.modelReady) root.utilityModel.openBase64(selectedFile.toLocalFile()) }
    FileDialog { id: decodeSave; title: "Сохранить файл"; fileMode: FileDialog.SaveFile; onAccepted: if (root.modelReady) root.utilityModel.saveDecoded(selectedFile.toLocalFile()) }

    ColumnLayout {
        anchors.fill: parent
        spacing: 12

        RowLayout {
            spacing: 8
            AppButton { text: "Кодировать файл"; primary: root.mode === 0; onClicked: root.mode = 0 }
            AppButton { text: "Декодировать Base64"; primary: root.mode === 1; onClicked: root.mode = 1 }
            Item { Layout.fillWidth: true }
            BusyIndicator { running: root.modelReady && root.utilityModel.busy; visible: running; implicitWidth: 24; implicitHeight: 24 }
            Label { text: root.modelReady ? root.utilityModel.status : ""; color: Theme.secondary; visible: text.length > 0 }
        }

        Card {
            Layout.fillWidth: true
            Layout.fillHeight: true
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12

                ColumnLayout {
                    visible: root.mode === 0
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    spacing: 12
                    RowLayout {
                        AppButton { text: "Выбрать файл"; enabled: root.modelReady && !root.utilityModel.busy; onClicked: encodeOpen.open() }
                        AppButton { text: "Копировать Base64"; enabled: root.modelReady && !root.utilityModel.busy && root.utilityModel.encodedFileName.length > 0; onClicked: root.utilityModel.copyBase64() }
                        AppButton { text: "Сохранить Base64"; enabled: root.modelReady && !root.utilityModel.busy && root.utilityModel.encodedFileName.length > 0; onClicked: encodeSave.open() }
                        AppButton { text: "Очистить"; enabled: root.modelReady && !root.utilityModel.busy; onClicked: root.utilityModel.clearEncode() }
                        Item { Layout.fillWidth: true }
                        AppButton { text: root.modelReady && root.utilityModel.showingFullPreview ? "Скрыть" : "Показать полностью"; compact: true; enabled: root.modelReady && !root.utilityModel.busy && root.utilityModel.canTogglePreview; onClicked: root.utilityModel.togglePreview() }
                    }
                    Label { text: root.modelReady && root.utilityModel.encodedFileName.length ? "Файл: " + root.utilityModel.encodedFileName + "   •   Исходный размер: " + root.utilityModel.sourceSize + " байт   •   Base64: " + root.utilityModel.encodedSize + " символов" : "Файл не выбран"; color: Theme.secondary; wrapMode: Text.Wrap }
                    Rectangle {
                        Layout.fillWidth: true; Layout.fillHeight: true; radius: 6; color: "#fbfcff"; border.color: Theme.fieldBorder
                        ScrollView { anchors.fill: parent; anchors.margins: 8; clip: true
                            TextArea { readOnly: true; text: root.modelReady ? root.utilityModel.encodedPreview : ""; wrapMode: TextEdit.WrapAnywhere; color: Theme.text; background: null; selectByMouse: true }
                        }
                    }
                }

                ColumnLayout {
                    visible: root.mode === 1
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    spacing: 12
                    RowLayout {
                        AppButton { text: "Открыть Base64"; enabled: root.modelReady && !root.utilityModel.busy; onClicked: decodeOpen.open() }
                        AppButton { text: "Декодировать"; primary: true; enabled: root.modelReady && !root.utilityModel.busy; onClicked: { root.utilityModel.setDecodeInput(decodeInput.text); root.utilityModel.decode() } }
                        AppButton { text: "Сохранить файл"; enabled: root.modelReady && !root.utilityModel.busy && root.utilityModel.hasDecodedResult; onClicked: decodeSave.open() }
                        AppButton { text: "Очистить"; enabled: root.modelReady && !root.utilityModel.busy; onClicked: root.utilityModel.clearDecode() }
                        Item { Layout.fillWidth: true }
                        Label { text: root.modelReady && root.utilityModel.hasDecodedResult ? "Результат: " + root.utilityModel.decodedSize + " байт" + (root.utilityModel.decodedFormatHint.length ? "   •   Похоже на " + root.utilityModel.decodedFormatHint : "") : ""; color: Theme.secondary }
                    }
                    Rectangle {
                        Layout.fillWidth: true; Layout.fillHeight: true; radius: 6; color: "#fbfcff"; border.color: Theme.fieldBorder
                        ScrollView { anchors.fill: parent; anchors.margins: 8; clip: true
                            TextArea {
                                id: decodeInput
                                placeholderText: "Вставьте Base64 или откройте .txt"
                                wrapMode: TextEdit.WrapAnywhere; color: Theme.text; background: null; selectByMouse: true
                                onTextChanged: if (root.modelReady && text !== root.utilityModel.decodeInput) root.utilityModel.setDecodeInput(text)
                                Component.onCompleted: if (root.modelReady) text = root.utilityModel.decodeInput
                                Connections {
                                    target: root.modelReady ? root.utilityModel : null
                                    ignoreUnknownSignals: true
                                    function onChanged() {
                                        if (root.modelReady && decodeInput.text !== root.utilityModel.decodeInput)
                                            decodeInput.text = root.utilityModel.decodeInput
                                    }
                                }
                            }
                        }
                    }
                }

                Label { text: root.modelReady ? root.utilityModel.error : ""; color: Theme.error; visible: text.length > 0; wrapMode: Text.Wrap; Layout.fillWidth: true }
            }
        }
    }
}
