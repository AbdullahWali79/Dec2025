"""
Main entry point for Petrol Pump Management System
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from login import LoginWindow
from main_window import MainWindow

class PetrolPumpApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        self.login_window = None
        self.main_window = None
    
    def show_login(self):
        """Show login window"""
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        self.login_window.close()
        self.main_window = MainWindow(user_data)
        self.main_window.logout_requested.connect(self.on_logout)
        self.main_window.showMaximized()
    
    def on_logout(self):
        """Handle logout"""
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        self.show_login()
    
    def run(self):
        """Run the application"""
        self.show_login()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = PetrolPumpApp()
    app.run()

