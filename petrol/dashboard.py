"""
Dashboard widget showing KPIs and sales trends
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import Database

# Try to import PyQtChart, fallback if not available
try:
    from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
    CHART_AVAILABLE = True
except ImportError:
    CHART_AVAILABLE = False
    # Create dummy classes for fallback
    class QChartView(QWidget):
        pass
    class QChart:
        pass
    class QLineSeries:
        pass
    class QValueAxis:
        pass

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Dashboard Overview")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Quick action buttons
        add_expense_btn = QPushButton("+ Add Expense")
        add_expense_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        header_layout.addWidget(add_expense_btn)
        
        add_sale_btn = QPushButton("+ Add Sale")
        add_sale_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        header_layout.addWidget(add_sale_btn)
        
        layout.addLayout(header_layout)
        
        # Welcome message
        welcome = QLabel("Welcome back, here's your summary for today.")
        welcome.setStyleSheet("color: #666; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(welcome)
        
        # KPI Cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        
        self.todays_sales_card = self.create_kpi_card("Today's Sales", "Rs. 0", "+0% vs yesterday")
        self.fuel_sold_card = self.create_kpi_card("Total Fuel Sold", "0 L", "+0% vs yesterday")
        self.current_stock_card = self.create_kpi_card("Current Fuel Stock", "0 L", "+0% vs last week")
        self.pending_payments_card = self.create_kpi_card("Pending Payments", "Rs. 0", "+0% vs last week")
        
        cards_layout.addWidget(self.todays_sales_card, 1)
        cards_layout.addWidget(self.fuel_sold_card, 1)
        cards_layout.addWidget(self.current_stock_card, 1)
        cards_layout.addWidget(self.pending_payments_card, 1)
        
        layout.addLayout(cards_layout)
        
        # Sales trend chart
        chart_label = QLabel("Daily Sales Trend (Last 7 Days)")
        chart_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 10px;")
        layout.addWidget(chart_label)
        
        # Chart container
        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        chart_layout = QVBoxLayout()
        chart_layout.setContentsMargins(10, 10, 10, 10)
        
        self.chart_view = QChartView()
        self.chart_view.setMinimumHeight(300)
        self.chart_view.setMaximumHeight(400)
        chart_layout.addWidget(self.chart_view)
        
        chart_frame.setLayout(chart_layout)
        layout.addWidget(chart_frame, 0)
        
        self.setLayout(layout)
    
    def create_kpi_card(self, title, value, trend):
        """Create a KPI card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 5px;
                padding: 20px;
            }
            QLabel {
                color: #333;
            }
        """)
        card.setMinimumHeight(140)
        card.setMaximumHeight(160)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 13px; font-weight: bold;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(22)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: #2c3e50; margin: 5px 0px;")
        value_label.setWordWrap(True)
        layout.addWidget(value_label)
        
        trend_label = QLabel(trend)
        trend_label.setStyleSheet("color: #27ae60; font-size: 11px; margin-top: 5px;")
        trend_label.setWordWrap(True)
        layout.addWidget(trend_label)
        
        layout.addStretch()
        card.setLayout(layout)
        
        # Store labels for updates
        card.value_label = value_label
        card.trend_label = trend_label
        
        return card
    
    def refresh_data(self):
        """Refresh dashboard data"""
        # Update KPI cards
        todays_sales = self.db.get_todays_sales()
        self.todays_sales_card.value_label.setText(f"Rs. {todays_sales:,.2f}")
        
        fuel_sold = self.db.get_todays_fuel_sold()
        self.fuel_sold_card.value_label.setText(f"{fuel_sold:,.1f} L")
        
        total_stock = self.db.get_total_stock()
        self.current_stock_card.value_label.setText(f"{total_stock:,.1f} L")
        
        pending = self.db.get_pending_payments()
        self.pending_payments_card.value_label.setText(f"Rs. {pending:,.2f}")
        
        # Update chart
        self.update_chart()
    
    def update_chart(self):
        """Update sales trend chart"""
        if not CHART_AVAILABLE:
            # If PyQtChart is not available, show a placeholder
            if isinstance(self.chart_view, QLabel):
                return  # Already showing placeholder
            self.chart_view.setStyleSheet("background: #f0f0f0;")
            label = QLabel("Chart visualization requires PyQtChart\nInstall with: pip install PyQtChart")
            label.setAlignment(Qt.AlignCenter)
            old_view = self.chart_view
            self.chart_view = label
            layout = self.layout()
            for i in range(layout.count()):
                if layout.itemAt(i).widget() == old_view:
                    layout.removeWidget(old_view)
                    old_view.setParent(None)
                    layout.insertWidget(i, label)
                    break
            return
        
        try:
            chart = QChart()
            chart.setTitle("Daily Sales Trend")
            chart.setTheme(QChart.ChartThemeLight)
            
            # Get sales data
            sales_data = self.db.get_sales_trend(7)
            
            series = QLineSeries()
            series.setName("Sales")
            
            max_value = 0
            for i, data in enumerate(sales_data):
                value = data['total']
                series.append(i, value)
                max_value = max(max_value, value)
            
            if max_value == 0:
                max_value = 100
            
            chart.addSeries(series)
            
            # Create axes
            axis_x = QValueAxis()
            axis_x.setRange(0, max(len(sales_data) - 1, 1))
            axis_x.setTitleText("Days")
            chart.addAxis(axis_x, Qt.AlignBottom)
            series.attachAxis(axis_x)
            
            axis_y = QValueAxis()
            axis_y.setRange(0, max_value * 1.1)
            axis_y.setTitleText("Amount (Rs.)")
            chart.addAxis(axis_y, Qt.AlignLeft)
            series.attachAxis(axis_y)
            
            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            
            self.chart_view.setChart(chart)
        except Exception as e:
            # Fallback on any error
            if not isinstance(self.chart_view, QLabel):
                self.chart_view.setStyleSheet("background: #f0f0f0;")
                label = QLabel(f"Chart error: {str(e)}")
                label.setAlignment(Qt.AlignCenter)
                old_view = self.chart_view
                self.chart_view = label
                layout = self.layout()
                for i in range(layout.count()):
                    if layout.itemAt(i).widget() == old_view:
                        layout.removeWidget(old_view)
                        old_view.setParent(None)
                        layout.insertWidget(i, label)
                        break

