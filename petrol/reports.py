"""
Reports module for generating sales and expense reports
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QDateEdit, QTabWidget, QMessageBox, QHeaderView, QFrame)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from database import Database

class ReportsWidget(QWidget):
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
        title = QLabel("Reports")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        export_pdf_btn = QPushButton("Export to PDF")
        export_pdf_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        export_pdf_btn.clicked.connect(self.export_to_pdf)
        header_layout.addWidget(export_pdf_btn)
        
        export_excel_btn = QPushButton("Export to Excel")
        export_excel_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        export_excel_btn.clicked.connect(self.export_to_excel)
        header_layout.addWidget(export_excel_btn)
        
        layout.addLayout(header_layout)
        
        # Tabs for report range
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
        
        # Daily tab
        daily_widget = self.create_daily_widget()
        self.tabs.addTab(daily_widget, "Daily")
        
        # Monthly tab
        monthly_widget = self.create_monthly_widget()
        self.tabs.addTab(monthly_widget, "Monthly")
        
        # Custom Range tab
        custom_widget = self.create_custom_widget()
        self.tabs.addTab(custom_widget, "Custom Range")
        
        self.tabs.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tabs)
        
        # Sales vs Expenses chart section
        chart_label = QLabel("Sales vs. Expenses")
        chart_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(chart_label)
        
        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 10px;
                min-height: 200px;
            }
        """)
        chart_layout = QVBoxLayout()
        self.chart_label = QLabel("Chart visualization would be displayed here")
        self.chart_label.setAlignment(Qt.AlignCenter)
        self.chart_label.setStyleSheet("color: #666; padding: 50px;")
        chart_layout.addWidget(self.chart_label)
        chart_frame.setLayout(chart_layout)
        layout.addWidget(chart_frame)
        
        # Detailed Transactions table
        table_label = QLabel("Detailed Transactions")
        table_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(table_label)
        
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        table_layout = QVBoxLayout()
        
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(6)
        self.transactions_table.setHorizontalHeaderLabels([
            "DATE", "TRANSACTION ID", "FUEL TYPE", "VOLUME (LITERS)", "TOTAL SALES ($)", "EXPENSES ($)"
        ])
        self.transactions_table.horizontalHeader().setStretchLastSection(True)
        self.transactions_table.setAlternatingRowColors(True)
        table_layout.addWidget(self.transactions_table)
        
        # Pagination info
        self.pagination_label = QLabel("Showing 1 to 0 of 0 entries")
        self.pagination_label.setStyleSheet("color: #666; margin-top: 10px;")
        table_layout.addWidget(self.pagination_label)
        
        table_frame.setLayout(table_layout)
        layout.addWidget(table_frame)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_daily_widget(self):
        """Create daily report widget"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        layout.addWidget(QLabel("Select Date:"))
        self.daily_date = QDateEdit()
        self.daily_date.setDate(QDate.currentDate())
        self.daily_date.setCalendarPopup(True)
        layout.addWidget(self.daily_date)
        
        layout.addStretch()
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        generate_btn.clicked.connect(self.generate_daily_report)
        layout.addWidget(generate_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_monthly_widget(self):
        """Create monthly report widget"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        layout.addWidget(QLabel("Select Month:"))
        self.monthly_date = QDateEdit()
        self.monthly_date.setDate(QDate.currentDate())
        self.monthly_date.setCalendarPopup(True)
        self.monthly_date.setDisplayFormat("MMM yyyy")
        layout.addWidget(self.monthly_date)
        
        layout.addStretch()
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        generate_btn.clicked.connect(self.generate_monthly_report)
        layout.addWidget(generate_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_custom_widget(self):
        """Create custom range report widget"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        layout.addWidget(QLabel("Start Date:"))
        self.custom_start = QDateEdit()
        self.custom_start.setDate(QDate.currentDate().addDays(-7))
        self.custom_start.setCalendarPopup(True)
        layout.addWidget(self.custom_start)
        
        layout.addWidget(QLabel("End Date:"))
        self.custom_end = QDateEdit()
        self.custom_end.setDate(QDate.currentDate())
        self.custom_end.setCalendarPopup(True)
        layout.addWidget(self.custom_end)
        
        layout.addStretch()
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        generate_btn.clicked.connect(self.generate_custom_report)
        layout.addWidget(generate_btn)
        
        widget.setLayout(layout)
        return widget
    
    def on_tab_changed(self, index):
        """Handle tab change"""
        self.refresh_data()
    
    def generate_daily_report(self):
        """Generate daily report"""
        date = self.daily_date.date().toString("yyyy-MM-dd")
        self.load_transactions(date, date)
    
    def generate_monthly_report(self):
        """Generate monthly report"""
        date = self.monthly_date.date()
        start_date = QDate(date.year(), date.month(), 1).toString("yyyy-MM-dd")
        end_date = QDate(date.year(), date.month(), date.daysInMonth()).toString("yyyy-MM-dd")
        self.load_transactions(start_date, end_date)
    
    def generate_custom_report(self):
        """Generate custom range report"""
        start_date = self.custom_start.date().toString("yyyy-MM-dd")
        end_date = self.custom_end.date().toString("yyyy-MM-dd")
        self.load_transactions(start_date, end_date)
    
    def load_transactions(self, start_date, end_date):
        """Load transactions for the date range"""
        sales = self.db.get_sales(start_date, end_date)
        expenses = self.db.get_expenses(start_date, end_date)
        
        # Combine sales and expenses
        transactions = []
        for sale in sales:
            transactions.append({
                'date': sale['date'],
                'id': f"TXN-{sale['id']:03d}",
                'type': sale['fuel_type'],
                'volume': sale['quantity'],
                'sales': sale['total'],
                'expenses': 0
            })
        
        # Add expenses (simplified - in real app, expenses might be linked to transactions)
        expense_dict = {}
        for expense in expenses:
            if expense['date'] not in expense_dict:
                expense_dict[expense['date']] = 0
            expense_dict[expense['date']] += expense['amount']
        
        # Update transactions with expenses
        for trans in transactions:
            if trans['date'] in expense_dict:
                trans['expenses'] = expense_dict[trans['date']]
        
        # Sort by date
        transactions.sort(key=lambda x: x['date'], reverse=True)
        
        # Update table
        self.transactions_table.setRowCount(len(transactions))
        total_sales = 0
        total_expenses = 0
        
        for i, trans in enumerate(transactions):
            self.transactions_table.setItem(i, 0, QTableWidgetItem(trans['date']))
            
            id_item = QTableWidgetItem(trans['id'])
            id_item.setForeground(Qt.blue)
            self.transactions_table.setItem(i, 1, id_item)
            
            self.transactions_table.setItem(i, 2, QTableWidgetItem(trans['type']))
            self.transactions_table.setItem(i, 3, QTableWidgetItem(f"{trans['volume']:.2f}"))
            
            sales_item = QTableWidgetItem(f"${trans['sales']:.2f}")
            sales_item.setForeground(Qt.darkGreen)
            self.transactions_table.setItem(i, 4, sales_item)
            
            expenses_item = QTableWidgetItem(f"${trans['expenses']:.2f}")
            expenses_item.setForeground(Qt.red)
            self.transactions_table.setItem(i, 5, expenses_item)
            
            total_sales += trans['sales']
            total_expenses += trans['expenses']
        
        self.pagination_label.setText(f"Showing 1 to {len(transactions)} of {len(transactions)} entries")
        self.transactions_table.resizeColumnsToContents()
        
        # Update chart label
        self.chart_label.setText(
            f"Sales: ${total_sales:,.2f} | Expenses: ${total_expenses:,.2f} | "
            f"Net: ${total_sales - total_expenses:,.2f}"
        )
    
    def export_to_pdf(self):
        """Export report to PDF"""
        QMessageBox.information(self, "Export", "PDF export functionality would be implemented here.")
    
    def export_to_excel(self):
        """Export report to Excel"""
        QMessageBox.information(self, "Export", "Excel export functionality would be implemented here.")
    
    def refresh_data(self):
        """Refresh report data"""
        # Generate report based on current tab
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:  # Daily
            self.generate_daily_report()
        elif current_tab == 1:  # Monthly
            self.generate_monthly_report()
        else:  # Custom
            self.generate_custom_report()

