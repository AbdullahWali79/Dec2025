"""
Customers module for managing customers
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QDialog, QLineEdit, QComboBox, QTextEdit, QDoubleSpinBox,
                             QMessageBox, QHeaderView, QTabWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from database import Database

class CustomersWidget(QWidget):
    view_ledger_requested = pyqtSignal(int)  # Emits customer_id
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Customer Management")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        add_customer_btn = QPushButton("+ Add Customer")
        add_customer_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        add_customer_btn.clicked.connect(self.show_add_customer_dialog)
        header_layout.addWidget(add_customer_btn)
        
        layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                background: white;
            }
            QTabBar::tab {
                padding: 10px 20px;
                background: #f0f0f0;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #4A90E2;
            }
        """)
        
        # Regular Customers tab
        self.regular_table = self.create_customer_table()
        self.tabs.addTab(self.regular_table, "Regular Customers")
        
        # Distributors tab
        self.distributor_table = self.create_customer_table()
        self.tabs.addTab(self.distributor_table, "Distributors")
        
        self.tabs.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
    
    def create_customer_table(self):
        """Create customer table widget"""
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Customer Name", "Phone", "Type", "Outstanding Balance", "Action"
        ])
        table.horizontalHeader().setStretchLastSection(True)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        return table
    
    def on_tab_changed(self, index):
        """Handle tab change"""
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh customer tables"""
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:  # Regular Customers
            customers = self.db.get_all_customers("Regular")
            self.populate_table(self.regular_table, customers)
        else:  # Distributors
            customers = self.db.get_all_customers("Distributor")
            self.populate_table(self.distributor_table, customers)
    
    def populate_table(self, table, customers):
        """Populate table with customer data"""
        table.setRowCount(len(customers))
        
        for i, customer in enumerate(customers):
            table.setItem(i, 0, QTableWidgetItem(customer['name']))
            table.setItem(i, 1, QTableWidgetItem(customer['phone']))
            table.setItem(i, 2, QTableWidgetItem(customer['type']))
            
            balance = customer['outstanding_balance']
            balance_item = QTableWidgetItem(f"Rs. {balance:,.2f}")
            if balance < 0:
                balance_item.setForeground(Qt.red)
            elif balance > 0:
                balance_item.setForeground(Qt.darkGreen)
            table.setItem(i, 3, balance_item)
            
            # View Ledger button
            view_btn = QPushButton("View Ledger")
            view_btn.setStyleSheet("""
                QPushButton {
                    background: #4A90E2;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
            """)
            view_btn.clicked.connect(lambda checked, cid=customer['id']: self.view_ledger(cid))
            table.setCellWidget(i, 4, view_btn)
        
        table.resizeColumnsToContents()
    
    def view_ledger(self, customer_id):
        """Open ledger for customer"""
        self.view_ledger_requested.emit(customer_id)
    
    def show_add_customer_dialog(self):
        """Show add customer dialog"""
        dialog = AddCustomerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_data()

class AddCustomerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.setWindowTitle("Add Customer")
        self.setFixedSize(500, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Add New Customer")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setFixedWidth(120)
        name_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Phone
        phone_layout = QHBoxLayout()
        phone_label = QLabel("Phone:")
        phone_label.setFixedWidth(120)
        phone_layout.addWidget(phone_label)
        self.phone_input = QLineEdit()
        phone_layout.addWidget(self.phone_input)
        layout.addLayout(phone_layout)
        
        # Type
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        type_label.setFixedWidth(120)
        type_layout.addWidget(type_label)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Regular", "Distributor"])
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Address
        address_label = QLabel("Address:")
        layout.addWidget(address_label)
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        layout.addWidget(self.address_input)
        
        # Opening Balance
        balance_layout = QHBoxLayout()
        balance_label = QLabel("Opening Balance:")
        balance_label.setFixedWidth(120)
        balance_layout.addWidget(balance_label)
        self.balance_input = QDoubleSpinBox()
        self.balance_input.setRange(-999999, 999999)
        self.balance_input.setValue(0.0)
        balance_layout.addWidget(self.balance_input)
        layout.addLayout(balance_layout)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: white;
                color: #4A90E2;
                border: 2px solid #4A90E2;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        add_btn = QPushButton("Add Customer")
        add_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        add_btn.clicked.connect(self.add_customer)
        button_layout.addWidget(add_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def add_customer(self):
        """Add customer to database"""
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        customer_type = self.type_combo.currentText()
        address = self.address_input.toPlainText().strip()
        opening_balance = self.balance_input.value()
        
        if not name:
            QMessageBox.warning(self, "Error", "Please enter customer name.")
            return
        
        customer_id = self.db.add_customer(name, phone, customer_type, address, opening_balance)
        if customer_id:
            QMessageBox.information(self, "Success", "Customer added successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to add customer.")

