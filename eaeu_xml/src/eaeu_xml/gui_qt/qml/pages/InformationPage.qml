import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
Item { id: root; property int selected: 0
    RowLayout { anchors.fill: parent; spacing: 12
        Card { Layout.preferredWidth: 220; Layout.fillHeight: true
            ListView { anchors.fill: parent; anchors.margins: 8; model: viewModel.information; clip: true
                delegate: Button { required property int index; required property var modelData; width: ListView.view.width; text: modelData.section; flat: true; onClicked: root.selected = index; background: Rectangle { color: root.selected === index ? Theme.accentSoft : "transparent"; radius: 4 } }
            }
        }
        Card { Layout.fillWidth: true; Layout.fillHeight: true
            ColumnLayout { anchors.fill: parent; anchors.margins: 20; spacing: 12
                Label { text: viewModel.information.length ? viewModel.information[root.selected].section : "Информация"; font.bold: true; font.pixelSize: 17 }
                ScrollView { Layout.fillWidth: true; Layout.fillHeight: true
                    TextArea { text: viewModel.information.length ? viewModel.information[root.selected].text : ""; readOnly: true; wrapMode: TextArea.Wrap; background: null }
                }
            }
        }
    }
}
