"""
Ledger module for viewing and managing customer ledgers
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QDialog, QLineEdit, QDateEdit, QDoubleSpinBox,
                             QMessageBox, QHeaderView, QComboBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from database import Database

class LedgerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.current_customer_id = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Ledger")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Customer selector
        customer_label = QLabel("Customer:")
        header_layout.addWidget(customer_label)
        self.customer_combo = QComboBox()
        self.customer_combo.currentIndexChanged.connect(self.on_customer_changed)
        header_layout.addWidget(self.customer_combo)
        
        layout.addLayout(header_layout)
        
        # Customer info and balance
        info_frame = QWidget()
        info_frame.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        info_layout = QHBoxLayout()
        
        self.customer_name_label = QLabel("Select a customer to view ledger")
        self.customer_name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        info_layout.addWidget(self.customer_name_label)
        
        info_layout.addStretch()
        
        self.balance_label = QLabel("Current Balance: Rs. 0.00")
        self.balance_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #27ae60;")
        info_layout.addWidget(self.balance_label)
        
        info_frame.setLayout(info_layout)
        layout.addWidget(info_frame)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        add_credit_btn = QPushButton("Add Credit (Sale)")
        add_credit_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        add_credit_btn.clicked.connect(lambda: self.show_add_entry_dialog("Credit"))
        button_layout.addWidget(add_credit_btn)
        
        add_payment_btn = QPushButton("Add Payment (Debit)")
        add_payment_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        add_payment_btn.clicked.connect(lambda: self.show_add_entry_dialog("Debit"))
        button_layout.addWidget(add_payment_btn)
        
        button_layout.addStretch()
        
        # Export buttons
        export_pdf_btn = QPushButton("Export to PDF")
        export_pdf_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
        """)
        export_pdf_btn.clicked.connect(self.export_to_pdf)
        button_layout.addWidget(export_pdf_btn)
        
        export_excel_btn = QPushButton("Export to Excel")
        export_excel_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
        """)
        export_excel_btn.clicked.connect(self.export_to_excel)
        button_layout.addWidget(export_excel_btn)
        
        layout.addLayout(button_layout)
        
        # Date filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Start Date:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate(2023, 1, 1))
        self.start_date.setCalendarPopup(True)
        filter_layout.addWidget(self.start_date)
        
        filter_layout.addWidget(QLabel("End Date:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate(2023, 12, 31))
        self.end_date.setCalendarPopup(True)
        filter_layout.addWidget(self.end_date)
        
        apply_filter_btn = QPushButton("Apply Filter")
        apply_filter_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
        """)
        apply_filter_btn.clicked.connect(self.refresh_table)
        filter_layout.addWidget(apply_filter_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Ledger table
        self.ledger_table = QTableWidget()
        self.ledger_table.setColumnCount(5)
        self.ledger_table.setHorizontalHeaderLabels([
            "DATE", "DESCRIPTION", "CREDIT", "DEBIT", "BALANCE"
        ])
        self.ledger_table.horizontalHeader().setStretchLastSection(True)
        self.ledger_table.setAlternatingRowColors(True)
        layout.addWidget(self.ledger_table)
        
        self.setLayout(layout)
        
        # Load customers
        self.load_customers()
    
    def load_customers(self):
        """Load customers into combo box"""
        self.customer_combo.clear()
        customers = self.db.get_all_customers()
        for customer in customers:
            self.customer_combo.addItem(customer['name'], customer['id'])
    
    def set_customer(self, customer_id):
        """Set customer from external call"""
        index = self.customer_combo.findData(customer_id)
        if index >= 0:
            self.customer_combo.setCurrentIndex(index)
    
    def on_customer_changed(self):
        """Handle customer selection change"""
        customer_id = self.customer_combo.currentData()
        if customer_id:
            self.current_customer_id = customer_id
            customers = self.db.get_all_customers()
            customer = next((c for c in customers if c['id'] == customer_id), None)
            if customer:
                self.customer_name_label.setText(customer['name'])
            self.refresh_table()
        else:
            self.current_customer_id = None
            self.customer_name_label.setText("Select a customer to view ledger")
            self.balance_label.setText("Current Balance: Rs. 0.00")
            self.ledger_table.setRowCount(0)
    
    def refresh_table(self):
        """Refresh ledger table"""
        if not self.current_customer_id:
            return
        
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        
        entries = self.db.get_ledger_entries(self.current_customer_id, start_date, end_date)
        
        self.ledger_table.setRowCount(len(entries))
        for i, entry in enumerate(entries):
            self.ledger_table.setItem(i, 0, QTableWidgetItem(entry['date']))
            self.ledger_table.setItem(i, 1, QTableWidgetItem(entry['description']))
            
            credit_item = QTableWidgetItem(f"Rs. {entry['credit']:.2f}" if entry['credit'] > 0 else "")
            credit_item.setForeground(Qt.darkGreen)
            self.ledger_table.setItem(i, 2, credit_item)
            
            debit_item = QTableWidgetItem(f"Rs. {entry['debit']:.2f}" if entry['debit'] > 0 else "")
            debit_item.setForeground(Qt.red)
            self.ledger_table.setItem(i, 3, debit_item)
            
            balance_item = QTableWidgetItem(f"Rs. {entry['balance']:.2f}")
            if entry['balance'] < 0:
                balance_item.setForeground(Qt.red)
            self.ledger_table.setItem(i, 4, balance_item)
        
        # Update balance label
        balance = self.db.get_customer_balance(self.current_customer_id)
        self.balance_label.setText(f"Current Balance: Rs. {balance:,.2f}")
        if balance < 0:
            self.balance_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c;")
        else:
            self.balance_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #27ae60;")
        
        self.ledger_table.resizeColumnsToContents()
    
    def show_add_entry_dialog(self, entry_type):
        """Show dialog to add ledger entry"""
        if not self.current_customer_id:
            QMessageBox.warning(self, "Error", "Please select a customer first.")
            return
        
        dialog = AddLedgerEntryDialog(self, entry_type, self.current_customer_id)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_table()
    
    def export_to_pdf(self):
        """Export ledger to PDF"""
        if not self.current_customer_id:
            QMessageBox.warning(self, "Error", "Please select a customer first.")
            return
        
        QMessageBox.information(self, "Export", "PDF export functionality would be implemented here.")
    
    def export_to_excel(self):
        """Export ledger to Excel"""
        if not self.current_customer_id:
            QMessageBox.warning(self, "Error", "Please select a customer first.")
            return
        
        QMessageBox.information(self, "Export", "Excel export functionality would be implemented here.")
    
    def refresh_data(self):
        """Refresh all data"""
        self.load_customers()
        if self.current_customer_id:
            self.refresh_table()

class AddLedgerEntryDialog(QDialog):
    def __init__(self, parent, entry_type, customer_id):
        super().__init__(parent)
        self.db = Database()
        self.entry_type = entry_type
        self.customer_id = customer_id
        self.setWindowTitle(f"Add {entry_type}")
        self.setFixedSize(400, 250)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel(f"Add {self.entry_type} Entry")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Date
        date_layout = QHBoxLayout()
        date_label = QLabel("Date:")
        date_label.setFixedWidth(100)
        date_layout.addWidget(date_label)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        date_layout.addWidget(self.date_input)
        layout.addLayout(date_layout)
        
        # Description
        desc_layout = QHBoxLayout()
        desc_label = QLabel("Description:")
        desc_label.setFixedWidth(100)
        desc_layout.addWidget(desc_label)
        self.desc_input = QLineEdit()
        if self.entry_type == "Credit":
            self.desc_input.setPlaceholderText("e.g., Fuel Purchase - 50L")
        else:
            self.desc_input.setPlaceholderText("e.g., Payment Received")
        desc_layout.addWidget(self.desc_input)
        layout.addLayout(desc_layout)
        
        # Amount
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Amount:")
        amount_label.setFixedWidth(100)
        amount_layout.addWidget(amount_label)
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 999999)
        self.amount_input.setValue(0.0)
        amount_layout.addWidget(self.amount_input)
        layout.addLayout(amount_layout)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        add_btn = QPushButton(f"Add {self.entry_type}")
        add_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        add_btn.clicked.connect(self.add_entry)
        button_layout.addWidget(add_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def add_entry(self):
        """Add ledger entry"""
        date = self.date_input.date().toString("yyyy-MM-dd")
        description = self.desc_input.text().strip()
        amount = self.amount_input.value()
        
        if not description:
            QMessageBox.warning(self, "Error", "Please enter a description.")
            return
        
        if amount <= 0:
            QMessageBox.warning(self, "Error", "Amount must be greater than 0.")
            return
        
        credit = amount if self.entry_type == "Credit" else 0
        debit = amount if self.entry_type == "Debit" else 0
        
        success = self.db.add_ledger_entry(self.customer_id, date, description, credit, debit)
        if success:
            QMessageBox.information(self, "Success", f"{self.entry_type} entry added successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to add entry.")

