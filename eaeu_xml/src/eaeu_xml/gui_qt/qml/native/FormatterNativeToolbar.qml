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
        Label { text: "Форматирование XML"; color: Theme.text; font.bold: true; font.pixelSize: 17; Layout.fillWidth: true }
        AppButton { objectName: "nativeFormatterFormat"; text: "Форматировать"; compact: true; onClicked: nativeBridge.formatXml() }
        AppButton { text: "Очистить"; compact: true; onClicked: nativeBridge.clearXml() }
        AppButton { text: "Копировать"; compact: true; onClicked: nativeBridge.copyXml() }
        AppButton { text: "Открыть файл"; compact: true; onClicked: { nativeBridge.flush(); openDialog.open() } }
        AppButton { text: "Сохранить XML"; compact: true; onClicked: saveDialog.open() }
        AppButton {
            objectName: "nativeFormatterLargeTextToggle"
            text: nativeBridge && nativeBridge.showingOriginal ? "Скрыть большие объекты" : "Показать оригинал"
            compact: true
            enabled: nativeBridge ? nativeBridge.hasLargeNodes : false
            onClicked: nativeBridge.toggleLargeText()
        }
        Label { text: (nativeBridge ? nativeBridge.fontSize : 14) + " px"; color: Theme.secondary }
    }
    FileDialog {
        id: openDialog
        title: "Открыть XML"
        fileMode: FileDialog.OpenFile
        nameFilters: ["XML (*.xml)"]
        onAccepted: nativeBridge.loadXml(selectedFile.toLocalFile())
    }
    FileDialog {
        id: saveDialog
        title: "Сохранить XML"
        fileMode: FileDialog.SaveFile
        nameFilters: ["XML (*.xml)"]
        onAccepted: nativeBridge.saveXml(selectedFile.toLocalFile())
    }
}
