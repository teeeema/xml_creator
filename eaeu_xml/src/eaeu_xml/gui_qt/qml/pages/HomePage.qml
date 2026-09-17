import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item { id: root; signal saveDraftRequested()
    RowLayout { anchors.fill: parent; spacing: 12
        Card { Layout.fillWidth: true; Layout.fillHeight: true
            ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 12
                Label { text: "Данные сообщения"; font.bold: true; font.pixelSize: 17 }
                ScrollView { Layout.fillWidth: true; Layout.fillHeight: true; clip: true
                    Column { width: parent.width; spacing: 6
                        Repeater { model: viewModel.fields
                            delegate: Column { required property var modelData; width: parent.width; spacing: 4
                                Rectangle {
                                    visible: modelData.kind === "GROUP"
                                    width: parent.width; height: groupLabel.implicitHeight + 18
                                    color: Theme.background; radius: 4
                                    Label { id: groupLabel; anchors.verticalCenter: parent.verticalCenter; anchors.left: parent.left; anchors.leftMargin: 9
                                        text: (modelData.level > 0 ? "    " : "") + "⌄  " + modelData.label; font.bold: true }
                                }
                                RowLayout { visible: modelData.kind !== "GROUP"; width: parent.width; spacing: 8
                                    Label { text: modelData.label; Layout.preferredWidth: 210; wrapMode: Text.Wrap; color: Theme.secondary }
                                    TextField { visible: modelData.kind === "TEXT"; text: modelData.value; placeholderText: modelData.placeholder || ""; readOnly: modelData.readOnly; Layout.fillWidth: true; onEditingFinished: viewModel.setFieldValue(modelData.path, text); onActiveFocusChanged: if (activeFocus) viewModel.selectField(modelData.path) }
                                    ComboBox { visible: modelData.kind === "SELECT"; model: modelData.choices; Layout.fillWidth: true; Component.onCompleted: currentIndex = find(modelData.value); onActivated: viewModel.setFieldValue(modelData.path, currentText); onHighlighted: viewModel.selectField(modelData.path) }
                                    ComboBox { visible: modelData.kind === "BOOLEAN"; model: ["", "true", "false"]; Layout.fillWidth: true; Component.onCompleted: currentIndex = find(modelData.value); onActivated: viewModel.setFieldValue(modelData.path, currentText); onHighlighted: viewModel.selectField(modelData.path) }
                                }
                            }
                        }
                    }
                }
                RowLayout { Layout.fillWidth: true
                    Button { text: "Тестовые данные"; onClicked: viewModel.applyTestData() }
                    Item { Layout.fillWidth: true }
                    Button { text: "Сохранить черновик"; onClicked: root.saveDraftRequested() }
                    Button { text: "Создать XML"; highlighted: true; onClicked: viewModel.generateXml() }
                }
            }
        }
        Card { Layout.preferredWidth: 300; Layout.fillHeight: true
            ColumnLayout { anchors.fill: parent; anchors.margins: 16; spacing: 10
                Label { text: "Сведения о поле"; font.bold: true; font.pixelSize: 17 }
                TextArea { text: viewModel.selectedFieldInfo; readOnly: true; wrapMode: TextArea.Wrap; background: null; Layout.fillWidth: true; Layout.fillHeight: true }
            }
        }
    }
}
