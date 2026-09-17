import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "components"
import "pages"

Rectangle {
    id: root
    color: Theme.background
    property int currentIndex: 0
    FileDialog { id: draftDialog; title: "Сохранить черновик"; fileMode: FileDialog.SaveFile; nameFilters: ["Черновик (*.eaeudraft.json)"]; onAccepted: viewModel.saveDraft(selectedFile.toLocalFile()) }
    ColumnLayout {
        anchors.fill: parent; spacing: 12
        SelectorBar { Layout.fillWidth: true; visible: root.currentIndex === 0 }
        StackLayout {
            id: pages; Layout.fillWidth: true; Layout.fillHeight: true; currentIndex: root.currentIndex
            HomePage { onSaveDraftRequested: draftDialog.open() }
            Item { }
            ValidationPage { }
            Item { }
            Base64Page { utilityModel: typeof base64Model === "undefined" ? null : base64Model }
            InformationPage { }
            SettingsPage { }
        }
    }
}
