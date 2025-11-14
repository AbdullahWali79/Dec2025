# Petrol Pump Management System

A comprehensive desktop application for managing petrol pump operations built with Python, SQLite, and PyQt5.

## Features

### 🏠 Login & Access Control
- Secure login with username and password
- Role-based access (Admin vs Operator)
- Password reset functionality
- Session management

### 📊 Dashboard
- Real-time KPIs (Today's Sales, Fuel Sold, Stock Levels, Pending Payments)
- Sales trend charts
- Quick action buttons
- User profile display

### ⛽ Fuel Stock Management
- View all fuel types with rates and stock levels
- Add new stock entries
- Update fuel rates
- Low stock alerts
- Stock history tracking

### 💵 Sales Management
- Create new sale entries
- Auto-calculate totals
- Support for Cash and Credit sales
- Customer selection
- Receipt printing
- Daily sales tracking

### 👥 Customer Management
- Separate tabs for Regular Customers and Distributors
- Add new customers with opening balance
- View outstanding balances
- Quick access to customer ledger

### 📒 Ledger Management
- View customer transaction history
- Add credit (sale) entries
- Add payment (debit) entries
- Date range filtering
- Export to PDF/Excel
- Running balance calculation

### 💰 Expense Management
- Categorize expenses
- Track daily and monthly totals
- Expense history
- Grand total calculation

### 📈 Reports
- Daily, Monthly, and Custom Range reports
- Sales vs Expenses comparison
- Detailed transaction reports
- Export to PDF/Excel

### ⚙️ Settings
- Change password
- Manage users (add/edit/delete)
- Database backup and restore
- Theme settings (Light/Dark mode)

## Installation

1. Install Python 3.7 or higher

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### Default Login Credentials
- **Username:** admin
- **Password:** admin123

## Database

The application uses SQLite database (`petrolpump.db`) with the following tables:
- `users` - User accounts and authentication
- `fuel_types` - Fuel inventory and rates
- `customers` - Customer information
- `sales` - Sales transactions
- `ledger_entries` - Customer ledger entries
- `expenses` - Expense records
- `stock_history` - Stock update history

## Project Structure

```
petrol/
├── main.py              # Application entry point
├── database.py          # Database operations
├── login.py             # Login window
├── main_window.py       # Main application window
├── dashboard.py         # Dashboard widget
├── sales.py             # Sales management
├── customers.py         # Customer management
├── ledger.py            # Ledger management
├── fuel_stock.py        # Fuel stock management
├── expenses.py          # Expense management
├── reports.py           # Reports generation
├── settings.py          # Settings management
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Features Verification Checklist

✅ All features from the verification checklist are implemented:
- Login & Access Control
- Dashboard with KPIs and charts
- Fuel Stock Management
- Sales Module with auto-calculation
- Customer Management with tabs
- Ledger with credit/debit entries
- Expense Management
- Reports with multiple date ranges
- Settings with user management
- Logout with confirmation
- Complete SQLite database schema

## Notes

- The application creates the database automatically on first run
- Default fuel types (Petrol, Diesel, CNG) are created with sample data
- All monetary values support both ₹ (Rupees) and $ (Dollars) formatting
- Export functionality (PDF/Excel) shows placeholder messages - full implementation would require additional libraries

## License

This project is developed for educational and commercial use.

