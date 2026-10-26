import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item { id: root; signal saveDraftRequested()
    RowLayout { anchors.fill: parent; spacing: 12
        Card { Layout.fillWidth: true; Layout.fillHeight: true
            ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 12
                Label { text: "Данные сообщения"; color: Theme.text; font.bold: true; font.pixelSize: 17 }
                ScrollView { Layout.fillWidth: true; Layout.fillHeight: true; clip: true
                    Column { width: parent.width; spacing: 6
                        Repeater { model: (viewModel ? viewModel.fields : [])
                            delegate: Column { required property var modelData; width: parent.width; spacing: 4
                                SectionHeader {
                                    visible: modelData.kind === "GROUP"
                                    width: parent.width; title: modelData.label; level: modelData.level
                                    onSelected: viewModel.selectField(modelData.path)
                                }
                                RowLayout { visible: modelData.kind !== "GROUP"; width: parent.width; spacing: 8
                                    Label { text: modelData.label + (modelData.required ? " *" : "") + (modelData.conditional ? " (условно)" : ""); Layout.preferredWidth: 210; wrapMode: Text.Wrap; color: Theme.text }
                                    AppTextField { visible: modelData.kind === "TEXT"; text: modelData.value; placeholderText: modelData.placeholder || ""; readOnly: modelData.readOnly; Layout.fillWidth: true; onEditingFinished: viewModel.setFieldValue(modelData.path, text); onActiveFocusChanged: if (activeFocus) viewModel.selectField(modelData.path) }
                                    AppComboBox { visible: modelData.kind === "SELECT"; model: modelData.choices; Layout.fillWidth: true; Component.onCompleted: currentIndex = find(modelData.value); onActivated: viewModel.setFieldValue(modelData.path, currentText); onHighlighted: viewModel.selectField(modelData.path) }
                                    AppComboBox { visible: modelData.kind === "BOOLEAN"; model: ["", "true", "false"]; Layout.fillWidth: true; Component.onCompleted: currentIndex = find(modelData.value); onActivated: viewModel.setFieldValue(modelData.path, currentText); onHighlighted: viewModel.selectField(modelData.path) }
                                }
                            }
                        }
                    }
                }
                RowLayout { Layout.fillWidth: true
                    AppButton { text: "Тестовые данные"; onClicked: viewModel.applyTestData() }
                    Item { Layout.fillWidth: true }
                    AppButton { text: "Сохранить черновик"; onClicked: root.saveDraftRequested() }
                    AppButton { text: "Создать XML"; primary: true; onClicked: viewModel.generateXml() }
                }
            }
        }
        Card { Layout.preferredWidth: 300; Layout.fillHeight: true
            ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 10
                Label { text: "Сведения о поле"; color: Theme.text; font.bold: true; font.pixelSize: 17 }
                ScrollView {
                    id: fieldInfoScroll
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    Column {
                        width: fieldInfoScroll.availableWidth
                        spacing: 14

                        Label {
                            visible: viewModel && viewModel.fieldInfoDetailedEnabled && !viewModel.fieldInfoDetailedHasSelection
                            width: fieldInfoScroll.availableWidth
                            text: "Выберите поле, чтобы посмотреть его нормативное описание."
                            color: Theme.text
                            wrapMode: Text.Wrap
                        }

                        Column {
                            visible: viewModel && viewModel.fieldInfoDetailedEnabled && viewModel.fieldInfoDetailedHasSelection
                            width: fieldInfoScroll.availableWidth
                            spacing: 14

                            Column {
                                width: parent.width; spacing: 4
                                Label { width: parent.width; text: "Имя реквизита"; color: Theme.text; font.weight: Font.DemiBold }
                                Label { width: parent.width; text: viewModel ? viewModel.selectedFieldDetails.name : ""; textFormat: Text.PlainText; color: Theme.text; wrapMode: Text.Wrap }
                            }
                            Column {
                                width: parent.width; spacing: 4
                                Label { width: parent.width; text: "Описание реквизита"; color: Theme.text; font.weight: Font.DemiBold }
                                Label {
                                    width: parent.width
                                    text: viewModel ? viewModel.selectedFieldDetails.description : ""
                                    textFormat: Text.PlainText
                                    color: Theme.text
                                    wrapMode: Text.Wrap
                                }
                            }
                            Column {
                                width: parent.width; spacing: 4
                                Label { width: parent.width; text: "Тип данных"; color: Theme.text; font.weight: Font.DemiBold }
                                Label { width: parent.width; text: viewModel ? viewModel.selectedFieldDetails.datatype : ""; textFormat: Text.PlainText; color: Theme.text; wrapMode: Text.Wrap }
                            }
                            Column {
                                width: parent.width; spacing: 4
                                Label { width: parent.width; text: "Множитель"; color: Theme.text; font.weight: Font.DemiBold }
                                Label { width: parent.width; text: viewModel ? viewModel.selectedFieldDetails.multiplicity : ""; textFormat: Text.PlainText; color: Theme.text; wrapMode: Text.Wrap }
                            }
                            Column {
                                visible: viewModel && viewModel.selectedFieldDetails.constraints && viewModel.selectedFieldDetails.constraints.length > 0
                                width: parent.width; spacing: 4
                                Label { width: parent.width; text: "Ограничения"; color: Theme.text; font.weight: Font.DemiBold }
                                Repeater {
                                    model: viewModel ? viewModel.selectedFieldDetails.constraints : []
                                    delegate: Label {
                                        required property var modelData
                                        width: parent.width
                                        text: modelData.label + ": " + modelData.value
                                        textFormat: Text.PlainText
                                        color: Theme.text
                                        wrapMode: Text.Wrap
                                    }
                                }
                            }
                            Column {
                                visible: viewModel && viewModel.selectedFieldDetails.policy
                                width: parent.width; spacing: 4
                                Label { width: parent.width; text: "Правило заполнения для текущего сообщения"; color: Theme.text; font.weight: Font.DemiBold; wrapMode: Text.Wrap }
                                Label { width: parent.width; text: viewModel ? viewModel.selectedFieldDetails.policy : ""; color: Theme.text; wrapMode: Text.Wrap; textFormat: Text.PlainText }
                            }
                        }

                        TextArea {
                            visible: !viewModel || !viewModel.fieldInfoDetailedEnabled
                            text: (viewModel ? viewModel.selectedFieldInfo : "")
                            color: Theme.text
                            readOnly: true
                            wrapMode: TextArea.Wrap
                            background: null
                            width: fieldInfoScroll.availableWidth
                        }
                    }
                }
            }
        }
    }
}
