"""
Database module for Petrol Pump Management System
Handles all SQLite database operations
"""
import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Tuple

class Database:
    def __init__(self, db_name: str = "petrolpump.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'Operator',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Fuel types table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fuel_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                rate_per_litre REAL NOT NULL,
                current_stock REAL DEFAULT 0,
                low_stock_threshold REAL DEFAULT 1000,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                type TEXT NOT NULL DEFAULT 'Regular',
                address TEXT,
                opening_balance REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Sales table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                fuel_type_id INTEGER NOT NULL,
                customer_id INTEGER,
                quantity REAL NOT NULL,
                rate REAL NOT NULL,
                total REAL NOT NULL,
                payment_type TEXT NOT NULL,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fuel_type_id) REFERENCES fuel_types(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
        
        # Ledger entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ledger_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                credit REAL DEFAULT 0,
                debit REAL DEFAULT 0,
                balance REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
        
        # Expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Stock history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fuel_type_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                quantity_added REAL NOT NULL,
                previous_stock REAL NOT NULL,
                new_stock REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fuel_type_id) REFERENCES fuel_types(id)
            )
        """)
        
        conn.commit()
        self.create_default_data(cursor, conn)
        conn.close()
    
    def create_default_data(self, cursor, conn):
        """Create default admin user and fuel types"""
        # Create default admin user (password: admin123)
        import hashlib
        default_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password, role) 
            VALUES (?, ?, ?)
        """, ("admin", default_password, "Admin"))
        
        # Create default fuel types
        fuel_types = [
            ("Petrol", 1.50, 15420, 5000),
            ("Diesel", 1.45, 12150, 5000),
            ("CNG", 0.95, 3000, 2000)
        ]
        
        for name, rate, stock, threshold in fuel_types:
            cursor.execute("""
                INSERT OR IGNORE INTO fuel_types (name, rate_per_litre, current_stock, low_stock_threshold)
                VALUES (?, ?, ?, ?)
            """, (name, rate, stock, threshold))
        
        conn.commit()
    
    # User operations
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        import hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, role FROM users 
            WHERE username = ? AND password = ?
        """, (username, hashed_password))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "username": row[1], "role": row[2]}
        return None
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        import hashlib
        old_hashed = hashlib.sha256(old_password.encode()).hexdigest()
        new_hashed = hashlib.sha256(new_password.encode()).hexdigest()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET password = ? 
            WHERE username = ? AND password = ?
        """, (new_hashed, username, old_hashed))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        users = [{"id": row[0], "username": row[1], "role": row[2]} for row in cursor.fetchall()]
        conn.close()
        return users
    
    def add_user(self, username: str, password: str, role: str) -> bool:
        """Add new user"""
        import hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, password, role) 
                VALUES (?, ?, ?)
            """, (username, hashed_password, role))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        finally:
            conn.close()
        return success
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user (cannot delete admin)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user and user[0] == "admin":
            conn.close()
            return False
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # Fuel stock operations
    def get_all_fuel_types(self) -> List[Dict]:
        """Get all fuel types with current stock"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, rate_per_litre, current_stock, low_stock_threshold, last_updated
            FROM fuel_types ORDER BY name
        """)
        fuels = []
        for row in cursor.fetchall():
            fuels.append({
                "id": row[0],
                "name": row[1],
                "rate_per_litre": row[2],
                "current_stock": row[3],
                "low_stock_threshold": row[4],
                "last_updated": row[5]
            })
        conn.close()
        return fuels
    
    def update_fuel_stock(self, fuel_type_id: int, quantity_added: float) -> bool:
        """Update fuel stock"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT current_stock FROM fuel_types WHERE id = ?", (fuel_type_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False
        
        previous_stock = row[0]
        new_stock = previous_stock + quantity_added
        
        cursor.execute("""
            UPDATE fuel_types 
            SET current_stock = ?, last_updated = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_stock, fuel_type_id))
        
        # Add to stock history
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO stock_history (fuel_type_id, date, quantity_added, previous_stock, new_stock)
            VALUES (?, ?, ?, ?, ?)
        """, (fuel_type_id, today, quantity_added, previous_stock, new_stock))
        
        conn.commit()
        conn.close()
        return True
    
    def update_fuel_rate(self, fuel_type_id: int, new_rate: float) -> bool:
        """Update fuel rate"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE fuel_types 
            SET rate_per_litre = ?, last_updated = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_rate, fuel_type_id))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # Customer operations
    def get_all_customers(self, customer_type: Optional[str] = None) -> List[Dict]:
        """Get all customers, optionally filtered by type"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if customer_type:
            cursor.execute("""
                SELECT id, name, phone, type, address, opening_balance
                FROM customers WHERE type = ? ORDER BY name
            """, (customer_type,))
        else:
            cursor.execute("""
                SELECT id, name, phone, type, address, opening_balance
                FROM customers ORDER BY name
            """)
        customers = []
        for row in cursor.fetchall():
            # Calculate outstanding balance
            cursor.execute("""
                SELECT COALESCE(SUM(credit - debit), 0) + ? as balance
                FROM ledger_entries WHERE customer_id = ?
            """, (row[5], row[0]))
            balance_row = cursor.fetchone()
            outstanding = balance_row[0] if balance_row else row[5]
            
            customers.append({
                "id": row[0],
                "name": row[1],
                "phone": row[2] or "",
                "type": row[3],
                "address": row[4] or "",
                "opening_balance": row[5],
                "outstanding_balance": outstanding
            })
        conn.close()
        return customers
    
    def add_customer(self, name: str, phone: str, customer_type: str, address: str, opening_balance: float) -> int:
        """Add new customer and create initial ledger entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO customers (name, phone, type, address, opening_balance)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, customer_type, address, opening_balance))
        customer_id = cursor.lastrowid
        
        # Create initial ledger entry for opening balance
        if opening_balance != 0:
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("""
                INSERT INTO ledger_entries (customer_id, date, description, credit, debit, balance)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (customer_id, today, "Initial Balance", 
                  0 if opening_balance < 0 else opening_balance,
                  abs(opening_balance) if opening_balance < 0 else 0,
                  opening_balance))
        
        conn.commit()
        conn.close()
        return customer_id
    
    # Sales operations
    def add_sale(self, date: str, fuel_type_id: int, customer_id: Optional[int], 
                 quantity: float, rate: float, total: float, payment_type: str, remarks: str) -> int:
        """Add new sale and update stock/ledger"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Add sale record
        cursor.execute("""
            INSERT INTO sales (date, fuel_type_id, customer_id, quantity, rate, total, payment_type, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (date, fuel_type_id, customer_id, quantity, rate, total, payment_type, remarks))
        sale_id = cursor.lastrowid
        
        # Update fuel stock (reduce)
        cursor.execute("SELECT current_stock FROM fuel_types WHERE id = ?", (fuel_type_id,))
        row = cursor.fetchone()
        if row:
            new_stock = row[0] - quantity
            cursor.execute("""
                UPDATE fuel_types 
                SET current_stock = ?, last_updated = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_stock, fuel_type_id))
        
        # If credit sale, update customer ledger
        if payment_type == "Credit" and customer_id:
            cursor.execute("""
                SELECT COALESCE(MAX(balance), 0) FROM ledger_entries WHERE customer_id = ?
            """, (customer_id,))
            row = cursor.fetchone()
            previous_balance = row[0] if row else 0
            
            # Get customer opening balance if no ledger entries
            if previous_balance == 0:
                cursor.execute("SELECT opening_balance FROM customers WHERE id = ?", (customer_id,))
                row = cursor.fetchone()
                if row:
                    previous_balance = row[0]
            
            new_balance = previous_balance + total
            
            cursor.execute("""
                INSERT INTO ledger_entries (customer_id, date, description, credit, debit, balance)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (customer_id, date, f"Fuel Purchase - {quantity}L", total, 0, new_balance))
        
        conn.commit()
        conn.close()
        return sale_id
    
    def get_sales(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                  customer_id: Optional[int] = None) -> List[Dict]:
        """Get sales with optional filters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT s.id, s.date, s.quantity, s.rate, s.total, s.payment_type, s.remarks,
                   ft.name as fuel_type, c.name as customer_name
            FROM sales s
            JOIN fuel_types ft ON s.fuel_type_id = ft.id
            LEFT JOIN customers c ON s.customer_id = c.id
            WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND s.date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND s.date <= ?"
            params.append(end_date)
        if customer_id:
            query += " AND s.customer_id = ?"
            params.append(customer_id)
        
        query += " ORDER BY s.date DESC, s.id DESC"
        cursor.execute(query, params)
        
        sales = []
        for row in cursor.fetchall():
            sales.append({
                "id": row[0],
                "date": row[1],
                "quantity": row[2],
                "rate": row[3],
                "total": row[4],
                "payment_type": row[5],
                "remarks": row[6] or "",
                "fuel_type": row[7],
                "customer_name": row[8] or "Walk-in Customer"
            })
        conn.close()
        return sales
    
    # Ledger operations
    def get_ledger_entries(self, customer_id: int, start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> List[Dict]:
        """Get ledger entries for a customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT id, date, description, credit, debit, balance
            FROM ledger_entries
            WHERE customer_id = ?
        """
        params = [customer_id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date ASC, id ASC"
        cursor.execute(query, params)
        
        entries = []
        for row in cursor.fetchall():
            entries.append({
                "id": row[0],
                "date": row[1],
                "description": row[2],
                "credit": row[3],
                "debit": row[4],
                "balance": row[5]
            })
        conn.close()
        return entries
    
    def get_customer_balance(self, customer_id: int) -> float:
        """Get current balance for a customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COALESCE(MAX(balance), 0) FROM ledger_entries WHERE customer_id = ?
        """, (customer_id,))
        row = cursor.fetchone()
        balance = row[0] if row else 0
        
        # If no ledger entries, return opening balance
        if balance == 0:
            cursor.execute("SELECT opening_balance FROM customers WHERE id = ?", (customer_id,))
            row = cursor.fetchone()
            if row:
                balance = row[0]
        
        conn.close()
        return balance
    
    def add_ledger_entry(self, customer_id: int, date: str, description: str,
                        credit: float, debit: float) -> bool:
        """Add ledger entry and update balance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get previous balance
        previous_balance = self.get_customer_balance(customer_id)
        new_balance = previous_balance + credit - debit
        
        cursor.execute("""
            INSERT INTO ledger_entries (customer_id, date, description, credit, debit, balance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (customer_id, date, description, credit, debit, new_balance))
        
        conn.commit()
        conn.close()
        return True
    
    # Expense operations
    def add_expense(self, date: str, category: str, amount: float, remarks: str) -> int:
        """Add new expense"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (date, category, amount, remarks)
            VALUES (?, ?, ?, ?)
        """, (date, category, amount, remarks))
        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return expense_id
    
    def get_expenses(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict]:
        """Get expenses with optional date filter"""
        conn = self.get_connection()
        cursor = conn.cursor()
        query = "SELECT id, date, category, amount, remarks FROM expenses WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date DESC, id DESC"
        cursor.execute(query, params)
        
        expenses = []
        for row in cursor.fetchall():
            expenses.append({
                "id": row[0],
                "date": row[1],
                "category": row[2],
                "amount": row[3],
                "remarks": row[4] or ""
            })
        conn.close()
        return expenses
    
    def get_expense_total(self, date: Optional[str] = None) -> float:
        """Get total expenses for a date or all time"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if date:
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date = ?", (date,))
        else:
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
        row = cursor.fetchone()
        total = row[0] if row else 0.0
        conn.close()
        return total
    
    # Dashboard statistics
    def get_todays_sales(self) -> float:
        """Get today's total sales"""
        today = datetime.now().strftime("%Y-%m-%d")
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM sales WHERE date = ?", (today,))
        row = cursor.fetchone()
        total = row[0] if row else 0.0
        conn.close()
        return total
    
    def get_todays_fuel_sold(self) -> float:
        """Get today's total fuel sold in liters"""
        today = datetime.now().strftime("%Y-%m-%d")
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM sales WHERE date = ?", (today,))
        row = cursor.fetchone()
        total = row[0] if row else 0.0
        conn.close()
        return total
    
    def get_total_stock(self) -> float:
        """Get total current fuel stock"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(current_stock), 0) FROM fuel_types")
        row = cursor.fetchone()
        total = row[0] if row else 0.0
        conn.close()
        return total
    
    def get_pending_payments(self) -> float:
        """Get total pending payments (negative balances)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(balance), 0) 
            FROM (
                SELECT customer_id, MAX(balance) as balance
                FROM ledger_entries
                GROUP BY customer_id
                UNION
                SELECT id as customer_id, opening_balance as balance
                FROM customers
                WHERE id NOT IN (SELECT DISTINCT customer_id FROM ledger_entries)
            )
            WHERE balance < 0
        """)
        row = cursor.fetchone()
        total = abs(row[0]) if row and row[0] < 0 else 0.0
        conn.close()
        return total
    
    def get_sales_trend(self, days: int = 7) -> List[Dict]:
        """Get sales trend for last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, COALESCE(SUM(total), 0) as total
            FROM sales
            WHERE date >= date('now', '-' || ? || ' days')
            GROUP BY date
            ORDER BY date ASC
        """, (days,))
        
        trends = []
        for row in cursor.fetchall():
            trends.append({
                "date": row[0],
                "total": row[1]
            })
        conn.close()
        return trends
    
    def get_expenses_trend(self, days: int = 7) -> List[Dict]:
        """Get expenses trend for last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, COALESCE(SUM(amount), 0) as total
            FROM expenses
            WHERE date >= date('now', '-' || ? || ' days')
            GROUP BY date
            ORDER BY date ASC
        """, (days,))
        
        trends = []
        for row in cursor.fetchall():
            trends.append({
                "date": row[0],
                "total": row[1]
            })
        conn.close()
        return trends

