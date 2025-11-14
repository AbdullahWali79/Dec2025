"""
Settings module for user management and system settings
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QDialog, QLineEdit, QMessageBox, QHeaderView,
                             QFrame, QTabWidget, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import Database

class SettingsWidget(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.db = Database()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Settings")
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        subtitle = QLabel("Manage your password and user access.")
        subtitle.setStyleSheet("color: #666; font-size: 14px; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
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
        
        # Security tab
        security_widget = self.create_security_widget()
        self.tabs.addTab(security_widget, "Security")
        
        # Data Management tab
        data_widget = self.create_data_widget()
        self.tabs.addTab(data_widget, "Data Management")
        
        # Appearance tab
        appearance_widget = self.create_appearance_widget()
        self.tabs.addTab(appearance_widget, "Appearance")
        
        layout.addWidget(self.tabs)
        layout.addStretch()
        self.setLayout(layout)
    
    def create_security_widget(self):
        """Create security settings widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Change Password section
        password_section = QFrame()
        password_section.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        password_layout = QVBoxLayout()
        password_layout.setSpacing(15)
        
        password_title = QLabel("Change Password")
        password_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        password_layout.addWidget(password_title)
        
        desc = QLabel("Update your password for enhanced security. Recommended to use a strong, unique password.")
        desc.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 15px;")
        desc.setWordWrap(True)
        password_layout.addWidget(desc)
        
        # Current Password
        current_pwd_layout = QHBoxLayout()
        current_pwd_label = QLabel("Current Password:")
        current_pwd_label.setFixedWidth(150)
        current_pwd_layout.addWidget(current_pwd_label)
        self.current_pwd_input = QLineEdit()
        self.current_pwd_input.setEchoMode(QLineEdit.Password)
        current_pwd_layout.addWidget(self.current_pwd_input)
        password_layout.addLayout(current_pwd_layout)
        
        # New Password
        new_pwd_layout = QHBoxLayout()
        new_pwd_label = QLabel("New Password:")
        new_pwd_label.setFixedWidth(150)
        new_pwd_layout.addWidget(new_pwd_label)
        self.new_pwd_input = QLineEdit()
        self.new_pwd_input.setEchoMode(QLineEdit.Password)
        new_pwd_layout.addWidget(self.new_pwd_input)
        password_layout.addLayout(new_pwd_layout)
        
        # Confirm Password
        confirm_pwd_layout = QHBoxLayout()
        confirm_pwd_label = QLabel("Confirm New Password:")
        confirm_pwd_label.setFixedWidth(150)
        confirm_pwd_layout.addWidget(confirm_pwd_label)
        self.confirm_pwd_input = QLineEdit()
        self.confirm_pwd_input.setEchoMode(QLineEdit.Password)
        confirm_pwd_layout.addWidget(self.confirm_pwd_input)
        password_layout.addLayout(confirm_pwd_layout)
        
        # Buttons
        pwd_button_layout = QHBoxLayout()
        pwd_button_layout.addStretch()
        cancel_pwd_btn = QPushButton("Cancel")
        cancel_pwd_btn.setStyleSheet("""
            QPushButton {
                background: white;
                color: #4A90E2;
                border: 2px solid #4A90E2;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        cancel_pwd_btn.clicked.connect(self.clear_password_form)
        pwd_button_layout.addWidget(cancel_pwd_btn)
        
        save_pwd_btn = QPushButton("Save Changes")
        save_pwd_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        save_pwd_btn.clicked.connect(self.change_password)
        pwd_button_layout.addWidget(save_pwd_btn)
        password_layout.addLayout(pwd_button_layout)
        
        password_section.setLayout(password_layout)
        layout.addWidget(password_section)
        
        # Manage Users section
        users_section = QFrame()
        users_section.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        users_layout = QVBoxLayout()
        users_layout.setSpacing(15)
        
        users_title_layout = QHBoxLayout()
        users_title = QLabel("Manage Users")
        users_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        users_title_layout.addWidget(users_title)
        users_title_layout.addStretch()
        
        add_user_btn = QPushButton("+ Add User")
        add_user_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
        """)
        add_user_btn.clicked.connect(self.show_add_user_dialog)
        users_title_layout.addWidget(add_user_btn)
        users_layout.addLayout(users_title_layout)
        
        desc2 = QLabel("Add, edit, or remove user accounts.")
        desc2.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 15px;")
        users_layout.addWidget(desc2)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(["Username", "Role", "Actions"])
        self.users_table.horizontalHeader().setStretchLastSection(True)
        self.users_table.setAlternatingRowColors(True)
        users_layout.addWidget(self.users_table)
        
        users_section.setLayout(users_layout)
        layout.addWidget(users_section)
        
        layout.addStretch()
        widget.setLayout(layout)
        
        # Load users
        self.load_users()
        
        return widget
    
    def create_data_widget(self):
        """Create data management widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        backup_section = QFrame()
        backup_section.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        backup_layout = QVBoxLayout()
        backup_layout.setSpacing(15)
        
        backup_title = QLabel("Database Backup & Restore")
        backup_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        backup_layout.addWidget(backup_title)
        
        desc = QLabel("Backup your database to prevent data loss or restore from a previous backup.")
        desc.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 15px;")
        desc.setWordWrap(True)
        backup_layout.addWidget(desc)
        
        button_layout = QHBoxLayout()
        backup_btn = QPushButton("Backup Database")
        backup_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        backup_btn.clicked.connect(self.backup_database)
        button_layout.addWidget(backup_btn)
        
        restore_btn = QPushButton("Restore Database")
        restore_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        restore_btn.clicked.connect(self.restore_database)
        button_layout.addWidget(restore_btn)
        
        backup_layout.addLayout(button_layout)
        backup_section.setLayout(backup_layout)
        layout.addWidget(backup_section)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_appearance_widget(self):
        """Create appearance settings widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        theme_section = QFrame()
        theme_section.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        theme_layout = QVBoxLayout()
        theme_layout.setSpacing(15)
        
        theme_title = QLabel("Theme Settings")
        theme_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        theme_layout.addWidget(theme_title)
        
        desc = QLabel("Choose between light and dark mode for the application interface.")
        desc.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 15px;")
        desc.setWordWrap(True)
        theme_layout.addWidget(desc)
        
        button_layout = QHBoxLayout()
        light_btn = QPushButton("Light Mode")
        light_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        light_btn.clicked.connect(lambda: self.set_theme("light"))
        button_layout.addWidget(light_btn)
        
        dark_btn = QPushButton("Dark Mode")
        dark_btn.setStyleSheet("""
            QPushButton {
                background: #2c3e50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        dark_btn.clicked.connect(lambda: self.set_theme("dark"))
        button_layout.addWidget(dark_btn)
        
        theme_layout.addLayout(button_layout)
        theme_section.setLayout(theme_layout)
        layout.addWidget(theme_section)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def change_password(self):
        """Change user password"""
        current = self.current_pwd_input.text()
        new = self.new_pwd_input.text()
        confirm = self.confirm_pwd_input.text()
        
        if not current or not new or not confirm:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
        
        if new != confirm:
            QMessageBox.warning(self, "Error", "New password and confirmation do not match.")
            return
        
        if len(new) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters long.")
            return
        
        success = self.db.change_password(self.user_data['username'], current, new)
        if success:
            QMessageBox.information(self, "Success", "Password changed successfully!")
            self.clear_password_form()
        else:
            QMessageBox.warning(self, "Error", "Current password is incorrect.")
    
    def clear_password_form(self):
        """Clear password form"""
        self.current_pwd_input.clear()
        self.new_pwd_input.clear()
        self.confirm_pwd_input.clear()
    
    def load_users(self):
        """Load users into table"""
        users = self.db.get_all_users()
        self.users_table.setRowCount(len(users))
        
        for i, user in enumerate(users):
            self.users_table.setItem(i, 0, QTableWidgetItem(user['username']))
            self.users_table.setItem(i, 1, QTableWidgetItem(user['role']))
            
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
            edit_btn.clicked.connect(lambda checked, uid=user['id']: self.edit_user(uid))
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
            delete_btn.clicked.connect(lambda checked, uid=user['id']: self.delete_user(uid))
            action_layout.addWidget(delete_btn)
            
            action_widget.setLayout(action_layout)
            self.users_table.setCellWidget(i, 2, action_widget)
        
        self.users_table.resizeColumnsToContents()
    
    def show_add_user_dialog(self):
        """Show add user dialog"""
        dialog = AddUserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()
    
    def edit_user(self, user_id):
        """Edit user"""
        QMessageBox.information(self, "Info", "Edit user functionality would be implemented here.")
    
    def delete_user(self, user_id):
        """Delete user"""
        reply = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this user?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success = self.db.delete_user(user_id)
            if success:
                QMessageBox.information(self, "Success", "User deleted successfully!")
                self.load_users()
            else:
                QMessageBox.warning(self, "Error", "Cannot delete admin user or user not found.")
    
    def backup_database(self):
        """Backup database"""
        QMessageBox.information(self, "Backup", "Database backup functionality would be implemented here.")
    
    def restore_database(self):
        """Restore database"""
        QMessageBox.information(self, "Restore", "Database restore functionality would be implemented here.")
    
    def set_theme(self, theme):
        """Set application theme"""
        QMessageBox.information(self, "Theme", f"{theme.capitalize()} mode would be applied here.")
    
    def refresh_data(self):
        """Refresh settings data"""
        self.load_users()

class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.setWindowTitle("Add User")
        self.setFixedSize(400, 250)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Add New User")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setFixedWidth(100)
        username_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setFixedWidth(100)
        password_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # Role
        role_layout = QHBoxLayout()
        role_label = QLabel("Role:")
        role_label.setFixedWidth(100)
        role_layout.addWidget(role_label)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Operator"])
        role_layout.addWidget(self.role_combo)
        layout.addLayout(role_layout)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        add_btn = QPushButton("Add User")
        add_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        add_btn.clicked.connect(self.add_user)
        button_layout.addWidget(add_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def add_user(self):
        """Add user to database"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters long.")
            return
        
        success = self.db.add_user(username, password, role)
        if success:
            QMessageBox.information(self, "Success", "User added successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Username already exists.")

