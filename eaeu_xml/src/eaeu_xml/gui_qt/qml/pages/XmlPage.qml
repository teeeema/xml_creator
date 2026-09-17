import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
Item { id: root; signal saveXmlRequested()
    Card { anchors.fill: parent
        ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 12
            RowLayout { Layout.fillWidth: true
                Label { text: "Сформированный XML"; font.bold: true; font.pixelSize: 17; Layout.fillWidth: true }
                Button { text: "Форматировать"; onClicked: viewModel.formatXml() }
                Button { text: "Копировать"; onClicked: { xml.selectAll(); xml.copy() } }
                Button { text: "Скачать XML"; onClicked: root.saveXmlRequested() }
            }
            TextArea {
                id: xml; text: viewModel.xml; readOnly: true; wrapMode: TextArea.NoWrap
                font.family: "monospace"; font.pixelSize: 13
                Layout.fillWidth: true; Layout.fillHeight: true
                background: Rectangle { color: "#fbfcff"; border.color: Theme.border; radius: 5 }
            }
        }
    }
}
