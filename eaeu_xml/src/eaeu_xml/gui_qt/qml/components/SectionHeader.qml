import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    property string title: ""; property int level: 0; property bool expanded: true
    signal toggled()
    height: 38; radius: 6; color: Theme.sectionBackground; border.color: Theme.border
    Text { anchors.left: parent.left; anchors.leftMargin: 12 + root.level * 12; anchors.verticalCenter: parent.verticalCenter; text: (root.expanded ? "⌄" : "›") + "  " + root.title; color: Theme.text; font.bold: true }
    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: root.toggled() }
}
