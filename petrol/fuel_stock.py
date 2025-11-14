"""
Fuel Stock Management module
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QDialog, QLineEdit, QDoubleSpinBox, QComboBox,
                             QMessageBox, QHeaderView, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import Database

class FuelStockWidget(QWidget):
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
        title = QLabel("Fuel Stock Management")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Monitor, add, and update fuel inventory.")
        subtitle.setStyleSheet("color: #666; font-size: 14px;")
        header_layout.addWidget(subtitle)
        
        header_layout.addStretch()
        
        add_stock_btn = QPushButton("+ Add New Stock")
        add_stock_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        add_stock_btn.clicked.connect(self.show_add_stock_dialog)
        header_layout.addWidget(add_stock_btn)
        
        layout.addLayout(header_layout)
        
        # Summary cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        
        self.stock_levels_card = self.create_summary_card("Stock Levels by Fuel Type", "0 L", "Total current stock")
        self.total_value_card = self.create_summary_card("Total Value", "Rs. 0.00", "Estimated stock value")
        self.low_stock_card = self.create_summary_card("Low Stock Alert", "0 Items", "Items below threshold")
        
        cards_layout.addWidget(self.stock_levels_card)
        cards_layout.addWidget(self.total_value_card)
        cards_layout.addWidget(self.low_stock_card)
        
        layout.addLayout(cards_layout)
        
        # Fuel stock table
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        table_layout = QVBoxLayout()
        
        table_title = QLabel("Fuel Stock Details")
        table_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        table_layout.addWidget(table_title)
        
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(5)
        self.stock_table.setHorizontalHeaderLabels([
            "FUEL TYPE", "RATE PER LITRE", "CURRENT STOCK (L)", "LAST UPDATED", "ACTIONS"
        ])
        self.stock_table.horizontalHeader().setStretchLastSection(True)
        self.stock_table.setAlternatingRowColors(True)
        table_layout.addWidget(self.stock_table)
        
        table_frame.setLayout(table_layout)
        layout.addWidget(table_frame)
        
        self.setLayout(layout)
    
    def create_summary_card(self, title, value, subtitle):
        """Create summary card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        card.setMinimumHeight(120)
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(20)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(value_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #95a5a6; font-size: 12px;")
        layout.addWidget(subtitle_label)
        
        layout.addStretch()
        card.setLayout(layout)
        
        card.value_label = value_label
        return card
    
    def refresh_data(self):
        """Refresh stock data"""
        fuels = self.db.get_all_fuel_types()
        
        # Update summary cards
        total_stock = sum(f['current_stock'] for f in fuels)
        self.stock_levels_card.value_label.setText(f"{total_stock:,.1f} L")
        
        total_value = sum(f['current_stock'] * f['rate_per_litre'] for f in fuels)
        self.total_value_card.value_label.setText(f"Rs. {total_value:,.2f}")
        
        low_stock_count = sum(1 for f in fuels if f['current_stock'] < f['low_stock_threshold'])
        self.low_stock_card.value_label.setText(f"{low_stock_count} Item{'s' if low_stock_count != 1 else ''}")
        if low_stock_count > 0:
            self.low_stock_card.setStyleSheet("""
                QFrame {
                    background: #fff3cd;
                    border-radius: 5px;
                    padding: 20px;
                    border: 2px solid #ffc107;
                }
            """)
        else:
            self.low_stock_card.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 5px;
                    padding: 20px;
                }
            """)
        
        # Update table
        self.stock_table.setRowCount(len(fuels))
        for i, fuel in enumerate(fuels):
            self.stock_table.setItem(i, 0, QTableWidgetItem(fuel['name']))
            self.stock_table.setItem(i, 1, QTableWidgetItem(f"Rs. {fuel['rate_per_litre']:.2f}"))
            
            stock_item = QTableWidgetItem(f"{fuel['current_stock']:,.2f} L")
            if fuel['current_stock'] < fuel['low_stock_threshold']:
                stock_item.setForeground(Qt.red)
            self.stock_table.setItem(i, 2, stock_item)
            
            self.stock_table.setItem(i, 3, QTableWidgetItem(fuel['last_updated']))
            
            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background: #4A90E2;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
            """)
            edit_btn.clicked.connect(lambda checked, fid=fuel['id']: self.edit_fuel(fid))
            action_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background: #e74c3c;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
            """)
            delete_btn.clicked.connect(lambda checked, fid=fuel['id']: self.delete_fuel(fid))
            action_layout.addWidget(delete_btn)
            
            action_widget.setLayout(action_layout)
            self.stock_table.setCellWidget(i, 4, action_widget)
        
        self.stock_table.resizeColumnsToContents()
    
    def show_add_stock_dialog(self):
        """Show add stock dialog"""
        dialog = AddStockDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_data()
    
    def edit_fuel(self, fuel_id):
        """Edit fuel type"""
        dialog = EditFuelDialog(self, fuel_id)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_data()
    
    def delete_fuel(self, fuel_id):
        """Delete fuel type"""
        reply = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this fuel type?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "Info", "Delete functionality would be implemented here.")

class AddStockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.setWindowTitle("Add New Stock")
        self.setFixedSize(400, 250)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Add New Stock")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Fuel Type
        fuel_layout = QHBoxLayout()
        fuel_label = QLabel("Fuel Type:")
        fuel_label.setFixedWidth(120)
        fuel_layout.addWidget(fuel_label)
        self.fuel_combo = QComboBox()
        fuels = self.db.get_all_fuel_types()
        for fuel in fuels:
            self.fuel_combo.addItem(fuel['name'], fuel['id'])
        fuel_layout.addWidget(self.fuel_combo)
        layout.addLayout(fuel_layout)
        
        # Quantity
        qty_layout = QHBoxLayout()
        qty_label = QLabel("Quantity (L):")
        qty_label.setFixedWidth(120)
        qty_layout.addWidget(qty_label)
        self.quantity_input = QDoubleSpinBox()
        self.quantity_input.setRange(0, 999999)
        self.quantity_input.setValue(0.0)
        qty_layout.addWidget(self.quantity_input)
        layout.addLayout(qty_layout)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        add_btn = QPushButton("Add Stock")
        add_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        add_btn.clicked.connect(self.add_stock)
        button_layout.addWidget(add_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def add_stock(self):
        """Add stock to fuel type"""
        fuel_id = self.fuel_combo.currentData()
        quantity = self.quantity_input.value()
        
        if quantity <= 0:
            QMessageBox.warning(self, "Error", "Quantity must be greater than 0.")
            return
        
        success = self.db.update_fuel_stock(fuel_id, quantity)
        if success:
            QMessageBox.information(self, "Success", "Stock added successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to add stock.")

class EditFuelDialog(QDialog):
    def __init__(self, parent, fuel_id):
        super().__init__(parent)
        self.db = Database()
        self.fuel_id = fuel_id
        self.setWindowTitle("Edit Fuel Type")
        self.setFixedSize(400, 250)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Edit Fuel Type")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Get fuel data
        fuels = self.db.get_all_fuel_types()
        fuel = next((f for f in fuels if f['id'] == self.fuel_id), None)
        if not fuel:
            self.reject()
            return
        
        # Name (read-only)
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setFixedWidth(120)
        name_layout.addWidget(name_label)
        name_input = QLineEdit(fuel['name'])
        name_input.setReadOnly(True)
        name_input.setStyleSheet("background: #f0f0f0;")
        name_layout.addWidget(name_input)
        layout.addLayout(name_layout)
        
        # Rate
        rate_layout = QHBoxLayout()
        rate_label = QLabel("Rate per Litre:")
        rate_label.setFixedWidth(120)
        rate_layout.addWidget(rate_label)
        self.rate_input = QDoubleSpinBox()
        self.rate_input.setRange(0, 9999)
        self.rate_input.setValue(fuel['rate_per_litre'])
        rate_layout.addWidget(self.rate_input)
        layout.addLayout(rate_layout)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        save_btn.clicked.connect(self.save_changes)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def save_changes(self):
        """Save fuel type changes"""
        new_rate = self.rate_input.value()
        
        if new_rate <= 0:
            QMessageBox.warning(self, "Error", "Rate must be greater than 0.")
            return
        
        success = self.db.update_fuel_rate(self.fuel_id, new_rate)
        if success:
            QMessageBox.information(self, "Success", "Fuel type updated successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to update fuel type.")

