import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Card { implicitHeight: 172
    ColumnLayout { anchors.fill: parent; anchors.margins: 12; spacing: 8
        Selector { Layout.fillWidth: true; title: "Процесс"; items: (viewModel ? viewModel.processes : []); code: (viewModel ? viewModel.processCode : ""); onChosen: value => viewModel.selectProcess(value) }
        Selector { Layout.fillWidth: true; title: "Транзакция"; items: (viewModel ? viewModel.transactions : []); code: (viewModel ? viewModel.transactionCode : ""); onChosen: value => viewModel.selectTransaction(value) }
        Selector { Layout.fillWidth: true; title: "Сообщение"; items: (viewModel ? viewModel.messages : []); code: (viewModel ? viewModel.messageCode : ""); onChosen: value => viewModel.selectMessage(value) }
    }
}
