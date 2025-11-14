"""
Main window with navigation sidebar and content area
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from dashboard import DashboardWidget
from sales import SalesWidget
from customers import CustomersWidget
from ledger import LedgerWidget
from fuel_stock import FuelStockWidget
from expenses import ExpensesWidget
from reports import ReportsWidget
from settings import SettingsWidget

class MainWindow(QMainWindow):
    logout_requested = pyqtSignal()
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Petrol Pump Management System")
        self.setMinimumSize(1200, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Content area
        self.content_area = self.create_content_area()
        main_layout.addWidget(self.content_area, 1)
        
        central_widget.setLayout(main_layout)
        
        # Set styles
        self.setStyleSheet("""
            QMainWindow {
                background: #f5f5f5;
            }
            QPushButton {
                border: none;
                padding: 12px 20px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #e8f4f8;
            }
        """)
    
    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QWidget {
                background: #2c3e50;
            }
            QPushButton {
                color: white;
                text-align: left;
                padding: 15px 20px;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #34495e;
            }
            QPushButton.active {
                background: #3498db;
                font-weight: bold;
            }
            QLabel {
                color: white;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo/Title
        logo_layout = QHBoxLayout()
        logo_label = QLabel("⛽ PetrolPump Pro")
        logo_font = QFont()
        logo_font.setPointSize(16)
        logo_font.setBold(True)
        logo_label.setFont(logo_font)
        logo_label.setStyleSheet("padding: 20px; color: white;")
        logo_layout.addWidget(logo_label)
        layout.addLayout(logo_layout)
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "dashboard"),
            ("Sales", "sales"),
            ("Customers", "customers"),
            ("Ledger", "ledger"),
            ("Fuel Stock", "fuel_stock"),
            ("Expenses", "expenses"),
            ("Reports", "reports"),
            ("Settings", "settings")
        ]
        
        for name, key in nav_items:
            btn = QPushButton(name)
            btn.setObjectName(f"nav_{key}")
            btn.clicked.connect(lambda checked, k=key: self.navigate_to(k))
            self.nav_buttons[key] = btn
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.handle_logout)
        logout_btn.setStyleSheet("""
            QPushButton {
                color: #e74c3c;
                border-top: 1px solid #34495e;
            }
            QPushButton:hover {
                background: #c0392b;
                color: white;
            }
        """)
        layout.addWidget(logout_btn)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def create_content_area(self):
        """Create main content area with stacked widgets"""
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Top bar
        top_bar = self.create_top_bar()
        layout.addWidget(top_bar)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        
        # Add all pages
        self.dashboard = DashboardWidget()
        self.sales = SalesWidget()
        self.customers = CustomersWidget()
        self.ledger = LedgerWidget()
        self.fuel_stock = FuelStockWidget()
        self.expenses = ExpensesWidget()
        self.reports = ReportsWidget()
        self.settings = SettingsWidget(self.user_data)
        
        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.sales)
        self.stacked_widget.addWidget(self.customers)
        self.stacked_widget.addWidget(self.ledger)
        self.stacked_widget.addWidget(self.fuel_stock)
        self.stacked_widget.addWidget(self.expenses)
        self.stacked_widget.addWidget(self.reports)
        self.stacked_widget.addWidget(self.settings)
        
        # Connect customer ledger view signal
        self.customers.view_ledger_requested.connect(self.on_view_customer_ledger)
        
        layout.addWidget(self.stacked_widget)
        
        content_widget.setLayout(layout)
        return content_widget
    
    def create_top_bar(self):
        """Create top bar with user info"""
        top_bar = QWidget()
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet("""
            QWidget {
                background: white;
                border-bottom: 1px solid #e0e0e0;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background: #4A90E2;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background: #357ABD;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        
        # App name
        app_label = QLabel("Petrol Pump Management System")
        app_font = QFont()
        app_font.setPointSize(16)
        app_font.setBold(True)
        app_label.setFont(app_font)
        layout.addWidget(app_label)
        
        layout.addStretch()
        
        # Quick action buttons
        quick_actions = QHBoxLayout()
        quick_actions.setSpacing(10)
        
        add_sale_btn = QPushButton("+ Add Sale")
        add_sale_btn.clicked.connect(lambda: self.navigate_to("sales"))
        quick_actions.addWidget(add_sale_btn)
        
        add_expense_btn = QPushButton("+ Add Expense")
        add_expense_btn.clicked.connect(lambda: self.navigate_to("expenses"))
        quick_actions.addWidget(add_expense_btn)
        
        layout.addLayout(quick_actions)
        
        # User info
        user_layout = QHBoxLayout()
        user_layout.setSpacing(10)
        
        user_label = QLabel(f"{self.user_data['username']} ({self.user_data['role']})")
        user_label.setStyleSheet("color: #666; font-size: 14px;")
        user_layout.addWidget(user_label)
        
        layout.addLayout(user_layout)
        
        top_bar.setLayout(layout)
        return top_bar
    
    def navigate_to(self, page_key):
        """Navigate to a specific page"""
        page_map = {
            "dashboard": 0,
            "sales": 1,
            "customers": 2,
            "ledger": 3,
            "fuel_stock": 4,
            "expenses": 5,
            "reports": 6,
            "settings": 7
        }
        
        if page_key in page_map:
            self.stacked_widget.setCurrentIndex(page_map[page_key])
            
            # Update active button
            for key, btn in self.nav_buttons.items():
                if key == page_key:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: #3498db;
                            font-weight: bold;
                            color: white;
                        }
                    """)
                else:
                    btn.setStyleSheet("""
                        QPushButton {
                            color: white;
                            background: transparent;
                        }
                    """)
            
            # Refresh page data
            current_widget = self.stacked_widget.currentWidget()
            if hasattr(current_widget, 'refresh_data'):
                current_widget.refresh_data()
    
    def on_view_customer_ledger(self, customer_id):
        """Handle view customer ledger request"""
        self.navigate_to("ledger")
        if hasattr(self.ledger, 'set_customer'):
            self.ledger.set_customer(customer_id)
    
    def handle_logout(self):
        """Handle logout with confirmation"""
        reply = QMessageBox.question(
            self,
            "Logout Confirmation",
            "Are you sure you want to log out?",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Yes:
            self.logout_requested.emit()

