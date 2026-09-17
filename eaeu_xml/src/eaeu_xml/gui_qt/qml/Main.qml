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
    palette.text: Theme.text
    palette.windowText: Theme.text
    FileDialog { id: xmlDialog; title: "Сохранить XML"; fileMode: FileDialog.SaveFile; nameFilters: ["XML (*.xml)"]; onAccepted: viewModel.saveXml(selectedFile.toLocalFile()) }
    FileDialog { id: formatterOpenDialog; title: "Открыть XML"; fileMode: FileDialog.OpenFile; nameFilters: ["XML (*.xml)"]; onAccepted: viewModel.loadFormatterXml(selectedFile.toLocalFile()) }
    FileDialog { id: formatterSaveDialog; title: "Сохранить XML"; fileMode: FileDialog.SaveFile; nameFilters: ["XML (*.xml)"]; onAccepted: viewModel.saveFormatterXml(selectedFile.toLocalFile()) }
    FileDialog { id: draftDialog; title: "Сохранить черновик"; fileMode: FileDialog.SaveFile; nameFilters: ["Черновик (*.eaeudraft.json)"]; onAccepted: viewModel.saveDraft(selectedFile.toLocalFile()) }
    ColumnLayout {
        anchors.fill: parent; anchors.margins: 24; spacing: 12
        TopNavigation { Layout.fillWidth: true; currentIndex: pages.currentIndex; onSelected: index => pages.currentIndex = index }
        SelectorBar { Layout.fillWidth: true; visible: pages.currentIndex === 0 }
        StackLayout {
            id: pages; Layout.fillWidth: true; Layout.fillHeight: true
            HomePage { onSaveDraftRequested: draftDialog.open() }
            XmlPage { onSaveXmlRequested: xmlDialog.open() }
            ValidationPage { }
            XmlFormatterPage { onOpenRequested: formatterOpenDialog.open(); onSaveRequested: formatterSaveDialog.open() }
            InformationPage { }
            SettingsPage { }
        }
        Label { visible: (viewModel ? viewModel.notice : "") !== ""; text: (viewModel ? viewModel.notice : ""); color: Theme.secondary; Layout.fillWidth: true }
    }
}
