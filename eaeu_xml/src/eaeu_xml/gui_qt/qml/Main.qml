import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "components"
import "pages"

ApplicationWindow {
    id: window
    visible: true
    width: 1440; height: 900
    minimumWidth: 980; minimumHeight: 640
    title: "ГИС_xml"
    color: Theme.background
    FileDialog { id: xmlDialog; title: "Сохранить XML"; fileMode: FileDialog.SaveFile; nameFilters: ["XML (*.xml)"]; onAccepted: viewModel.saveXml(selectedFile.toLocalFile()) }
    FileDialog { id: draftDialog; title: "Сохранить черновик"; fileMode: FileDialog.SaveFile; nameFilters: ["Черновик (*.eaeudraft.json)"]; onAccepted: viewModel.saveDraft(selectedFile.toLocalFile()) }
    ColumnLayout {
        anchors.fill: parent; anchors.margins: 24; spacing: 12
        TopNavigation { Layout.fillWidth: true; currentIndex: pages.currentIndex; onSelected: index => pages.currentIndex = index }
        SelectorBar { Layout.fillWidth: true }
        StackLayout {
            id: pages; Layout.fillWidth: true; Layout.fillHeight: true
            HomePage { onSaveDraftRequested: draftDialog.open() }
            XmlPage { onSaveXmlRequested: xmlDialog.open() }
            ValidationPage { }
            InformationPage { }
            SettingsPage { }
        }
        Label { visible: viewModel.notice !== ""; text: viewModel.notice; color: Theme.secondary; Layout.fillWidth: true }
    }
}
