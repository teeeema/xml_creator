import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
Item {
    id: root
    property string validationFilter: "ALL"
    property var diagnostics: viewModel ? viewModel.validationItems : []
    property var filteredDiagnostics: diagnostics.filter(item => validationFilter === "ALL" || item.severity === validationFilter)
    function count(severity) { return severity === "ALL" ? diagnostics.length : diagnostics.filter(item => item.severity === severity).length }
    function filterButton(label, severity) { return label + " (" + count(severity) + ")" }
    function emptyText() {
        if (validationFilter === "ERROR") return "Ошибок нет."
        if (validationFilter === "WARNING") return "Предупреждений нет."
        if (validationFilter === "INFO") return "Информационных сообщений нет."
        return "Результатов проверки нет."
    }
    RowLayout { anchors.fill: parent; spacing: 12
    Card { Layout.fillWidth: true; Layout.fillHeight: true
        ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 12
            Label { text: "Результат проверки"; color: Theme.text; font.bold: true; font.pixelSize: 17 }
            Label { text: (viewModel ? viewModel.validationSummary : ""); color: (viewModel ? viewModel.validationItems : []).length === 0 ? Theme.success : Theme.error }
            RowLayout {
                AppButton { objectName: "validationAll"; text: root.filterButton("Все", "ALL"); compact: true; primary: root.validationFilter === "ALL"; onClicked: root.validationFilter = "ALL" }
                AppButton { objectName: "validationErrors"; text: root.filterButton("Ошибки", "ERROR"); compact: true; primary: root.validationFilter === "ERROR"; onClicked: root.validationFilter = "ERROR" }
                AppButton { objectName: "validationWarnings"; text: root.filterButton("Предупреждения", "WARNING"); compact: true; primary: root.validationFilter === "WARNING"; onClicked: root.validationFilter = "WARNING" }
                AppButton { objectName: "validationInfos"; text: root.filterButton("Информационные", "INFO"); compact: true; primary: root.validationFilter === "INFO"; onClicked: root.validationFilter = "INFO" }
            }
            ListView { id: diagnosticList; objectName: "validationDiagnosticList"; Layout.fillWidth: true; Layout.fillHeight: true; model: root.filteredDiagnostics; clip: true
                delegate: Rectangle { width: ListView.view.width; height: 34; radius: 4; color: mouse.containsMouse && modelData.line > 0 ? Theme.accentSoft : "transparent"
                    RowLayout { anchors.fill: parent; anchors.leftMargin: 6; anchors.rightMargin: 6; spacing: 12
                    Label { text: modelData.severity; Layout.preferredWidth: 110; color: modelData.severity === "ERROR" ? Theme.error : Theme.warning }
                    Label { text: modelData.code + ": " + modelData.message; Layout.fillWidth: true; elide: Text.ElideRight }
                    Label { text: modelData.location; Layout.preferredWidth: 220; color: Theme.text; elide: Text.ElideRight }
                    }
                    MouseArea { id: mouse; anchors.fill: parent; hoverEnabled: modelData.line > 0; cursorShape: modelData.line > 0 ? Qt.PointingHandCursor : Qt.ArrowCursor; onClicked: if (modelData.line > 0) viewModel.goToXmlDiagnostic(modelData.line, modelData.column) }
                }
            }
            Label { objectName: "validationEmpty"; visible: root.filteredDiagnostics.length === 0; text: root.emptyText(); color: Theme.secondary; Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter }
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
