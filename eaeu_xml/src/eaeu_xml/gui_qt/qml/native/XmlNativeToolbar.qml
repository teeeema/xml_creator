import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../components"

Rectangle {
    color: Theme.surface
    RowLayout {
        anchors.fill: parent
        spacing: 8
        Label { text: "Сформированный XML"; color: Theme.text; font.bold: true; font.pixelSize: 17; Layout.fillWidth: true }
        AppButton { objectName: "nativeXmlFormat"; text: "Форматировать"; compact: true; onClicked: nativeBridge.formatXml() }
        AppButton { text: "Отменить"; compact: true; enabled: nativeBridge ? nativeBridge.canUndo : false; onClicked: nativeBridge.undo() }
        AppButton { text: "Повторить"; compact: true; enabled: nativeBridge ? nativeBridge.canRedo : false; onClicked: nativeBridge.redo() }
        AppButton {
            objectName: "nativeXmlLargeTextToggle"
            text: nativeBridge && nativeBridge.showingOriginal ? "Скрыть большие объекты" : "Показать оригинал"
            compact: true
            enabled: nativeBridge ? nativeBridge.hasLargeNodes : false
            onClicked: nativeBridge.toggleLargeText()
        }
        AppButton { text: "Копировать"; compact: true; onClicked: nativeBridge.copyXml() }
        AppButton { objectName: "nativeXmlSave"; text: "Сохранить XML"; compact: true; onClicked: saveDialog.open() }
        Label { text: (nativeBridge ? nativeBridge.fontSize : 14) + " px"; color: Theme.secondary; Layout.leftMargin: 4 }
    }
    FileDialog {
        id: saveDialog
        title: "Сохранить XML"
        fileMode: FileDialog.SaveFile
        nameFilters: ["XML (*.xml)"]
        onAccepted: nativeBridge.saveXml(selectedFile.toLocalFile())
    }
}
