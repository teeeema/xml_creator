import QtQuick
import QtQuick.Controls

ComboBox {
    id: control
    implicitHeight: 40; leftPadding: 11; rightPadding: 34
    contentItem: Text { leftPadding: control.leftPadding; rightPadding: control.rightPadding; text: control.displayText; color: Theme.text; font: control.font; verticalAlignment: Text.AlignVCenter; elide: Text.ElideRight }
    indicator: Canvas { x: control.width - width - 12; y: (control.height - height) / 2; width: 10; height: 6; contextType: "2d"; onPaint: { const ctx = getContext("2d"); ctx.reset(); ctx.fillStyle = Theme.secondary; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(width, 0); ctx.lineTo(width / 2, height); ctx.closePath(); ctx.fill() } }
    background: Rectangle { radius: 6; color: Theme.surface; border.width: control.activeFocus ? 1.5 : 1; border.color: control.activeFocus ? Theme.accent : Theme.fieldBorder }
    delegate: ItemDelegate {
        width: control.width; height: 36
        contentItem: Text { text: modelData.label !== undefined ? modelData.label : modelData; color: Theme.text; verticalAlignment: Text.AlignVCenter; elide: Text.ElideRight }
        ToolTip.visible: hovered
        ToolTip.text: modelData.label !== undefined ? modelData.label : modelData
        background: Rectangle { color: highlighted ? Theme.accentSoft : Theme.surface }
    }
    popup: Popup {
        y: control.height + 4; width: control.width
        implicitHeight: Math.min(contentItem.implicitHeight + 8, 280); padding: 4
        contentItem: ListView { clip: true; implicitHeight: contentHeight; model: control.popup.visible ? control.delegateModel : null; currentIndex: control.highlightedIndex; ScrollIndicator.vertical: ScrollIndicator {} }
        background: Rectangle { color: Theme.surface; border.color: Theme.border; radius: 6 }
    }
}
