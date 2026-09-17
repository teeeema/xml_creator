import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
Item { id: root; property int selected: 0
    RowLayout { anchors.fill: parent; spacing: 12
        Card { Layout.preferredWidth: 220; Layout.fillHeight: true
            ListView { anchors.fill: parent; anchors.margins: 8; model: viewModel ? viewModel.information : []; clip: true
                delegate: AppButton {
                    required property int index
                    required property var modelData
                    width: ListView.view.width; text: modelData.section; compact: true
                    onClicked: root.selected = index
                    contentItem: Text { text: parent.text; color: root.selected === index ? Theme.accent : Theme.text; verticalAlignment: Text.AlignVCenter; leftPadding: 8; elide: Text.ElideRight }
                    background: Rectangle { color: root.selected === index ? Theme.accentSoft : "transparent"; radius: 4 }
                }
            }
        }
        Card { Layout.fillWidth: true; Layout.fillHeight: true
            ColumnLayout { anchors.fill: parent; anchors.margins: 20; spacing: 12
                Label { text: viewModel && viewModel.information.length ? viewModel.information[root.selected].section : "Информация"; font.bold: true; font.pixelSize: 17 }
                ScrollView { Layout.fillWidth: true; Layout.fillHeight: true
                    TextArea { text: viewModel && viewModel.information.length ? viewModel.information[root.selected].text : ""; readOnly: true; color: Theme.text; wrapMode: TextArea.Wrap; background: null }
                }
            }
        }
    }
}
