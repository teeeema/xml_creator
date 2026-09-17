import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
Item { Card { anchors.fill: parent; width: Math.min(parent.width, 560)
    ColumnLayout { anchors.fill: parent; anchors.margins: 20; spacing: 12
        Label { text: "Настройки"; color: Theme.text; font.bold: true; font.pixelSize: 17 }
        Label { text: "Режим генерации"; color: Theme.secondary }
        AppComboBox { model: ["TEST", "STRICT"]; Component.onCompleted: currentIndex = find((viewModel ? viewModel.validationMode : "TEST")); onActivated: viewModel.setValidationMode(currentText); Layout.preferredWidth: 220 }
        Item { Layout.fillHeight: true }
    }
} }
