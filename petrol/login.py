"""
Login module for Petrol Pump Management System
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from database import Database

class LoginWindow(QWidget):
    login_successful = pyqtSignal(dict)  # Emits user data on successful login
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Petrol Pump Management - Login")
        self.setFixedSize(450, 500)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f0f0, stop:1 #e0e0e0);
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border: 2px solid #4A90E2;
            }
            QPushButton {
                padding: 12px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#loginBtn {
                background: #4A90E2;
                color: white;
            }
            QPushButton#loginBtn:hover {
                background: #357ABD;
            }
            QPushButton#resetBtn {
                background: white;
                color: #4A90E2;
                border: 2px solid #4A90E2;
            }
            QPushButton#resetBtn:hover {
                background: #f0f0f0;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Welcome Back")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Login to your account")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; font-size: 14px; margin-bottom: 30px;")
        layout.addWidget(subtitle)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding-left: 35px;
            }
        """)
        layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setStyleSheet("font-weight: bold; color: #333; margin-top: 15px;")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding-left: 35px;
            }
        """)
        layout.addWidget(self.password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.login_btn = QPushButton("Login")
        self.login_btn.setObjectName("loginBtn")
        self.login_btn.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_btn)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setObjectName("resetBtn")
        self.reset_btn.clicked.connect(self.handle_reset)
        button_layout.addWidget(self.reset_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        # Footer
        footer = QLabel("Developed by : M Abdullah (03046983794)")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #95a5a6; font-size: 12px; margin-top: 20px;")
        layout.addWidget(footer)
        
        self.setLayout(layout)
        
        # Center window
        self.center_window()
        
        # Set focus
        self.username_input.setFocus()
        
        # Enter key support
        self.password_input.returnPressed.connect(self.handle_login)
    
    def center_window(self):
        """Center the window on screen"""
        from PyQt5.QtWidgets import QDesktopWidget
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Login Error", 
                              "Please enter both username and password.")
            return
        
        user = self.db.authenticate_user(username, password)
        if user:
            self.login_successful.emit(user)
        else:
            QMessageBox.warning(self, "Login Error", 
                              "Invalid username or password. Please try again.")
            self.password_input.clear()
            self.password_input.setFocus()
    
    def handle_reset(self):
        """Handle reset button click"""
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()

