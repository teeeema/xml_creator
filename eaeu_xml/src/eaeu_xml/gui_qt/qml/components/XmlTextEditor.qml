import QtQuick
import QtQuick.Controls

Item {
    id: root

    property string editorObjectName: "xmlEditor"
    property string viewportObjectName: "xmlEditorViewport"
    property int fontSize: 14
    property bool updatingFromModel: false
    property bool syncPending: false
    property int syncInterval: 300
    property alias text: editor.text
    property alias canUndo: editor.canUndo
    property alias canRedo: editor.canRedo
    property alias cursorPosition: editor.cursorPosition

    signal textCommitted(string text)
    signal zoomRequested(int delta)
    signal zoomResetRequested()

    function setTextFromModel(value) {
        updatingFromModel = true
        editor.text = value
        updatingFromModel = false
        syncPending = false
        syncTimer.stop()
    }

    function flush() {
        if (!syncPending)
            return
        textCommitted(editor.text)
        syncPending = false
        syncTimer.stop()
    }

    function undo() { editor.undo() }
    function redo() { editor.redo() }
    function selectRangeAndReveal(start, end) {
        editor.cursorPosition = start
        editor.select(start, end)
        const lineHeight = editor.font.pixelSize * 1.35
        const line = editor.text.slice(0, start).split("\n").length - 1
        viewport.contentY = Math.max(0, line * lineHeight - viewport.height / 2)
    }

    Flickable {
        id: viewport
        objectName: root.viewportObjectName
        anchors.fill: parent
        clip: true
        interactive: true
        boundsBehavior: Flickable.StopAtBounds
        contentWidth: Math.max(width, editor.implicitWidth)
        contentHeight: Math.max(height, editor.implicitHeight)

        // The viewport itself is anchored and never resizes with the document.
        // Only the Flickable content metrics change after an edit or zoom.
        TextArea {
            id: editor
            objectName: root.editorObjectName
            width: Math.max(viewport.width, implicitWidth)
            height: Math.max(viewport.height, implicitHeight)
            wrapMode: TextArea.NoWrap
            textFormat: TextEdit.PlainText
            font.family: "monospace"
            font.pixelSize: root.fontSize
            color: Theme.text
            selectionColor: Theme.accent
            selectedTextColor: "white"
            background: Rectangle { color: "#fbfcff"; border.color: Theme.border; radius: 5 }

            onTextChanged: {
                if (root.updatingFromModel)
                    return
                root.syncPending = true
                syncTimer.restart()
            }
            Keys.onPressed: event => {
                const modifier = (event.modifiers & Qt.ControlModifier) || (event.modifiers & Qt.MetaModifier)
                if (!modifier)
                    return
                if (event.key === Qt.Key_Plus || event.key === Qt.Key_Equal) {
                    root.zoomRequested(1)
                    event.accepted = true
                } else if (event.key === Qt.Key_Minus) {
                    root.zoomRequested(-1)
                    event.accepted = true
                } else if (event.key === Qt.Key_0) {
                    root.zoomResetRequested()
                    event.accepted = true
                }
            }
        }

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AsNeeded
            interactive: true
        }
        ScrollBar.horizontal: ScrollBar {
            policy: ScrollBar.AsNeeded
            interactive: true
        }

        onMovementEnded: {
            if (root.syncPending)
                syncTimer.restart()
        }
    }

    Timer {
        id: syncTimer
        interval: root.syncInterval
        repeat: false
        onTriggered: {
            // A Python update can be expensive for a large paste.  Never do it
            // in the middle of native flick/trackpad scrolling; it is flushed
            // as soon as the interaction ends or immediately by page actions.
            if (viewport.moving || viewport.dragging)
                return
            root.flush()
        }
    }
}
