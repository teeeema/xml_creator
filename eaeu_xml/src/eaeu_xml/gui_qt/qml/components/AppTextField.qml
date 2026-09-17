import QtQuick
import QtQuick.Controls

TextField {
    id: control
    implicitHeight: 40; color: Theme.text; placeholderTextColor: Theme.placeholder
    selectionColor: Theme.accent; selectedTextColor: "white"; leftPadding: 11; rightPadding: 11
    background: Rectangle { radius: 6; color: control.readOnly ? "#f8fafc" : Theme.surface; border.width: control.activeFocus ? 1.5 : 1; border.color: control.activeFocus ? Theme.accent : Theme.fieldBorder }
}
