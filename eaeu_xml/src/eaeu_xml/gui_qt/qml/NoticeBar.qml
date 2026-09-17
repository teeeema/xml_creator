import QtQuick
import QtQuick.Controls
import "components"

Rectangle {
    color: Theme.background
    Label {
        anchors.fill: parent
        text: viewModel ? viewModel.notice : ""
        color: Theme.secondary
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
}
