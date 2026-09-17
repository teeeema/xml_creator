import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
Item { RowLayout { anchors.fill: parent; spacing: 12
    Card { Layout.fillWidth: true; Layout.fillHeight: true
        ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 12
            Label { text: "Результат проверки"; color: Theme.text; font.bold: true; font.pixelSize: 17 }
            Label { text: (viewModel ? viewModel.validationSummary : ""); color: (viewModel ? viewModel.validationItems : []).length === 0 ? Theme.success : Theme.error }
            RowLayout {
                AppButton { text: "Все (" + (viewModel ? viewModel.validationItems : []).length + ")"; compact: true }
                AppButton { text: "Ошибки"; compact: true }
                AppButton { text: "Предупреждения"; compact: true }
                AppButton { text: "Информационные (0)"; compact: true }
            }
            ListView { Layout.fillWidth: true; Layout.fillHeight: true; model: (viewModel ? viewModel.validationItems : []); clip: true
                delegate: RowLayout { width: ListView.view.width; height: 34; spacing: 12
                    Label { text: modelData.severity; Layout.preferredWidth: 110; color: modelData.severity === "ERROR" ? Theme.error : Theme.warning }
                    Label { text: modelData.code + ": " + modelData.message; Layout.fillWidth: true; elide: Text.ElideRight }
                    Label { text: modelData.location; Layout.preferredWidth: 220; color: Theme.text; elide: Text.ElideRight }
                }
            }
        }
    }
    Card { Layout.preferredWidth: 280; Layout.fillHeight: true
        ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 12
            Label { text: "Информация о проверке"; color: Theme.text; font.bold: true; font.pixelSize: 17 }
            Label { text: (viewModel ? viewModel.messageCode : ""); color: Theme.text }
            Label { text: "Режим проверки"; color: Theme.text }
            AppComboBox { model: ["TEST", "STRICT"]; Component.onCompleted: currentIndex = find((viewModel ? viewModel.validationMode : "TEST")); onActivated: viewModel.setValidationMode(currentText); Layout.fillWidth: true }
            Label { text: (viewModel ? viewModel.validationSummary : ""); wrapMode: Text.Wrap; Layout.fillWidth: true }
            Item { Layout.fillHeight: true }
            AppButton { text: "Проверить"; primary: true; Layout.fillWidth: true; onClicked: viewModel.validate() }
        }
    }
} }
