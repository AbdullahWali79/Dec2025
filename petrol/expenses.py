"""
Expenses Management module
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QComboBox, QTextEdit, QDateEdit,
                             QDoubleSpinBox, QMessageBox, QHeaderView, QFrame)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from database import Database

class ExpensesWidget(QWidget):
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
        header = QLabel("Expenses Management")
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Today's total card
        today_card = QFrame()
        today_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        today_layout = QHBoxLayout()
        today_label = QLabel("Today's Total Expenses:")
        today_label.setStyleSheet("font-size: 16px;")
        today_layout.addWidget(today_label)
        self.today_total_label = QLabel("$0.00")
        self.today_total_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #e74c3c;")
        today_layout.addWidget(self.today_total_label)
        today_layout.addStretch()
        today_card.setLayout(today_layout)
        layout.addWidget(today_card)
        
        # Main content - two columns
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Left: Add Expense Form
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        form_frame.setFixedWidth(400)
        form_layout = QVBoxLayout()
        
        form_title = QLabel("Add New Expense")
        form_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        form_layout.addWidget(form_title)
        
        # Category
        category_label = QLabel("Category:")
        form_layout.addWidget(category_label)
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.addItems([
            "Staff Salary", "Maintenance", "Utilities", "Fuel Purchase",
            "Rent", "Insurance", "Other"
        ])
        form_layout.addWidget(self.category_combo)
        
        # Amount
        amount_label = QLabel("Amount:")
        form_layout.addWidget(amount_label)
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 999999)
        self.amount_input.setValue(0.0)
        self.amount_input.setPrefix("$ ")
        form_layout.addWidget(self.amount_input)
        
        # Remarks
        remarks_label = QLabel("Remarks:")
        form_layout.addWidget(remarks_label)
        self.remarks_input = QTextEdit()
        self.remarks_input.setMaximumHeight(100)
        self.remarks_input.setPlaceholderText("Add a short description...")
        form_layout.addWidget(self.remarks_input)
        
        # Date
        date_label = QLabel("Date:")
        form_layout.addWidget(date_label)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        form_layout.addWidget(self.date_input)
        
        # Add button
        add_btn = QPushButton("Add Expense")
        add_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        add_btn.clicked.connect(self.add_expense)
        form_layout.addWidget(add_btn)
        
        form_frame.setLayout(form_layout)
        content_layout.addWidget(form_frame)
        
        # Right: All Expenses Table
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        table_layout = QVBoxLayout()
        
        table_title = QLabel("All Expenses")
        table_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        table_layout.addWidget(table_title)
        
        self.expenses_table = QTableWidget()
        self.expenses_table.setColumnCount(5)
        self.expenses_table.setHorizontalHeaderLabels([
            "EXPENSE ID", "DATE", "CATEGORY", "REMARKS", "AMOUNT"
        ])
        self.expenses_table.horizontalHeader().setStretchLastSection(True)
        self.expenses_table.setAlternatingRowColors(True)
        table_layout.addWidget(self.expenses_table)
        
        # Grand total
        self.grand_total_label = QLabel("Grand Total: $0.00")
        self.grand_total_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        table_layout.addWidget(self.grand_total_label)
        
        table_frame.setLayout(table_layout)
        content_layout.addWidget(table_frame, 1)
        
        layout.addLayout(content_layout)
        self.setLayout(layout)
    
    def add_expense(self):
        """Add new expense"""
        category = self.category_combo.currentText().strip()
        amount = self.amount_input.value()
        remarks = self.remarks_input.toPlainText().strip()
        date = self.date_input.date().toString("yyyy-MM-dd")
        
        if not category:
            QMessageBox.warning(self, "Error", "Please select or enter a category.")
            return
        
        if amount <= 0:
            QMessageBox.warning(self, "Error", "Amount must be greater than 0.")
            return
        
        expense_id = self.db.add_expense(date, category, amount, remarks)
        if expense_id:
            QMessageBox.information(self, "Success", "Expense added successfully!")
            # Clear form
            self.category_combo.setCurrentIndex(0)
            self.amount_input.setValue(0.0)
            self.remarks_input.clear()
            self.date_input.setDate(QDate.currentDate())
            self.refresh_data()
        else:
            QMessageBox.warning(self, "Error", "Failed to add expense.")
    
    def refresh_data(self):
        """Refresh expenses data"""
        # Update today's total
        today = QDate.currentDate().toString("yyyy-MM-dd")
        today_total = self.db.get_expense_total(today)
        self.today_total_label.setText(f"${today_total:,.2f}")
        
        # Load expenses
        expenses = self.db.get_expenses()
        
        self.expenses_table.setRowCount(len(expenses))
        grand_total = 0
        
        for i, expense in enumerate(expenses):
            self.expenses_table.setItem(i, 0, QTableWidgetItem(f"#EXP{expense['id']:03d}"))
            self.expenses_table.setItem(i, 1, QTableWidgetItem(expense['date']))
            self.expenses_table.setItem(i, 2, QTableWidgetItem(expense['category']))
            self.expenses_table.setItem(i, 3, QTableWidgetItem(expense['remarks']))
            
            amount_item = QTableWidgetItem(f"${expense['amount']:,.2f}")
            amount_item.setForeground(Qt.red)
            self.expenses_table.setItem(i, 4, amount_item)
            
            grand_total += expense['amount']
        
        self.grand_total_label.setText(f"Grand Total: ${grand_total:,.2f}")
        self.expenses_table.resizeColumnsToContents()

