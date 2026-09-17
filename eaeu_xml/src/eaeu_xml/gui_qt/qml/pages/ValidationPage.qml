import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
Item { RowLayout { anchors.fill: parent; spacing: 12
    Card { Layout.fillWidth: true; Layout.fillHeight: true
        ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 12
            Label { text: "Результат проверки"; font.bold: true; font.pixelSize: 17 }
            Label { text: viewModel.validationSummary; color: viewModel.validationItems.length === 0 ? Theme.success : Theme.error }
            RowLayout {
                Button { text: "Все (" + viewModel.validationItems.length + ")" }
                Button { text: "Ошибки" }
                Button { text: "Предупреждения" }
                Button { text: "Информационные (0)" }
            }
            ListView { Layout.fillWidth: true; Layout.fillHeight: true; model: viewModel.validationItems; clip: true
                delegate: RowLayout { width: ListView.view.width; height: 34; spacing: 12
                    Label { text: modelData.severity; Layout.preferredWidth: 110; color: modelData.severity === "ERROR" ? Theme.error : Theme.warning }
                    Label { text: modelData.code + ": " + modelData.message; Layout.fillWidth: true; elide: Text.ElideRight }
                    Label { text: modelData.location; Layout.preferredWidth: 220; color: Theme.secondary; elide: Text.ElideRight }
                }
            }
        }
    }
    Card { Layout.preferredWidth: 280; Layout.fillHeight: true
        ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 12
            Label { text: "Информация о проверке"; font.bold: true; font.pixelSize: 17 }
            Label { text: viewModel.messageCode; color: Theme.secondary }
            Label { text: "Режим проверки"; color: Theme.secondary }
            ComboBox { model: ["TEST", "STRICT"]; Component.onCompleted: currentIndex = find(viewModel.validationMode); onActivated: viewModel.setValidationMode(currentText); Layout.fillWidth: true }
            Label { text: viewModel.validationSummary; wrapMode: Text.Wrap; Layout.fillWidth: true }
            Item { Layout.fillHeight: true }
            Button { text: "Проверить"; highlighted: true; Layout.fillWidth: true; onClicked: viewModel.validate() }
        }
    }
} }
