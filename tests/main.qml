import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: "Hello QML with PySide6"
    flags: Qt.Window | Qt.FramelessWindowHint

    Rectangle {
        anchors.fill: parent
        color: "#f0f0f0"

        Text {
            id: helloText
            text: backend.message
            anchors.centerIn: parent
            font.pixelSize: 24
        }

        Button {
            text: "Change Message"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: helloText.bottom
            anchors.topMargin: 20
            onClicked: {
                backend.message = "Message Changed from QML!"
            }
        }
    }

    DragHandler {
        id: resizeHandler
        grabPermissions: TapHandler.TakeOverForbidden
        target: null
        onActiveChanged: if (active) {
            const p = resizeHandler.centroid.position;
            let e = 0;
            if (p.x < border) e |= Qt.LeftEdge;
            if (p.x >= width - border) e |= Qt.RightEdge;
            if (p.y < border) e |= Qt.TopEdge;
            if (p.y >= height - border) e |= Qt.BottomEdge;
            window.startSystemResize(e);
        }
    }
}
