import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
Item { Card { anchors.fill: parent; width: Math.min(parent.width, 560)
    ColumnLayout { anchors.fill: parent; anchors.margins: 20; spacing: 12
        Label { text: "Настройки"; font.bold: true; font.pixelSize: 17 }
        Label { text: "Режим генерации"; color: Theme.secondary }
        ComboBox { model: ["TEST", "STRICT"]; Component.onCompleted: currentIndex = find(viewModel.validationMode); onActivated: viewModel.setValidationMode(currentText); Layout.preferredWidth: 220 }
        Item { Layout.fillHeight: true }
    }
} }
