import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Card { implicitHeight: 76
    RowLayout { anchors.fill: parent; anchors.margins: 12; spacing: 12
        Selector { Layout.fillWidth: true; title: "Процесс"; items: viewModel.processes; code: viewModel.processCode; onChosen: value => viewModel.selectProcess(value) }
        Label { text: "›"; color: Theme.secondary }
        Selector { Layout.fillWidth: true; title: "Транзакция"; items: viewModel.transactions; code: viewModel.transactionCode; onChosen: value => viewModel.selectTransaction(value) }
        Label { text: "›"; color: Theme.secondary }
        Selector { Layout.fillWidth: true; title: "Сообщение"; items: viewModel.messages; code: viewModel.messageCode; onChosen: value => viewModel.selectMessage(value) }
    }
}
