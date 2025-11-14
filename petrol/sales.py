"""
Sales module for managing fuel sales
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QTableWidget,
                             QTableWidgetItem, QDateEdit, QTextEdit, QRadioButton,
                             QButtonGroup, QHeaderView, QMessageBox, QFrame, QDialog)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPrinter, QPainter
from PyQt5.QtPrintSupport import QPrintDialog
from datetime import datetime
from database import Database

class SalesWidget(QWidget):
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
        header = QLabel("Sales Management")
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        subtitle = QLabel("Create new sale entries and view daily transactions.")
        subtitle.setStyleSheet("color: #666; font-size: 14px; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Stats
        stats_layout = QHBoxLayout()
        self.todays_total_label = QLabel("Today's Total Sales: Rs. 0.00")
        self.todays_total_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #27ae60;")
        stats_layout.addWidget(self.todays_total_label)
        
        self.litres_sold_label = QLabel("Total Litres Sold: 0 L")
        self.litres_sold_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db;")
        stats_layout.addWidget(self.litres_sold_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # Main content - two columns
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Left: New Sale Form
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        form_frame.setFixedWidth(500)
        form_layout = QVBoxLayout()
        
        form_title = QLabel("New Sale Entry")
        form_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        form_layout.addWidget(form_title)
        
        # Date
        date_layout = QHBoxLayout()
        date_layout.setSpacing(10)
        date_label = QLabel("Date:")
        date_label.setFixedWidth(130)
        date_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        date_layout.addWidget(date_label)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setStyleSheet("padding: 8px; font-size: 14px;")
        date_layout.addWidget(self.date_input)
        form_layout.addLayout(date_layout)
        form_layout.addSpacing(10)
        
        # Fuel Type
        fuel_layout = QHBoxLayout()
        fuel_layout.setSpacing(10)
        fuel_label = QLabel("Fuel Type:")
        fuel_label.setFixedWidth(130)
        fuel_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        fuel_layout.addWidget(fuel_label)
        self.fuel_type_combo = QComboBox()
        self.fuel_type_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        fuel_layout.addWidget(self.fuel_type_combo)
        form_layout.addLayout(fuel_layout)
        form_layout.addSpacing(10)
        
        # Customer
        customer_layout = QHBoxLayout()
        customer_layout.setSpacing(10)
        customer_label = QLabel("Customer:")
        customer_label.setFixedWidth(130)
        customer_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        customer_layout.addWidget(customer_label)
        self.customer_combo = QComboBox()
        self.customer_combo.setEditable(True)
        self.customer_combo.setInsertPolicy(QComboBox.NoInsert)
        self.customer_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        customer_layout.addWidget(self.customer_combo)
        form_layout.addLayout(customer_layout)
        form_layout.addSpacing(10)
        
        # Quantity
        qty_layout = QHBoxLayout()
        qty_layout.setSpacing(10)
        qty_label = QLabel("Quantity (L):")
        qty_label.setFixedWidth(130)
        qty_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        qty_layout.addWidget(qty_label)
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("e.g., 10.5")
        self.quantity_input.setStyleSheet("padding: 8px; font-size: 14px;")
        self.quantity_input.textChanged.connect(self.calculate_total)
        qty_layout.addWidget(self.quantity_input)
        form_layout.addLayout(qty_layout)
        form_layout.addSpacing(10)
        
        # Rate
        rate_layout = QHBoxLayout()
        rate_layout.setSpacing(10)
        rate_label = QLabel("Rate (per litre):")
        rate_label.setFixedWidth(130)
        rate_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        rate_layout.addWidget(rate_label)
        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText("e.g., 96.72")
        self.rate_input.setStyleSheet("padding: 8px; font-size: 14px;")
        self.rate_input.textChanged.connect(self.calculate_total)
        rate_layout.addWidget(self.rate_input)
        form_layout.addLayout(rate_layout)
        form_layout.addSpacing(10)
        
        # Total
        total_layout = QHBoxLayout()
        total_layout.setSpacing(10)
        total_label = QLabel("Total:")
        total_label.setFixedWidth(130)
        total_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        total_layout.addWidget(total_label)
        self.total_input = QLineEdit()
        self.total_input.setPlaceholderText("Auto-calculated")
        self.total_input.setReadOnly(True)
        self.total_input.setStyleSheet("background: #f0f0f0; padding: 8px; font-size: 14px; font-weight: bold;")
        total_layout.addWidget(self.total_input)
        form_layout.addLayout(total_layout)
        form_layout.addSpacing(10)
        
        # Payment Type
        payment_layout = QHBoxLayout()
        payment_layout.setSpacing(10)
        payment_label = QLabel("Payment Type:")
        payment_label.setFixedWidth(130)
        payment_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        payment_layout.addWidget(payment_label)
        self.payment_group = QButtonGroup()
        self.cash_radio = QRadioButton("Cash")
        self.cash_radio.setChecked(True)
        self.cash_radio.setStyleSheet("font-size: 14px;")
        self.credit_radio = QRadioButton("Credit")
        self.credit_radio.setStyleSheet("font-size: 14px;")
        self.payment_group.addButton(self.cash_radio, 0)
        self.payment_group.addButton(self.credit_radio, 1)
        payment_btn_layout = QHBoxLayout()
        payment_btn_layout.setSpacing(15)
        payment_btn_layout.addWidget(self.cash_radio)
        payment_btn_layout.addWidget(self.credit_radio)
        payment_btn_layout.addStretch()
        payment_layout.addLayout(payment_btn_layout)
        form_layout.addLayout(payment_layout)
        form_layout.addSpacing(10)
        
        # Remarks
        remarks_label = QLabel("Remarks (Optional):")
        remarks_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px; margin-top: 5px;")
        form_layout.addWidget(remarks_label)
        self.remarks_input = QTextEdit()
        self.remarks_input.setMaximumHeight(80)
        self.remarks_input.setPlaceholderText("Add any notes here...")
        self.remarks_input.setStyleSheet("padding: 8px; font-size: 14px;")
        form_layout.addWidget(self.remarks_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear Form")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: white;
                color: #4A90E2;
                border: 2px solid #4A90E2;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(clear_btn)
        
        add_sale_btn = QPushButton("Add Sale")
        add_sale_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        add_sale_btn.clicked.connect(self.add_sale)
        button_layout.addWidget(add_sale_btn)
        
        form_layout.addLayout(button_layout)
        form_frame.setLayout(form_layout)
        content_layout.addWidget(form_frame)
        
        # Right: Today's Sales Table
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        table_layout = QVBoxLayout()
        
        table_title = QLabel("Today's Sales")
        table_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        table_layout.addWidget(table_title)
        
        # Search and filter
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by customer...")
        filter_layout.addWidget(self.search_input)
        
        self.date_filter = QDateEdit()
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setCalendarPopup(True)
        self.date_filter.dateChanged.connect(self.refresh_sales_table)
        filter_layout.addWidget(self.date_filter)
        
        print_btn = QPushButton("Print Receipt")
        print_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
        """)
        print_btn.clicked.connect(self.show_receipt_preview)
        filter_layout.addWidget(print_btn)
        
        table_layout.addLayout(filter_layout)
        
        # Sales table
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(7)
        self.sales_table.setHorizontalHeaderLabels([
            "DATE", "CUSTOMER", "FUEL TYPE", "QTY (L)", "RATE", "TOTAL", "PAYMENT"
        ])
        self.sales_table.horizontalHeader().setStretchLastSection(True)
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sales_table.itemSelectionChanged.connect(self.on_sale_selected)
        table_layout.addWidget(self.sales_table)
        
        table_frame.setLayout(table_layout)
        content_layout.addWidget(table_frame, 1)
        
        layout.addLayout(content_layout)
        self.setLayout(layout)
        
        # Load fuel types and customers
        self.load_fuel_types()
        self.load_customers()
        
        # Set default rate when fuel type changes
        self.fuel_type_combo.currentIndexChanged.connect(self.set_default_rate)
        
        # Store selected sale for receipt
        self.selected_sale = None
    
    def load_fuel_types(self):
        """Load fuel types into combo box"""
        self.fuel_type_combo.clear()
        fuels = self.db.get_all_fuel_types()
        for fuel in fuels:
            self.fuel_type_combo.addItem(f"{fuel['name']} - Rs. {fuel['rate_per_litre']:.2f}/L", fuel['id'])
    
    def load_customers(self):
        """Load customers into combo box"""
        self.customer_combo.clear()
        self.customer_combo.addItem("Walk-in Customer", None)
        customers = self.db.get_all_customers()
        for customer in customers:
            self.customer_combo.addItem(customer['name'], customer['id'])
    
    def set_default_rate(self):
        """Set default rate when fuel type is selected"""
        index = self.fuel_type_combo.currentIndex()
        if index >= 0:
            fuel_id = self.fuel_type_combo.currentData()
            fuels = self.db.get_all_fuel_types()
            for fuel in fuels:
                if fuel['id'] == fuel_id:
                    self.rate_input.setText(str(fuel['rate_per_litre']))
                    break
    
    def calculate_total(self):
        """Calculate total from quantity and rate"""
        try:
            quantity = float(self.quantity_input.text() or 0)
            rate = float(self.rate_input.text() or 0)
            total = quantity * rate
            self.total_input.setText(f"{total:.2f}")
        except ValueError:
            self.total_input.setText("0.00")
    
    def clear_form(self):
        """Clear the sale form"""
        self.date_input.setDate(QDate.currentDate())
        self.fuel_type_combo.setCurrentIndex(0)
        self.customer_combo.setCurrentIndex(0)
        self.quantity_input.clear()
        self.rate_input.clear()
        self.total_input.clear()
        self.cash_radio.setChecked(True)
        self.remarks_input.clear()
    
    def add_sale(self):
        """Add new sale"""
        try:
            date = self.date_input.date().toString("yyyy-MM-dd")
            fuel_id = self.fuel_type_combo.currentData()
            customer_id = self.customer_combo.currentData()
            quantity = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            total = float(self.total_input.text())
            payment_type = "Cash" if self.cash_radio.isChecked() else "Credit"
            remarks = self.remarks_input.toPlainText()
            
            if quantity <= 0 or rate <= 0:
                QMessageBox.warning(self, "Error", "Quantity and rate must be greater than 0.")
                return
            
            # Check stock availability
            fuels = self.db.get_all_fuel_types()
            fuel_stock = next((f['current_stock'] for f in fuels if f['id'] == fuel_id), 0)
            if quantity > fuel_stock:
                QMessageBox.warning(self, "Insufficient Stock", 
                                  f"Available stock: {fuel_stock:.2f} L\nRequested: {quantity:.2f} L")
                return
            
            # If credit sale, customer must be selected
            if payment_type == "Credit" and not customer_id:
                QMessageBox.warning(self, "Error", "Please select a customer for credit sales.")
                return
            
            sale_id = self.db.add_sale(date, fuel_id, customer_id, quantity, rate, total, 
                                      payment_type, remarks)
            
            if sale_id:
                QMessageBox.information(self, "Success", "Sale added successfully!")
                self.clear_form()
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Error", "Failed to add sale.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numeric values.")
    
    def refresh_sales_table(self):
        """Refresh sales table"""
        date = self.date_filter.date().toString("yyyy-MM-dd")
        sales = self.db.get_sales(start_date=date, end_date=date)
        
        self.sales_table.setRowCount(len(sales))
        for i, sale in enumerate(sales):
            self.sales_table.setItem(i, 0, QTableWidgetItem(sale['date']))
            self.sales_table.setItem(i, 1, QTableWidgetItem(sale['customer_name']))
            self.sales_table.setItem(i, 2, QTableWidgetItem(sale['fuel_type']))
            self.sales_table.setItem(i, 3, QTableWidgetItem(f"{sale['quantity']:.2f}"))
            self.sales_table.setItem(i, 4, QTableWidgetItem(f"Rs. {sale['rate']:.2f}"))
            self.sales_table.setItem(i, 5, QTableWidgetItem(f"Rs. {sale['total']:.2f}"))
            
            payment_item = QTableWidgetItem(sale['payment_type'])
            if sale['payment_type'] == "Cash":
                payment_item.setForeground(Qt.darkGreen)
            else:
                payment_item.setForeground(Qt.blue)
            self.sales_table.setItem(i, 6, payment_item)
        
        self.sales_table.resizeColumnsToContents()
    
    def refresh_data(self):
        """Refresh all data"""
        # Update stats
        todays_sales = self.db.get_todays_sales()
        self.todays_total_label.setText(f"Today's Total Sales: Rs. {todays_sales:,.2f}")
        
        fuel_sold = self.db.get_todays_fuel_sold()
        self.litres_sold_label.setText(f"Total Litres Sold: {fuel_sold:.1f} L")
        
        # Refresh table
        self.refresh_sales_table()
        
        # Reload combos
        self.load_fuel_types()
        self.load_customers()
    
    def on_sale_selected(self):
        """Handle sale selection from table"""
        current_row = self.sales_table.currentRow()
        if current_row >= 0:
            date = self.sales_table.item(current_row, 0).text()
            customer = self.sales_table.item(current_row, 1).text()
            fuel_type = self.sales_table.item(current_row, 2).text()
            quantity = self.sales_table.item(current_row, 3).text()
            rate = self.sales_table.item(current_row, 4).text().replace("Rs. ", "")
            total = self.sales_table.item(current_row, 5).text().replace("Rs. ", "")
            payment = self.sales_table.item(current_row, 6).text()
            
            self.selected_sale = {
                'date': date,
                'customer': customer,
                'fuel_type': fuel_type,
                'quantity': quantity,
                'rate': rate,
                'total': total,
                'payment': payment
            }
    
    def show_receipt_preview(self):
        """Show thermal receipt preview"""
        if not self.selected_sale:
            # If no sale selected, check if form has data
            if self.quantity_input.text() and self.rate_input.text():
                try:
                    quantity = float(self.quantity_input.text())
                    rate = float(self.rate_input.text())
                    total = float(self.total_input.text() or 0)
                    
                    fuel_name = self.fuel_type_combo.currentText().split(" - ")[0] if self.fuel_type_combo.currentText() else "N/A"
                    customer = self.customer_combo.currentText() or "Walk-in Customer"
                    payment = "Cash" if self.cash_radio.isChecked() else "Credit"
                    date = self.date_input.date().toString("dd/MM/yyyy")
                    
                    self.selected_sale = {
                        'date': date,
                        'customer': customer,
                        'fuel_type': fuel_name,
                        'quantity': f"{quantity:.2f}",
                        'rate': f"{rate:.2f}",
                        'total': f"{total:.2f}",
                        'payment': payment
                    }
                except:
                    QMessageBox.warning(self, "Error", "Please select a sale from the table or fill the form.")
                    return
            else:
                QMessageBox.warning(self, "Error", "Please select a sale from the table or fill the form to print receipt.")
                return
        
        # Show receipt preview dialog
        dialog = ReceiptPreviewDialog(self, self.selected_sale)
        dialog.exec_()


class ReceiptPreviewDialog(QDialog):
    """Thermal receipt preview dialog"""
    def __init__(self, parent, sale_data):
        super().__init__(parent)
        self.sale_data = sale_data
        self.setWindowTitle("Receipt Preview - Thermal Printer")
        self.setFixedSize(300, 600)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(0)
        
        # Receipt preview (white background, narrow width for thermal printer)
        receipt_frame = QFrame()
        receipt_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #333;
                border-radius: 0px;
            }
        """)
        receipt_frame.setFixedWidth(280)
        receipt_layout = QVBoxLayout()
        receipt_layout.setContentsMargins(15, 20, 15, 20)
        receipt_layout.setSpacing(5)
        
        # Header
        header_label = QLabel("PETROL PUMP")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: #000; margin-bottom: 5px;")
        receipt_layout.addWidget(header_label)
        
        address_label = QLabel("123 Main Street, City")
        address_label.setAlignment(Qt.AlignCenter)
        address_label.setStyleSheet("color: #333; font-size: 10px;")
        receipt_layout.addWidget(address_label)
        
        phone_label = QLabel("Phone: +92 304 6983794")
        phone_label.setAlignment(Qt.AlignCenter)
        phone_label.setStyleSheet("color: #333; font-size: 10px;")
        receipt_layout.addWidget(phone_label)
        
        # Separator
        separator1 = QLabel("=" * 32)
        separator1.setAlignment(Qt.AlignCenter)
        separator1.setStyleSheet("color: #000; font-size: 10px; margin: 5px 0px;")
        receipt_layout.addWidget(separator1)
        
        # Sale details
        date_label = QLabel(f"Date: {self.sale_data['date']}")
        date_label.setStyleSheet("color: #000; font-size: 11px; font-weight: bold;")
        receipt_layout.addWidget(date_label)
        
        time_label = QLabel(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        time_label.setStyleSheet("color: #000; font-size: 11px;")
        receipt_layout.addWidget(time_label)
        
        separator2 = QLabel("-" * 32)
        separator2.setAlignment(Qt.AlignCenter)
        separator2.setStyleSheet("color: #000; font-size: 10px; margin: 5px 0px;")
        receipt_layout.addWidget(separator2)
        
        # Customer
        customer_label = QLabel(f"Customer: {self.sale_data['customer']}")
        customer_label.setStyleSheet("color: #000; font-size: 11px;")
        customer_label.setWordWrap(True)
        receipt_layout.addWidget(customer_label)
        
        separator3 = QLabel("-" * 32)
        separator3.setAlignment(Qt.AlignCenter)
        separator3.setStyleSheet("color: #000; font-size: 10px; margin: 5px 0px;")
        receipt_layout.addWidget(separator3)
        
        # Fuel details
        fuel_label = QLabel(f"Fuel Type: {self.sale_data['fuel_type']}")
        fuel_label.setStyleSheet("color: #000; font-size: 11px; font-weight: bold;")
        receipt_layout.addWidget(fuel_label)
        
        qty_label = QLabel(f"Quantity: {self.sale_data['quantity']} L")
        qty_label.setStyleSheet("color: #000; font-size: 11px;")
        receipt_layout.addWidget(qty_label)
        
        rate_label = QLabel(f"Rate: Rs. {self.sale_data['rate']}/L")
        rate_label.setStyleSheet("color: #000; font-size: 11px;")
        receipt_layout.addWidget(rate_label)
        
        separator4 = QLabel("=" * 32)
        separator4.setAlignment(Qt.AlignCenter)
        separator4.setStyleSheet("color: #000; font-size: 10px; margin: 5px 0px;")
        receipt_layout.addWidget(separator4)
        
        # Total
        total_label = QLabel(f"TOTAL: Rs. {self.sale_data['total']}")
        total_font = QFont()
        total_font.setPointSize(14)
        total_font.setBold(True)
        total_label.setFont(total_font)
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet("color: #000; margin: 10px 0px;")
        receipt_layout.addWidget(total_label)
        
        payment_label = QLabel(f"Payment: {self.sale_data['payment']}")
        payment_label.setAlignment(Qt.AlignCenter)
        payment_label.setStyleSheet("color: #000; font-size: 11px; font-weight: bold;")
        receipt_layout.addWidget(payment_label)
        
        separator5 = QLabel("=" * 32)
        separator5.setAlignment(Qt.AlignCenter)
        separator5.setStyleSheet("color: #000; font-size: 10px; margin: 10px 0px 5px 0px;")
        receipt_layout.addWidget(separator5)
        
        # Footer
        footer_label = QLabel("Thank You!")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_font = QFont()
        footer_font.setPointSize(12)
        footer_font.setBold(True)
        footer_label.setFont(footer_font)
        footer_label.setStyleSheet("color: #000; margin-top: 10px;")
        receipt_layout.addWidget(footer_label)
        
        visit_label = QLabel("Visit Again")
        visit_label.setAlignment(Qt.AlignCenter)
        visit_label.setStyleSheet("color: #333; font-size: 10px;")
        receipt_layout.addWidget(visit_label)
        
        receipt_frame.setLayout(receipt_layout)
        layout.addWidget(receipt_frame, 0, Qt.AlignCenter)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        print_btn = QPushButton("Print")
        print_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        print_btn.clicked.connect(self.print_receipt)
        button_layout.addWidget(print_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        self.setLayout(layout)
    
    def print_receipt(self):
        """Print receipt to thermal printer"""
        try:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setPageSize(QPrinter.Custom)
            printer.setPageSizeMM(QPrinter.A4)  # Thermal printers typically use 80mm width
            printer.setOutputFormat(QPrinter.NativeFormat)
            
            print_dialog = QPrintDialog(printer, self)
            if print_dialog.exec_() == QPrintDialog.Accepted:
                painter = QPainter()
                painter.begin(printer)
                
                # Draw receipt content
                y = 100
                painter.setFont(QFont("Arial", 12, QFont.Bold))
                painter.drawText(100, y, "PETROL PUMP")
                y += 30
                
                painter.setFont(QFont("Arial", 8))
                painter.drawText(100, y, "123 Main Street, City")
                y += 20
                painter.drawText(100, y, f"Date: {self.sale_data['date']}")
                y += 20
                painter.drawText(100, y, f"Customer: {self.sale_data['customer']}")
                y += 30
                
                painter.drawText(100, y, f"Fuel: {self.sale_data['fuel_type']}")
                y += 20
                painter.drawText(100, y, f"Qty: {self.sale_data['quantity']} L")
                y += 20
                painter.drawText(100, y, f"Rate: Rs. {self.sale_data['rate']}/L")
                y += 30
                
                painter.setFont(QFont("Arial", 14, QFont.Bold))
                painter.drawText(100, y, f"TOTAL: Rs. {self.sale_data['total']}")
                y += 30
                
                painter.setFont(QFont("Arial", 10))
                painter.drawText(100, y, "Thank You!")
                
                painter.end()
                QMessageBox.information(self, "Success", "Receipt sent to printer!")
        except Exception as e:
            QMessageBox.warning(self, "Print Error", f"Could not print receipt: {str(e)}")

