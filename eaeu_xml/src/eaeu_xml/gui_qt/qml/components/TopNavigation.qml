import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Rectangle { id: root; property int currentIndex: 0; signal selected(int index); color: Theme.background
    RowLayout { anchors.fill: parent; spacing: 8
        Repeater { model: ["Главная", "XML", "Проверка", "Форматирование", "Base64", "Информация", "Настройки"]
            delegate: AppButton { required property int index; required property string modelData; text: modelData; compact: true; Layout.fillWidth: true; Layout.preferredHeight: 38; onClicked: root.selected(index)
                contentItem: Text { text: parent.text; color: root.currentIndex === index ? Theme.accent : Theme.text; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                background: Rectangle { color: "transparent"; Rectangle { visible: root.currentIndex === index; anchors.bottom: parent.bottom; width: parent.width; height: 2; color: Theme.accent } }
            }
        }
    }
}
