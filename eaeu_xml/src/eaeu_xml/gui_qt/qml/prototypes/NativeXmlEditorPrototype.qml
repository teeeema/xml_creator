import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    color: "#f7f9fc"
    border.color: "#dfe5ee"

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        spacing: 8

        Label {
            text: "QPlainTextEdit prototype"
            font.bold: true
            Layout.fillWidth: true
        }
        Button { text: "Отменить"; onClicked: nativeBridge.undo() }
        Button { text: "Повторить"; onClicked: nativeBridge.redo() }
        Button { text: "Форматировать"; onClicked: nativeBridge.formatXml() }
        Button { text: "Копировать XML"; onClicked: nativeBridge.copyXml() }
        Button { text: "Проверить"; onClicked: nativeBridge.validateXml() }
    }
}

