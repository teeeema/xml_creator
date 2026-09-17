import QtQuick
import QtQuick.Controls

Button {
    id: control
    property bool primary: false
    property bool compact: false
    implicitHeight: compact ? 32 : 38
    implicitWidth: contentItem.implicitWidth + 28
    hoverEnabled: true
    contentItem: Text { text: control.text; color: control.primary ? "white" : Theme.text; font: control.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter; elide: Text.ElideRight }
    background: Rectangle {
        radius: 6
        color: control.primary ? (control.down ? "#0867db" : control.hovered ? "#2684f5" : Theme.accent) : (control.down ? "#eef2f6" : control.hovered ? "#f6f8fb" : Theme.surface)
        border.color: control.primary ? "transparent" : (control.activeFocus ? Theme.accent : Theme.border)
        border.width: 1
        opacity: control.enabled ? 1 : 0.55
    }
}
