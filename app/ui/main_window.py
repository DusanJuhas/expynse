from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QLineEdit
)

from app.parsing.rb_parser import parse_transactions
from app.services.transaction_service import insert_transactions, get_all_transactions
from app.services.search_service import search_transactions


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("expynse")

        layout = QVBoxLayout()

        self.import_btn = QPushButton("Import PDF")
        self.import_btn.clicked.connect(self.import_pdf)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self.search)

        self.table = QTableWidget()

        layout.addWidget(self.import_btn)
        layout.addWidget(self.search_input)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_data()

    def import_pdf(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if file:
            txs = parse_transactions(file)
            insert_transactions(txs)
            self.load_data()

    def load_data(self):
        rows = get_all_transactions()
        self.populate_table(rows)

    def search(self):
        query = self.search_input.text()
        if not query:
            self.load_data()
        else:
            rows = search_transactions(query)
            self.populate_table(rows)

    def populate_table(self, rows):
        headers = ["date", "amount", "description", "user_category", "transaction_type", "counter_name"]

        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(rows))
        self.table.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(rows):
            for j, col in enumerate(headers):
                self.table.setItem(i, j, QTableWidgetItem(str(row[col])))