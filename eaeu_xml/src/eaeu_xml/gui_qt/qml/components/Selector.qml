import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
ColumnLayout { id: root; property string title: ""; property var items: []; property string code: ""; signal chosen(string value); spacing: 3
    Label { text: root.title; color: Theme.secondary; font.pixelSize: 11 }
    AppComboBox { id: box; Layout.fillWidth: true; model: root.items; textRole: "label"; valueRole: "code"; currentIndex: indexOfValue(root.code); ToolTip.visible: hovered; ToolTip.text: currentText; onActivated: root.chosen(currentValue) }
}
