# 🏥 Pharmacy Invoice Generator

A professional pharmacy invoice generator with machine ID protection and thermal printing support.

## ✨ Features

- **Modern UI**: Beautiful, responsive interface with gradient styling
- **Medicine Management**: Search and manage medicine inventory
- **Invoice Generation**: Create professional PDF receipts
- **Thermal Printing**: Direct thermal printer support
- **Stock Management**: Real-time stock tracking
- **Multi-Currency**: Support for PKR, USD, EUR, GBP
- **Machine Protection**: Restricted to authorized machines only
- **Keyboard Shortcuts**: Full keyboard navigation support

## 🔒 Security Features

- **Machine ID Validation**: Application only runs on authorized machines
- **Hardware-based ID**: Machine ID generated from hardware characteristics
- **Centralized Management**: Easy machine authorization management

## 📋 Requirements

- Python 3.7 or higher
- Windows OS (for thermal printing)
- Required packages (see requirements.txt)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python invoicegeneratorforphramacy
```

### 3. First Time Setup
- The application will create a sample `medicines.xlsx` file
- Add your medicine inventory to this file
- Restart the application

## 🔧 Building Executable

### Automatic Build
```bash
python build_exe.py
```

### Manual Build
```bash
pyinstaller --onefile --windowed --name PharmacyInvoiceGenerator invoicegeneratorforphramacy
```

## 🖥️ Machine ID Management

### Adding New Machines
1. Run the application on the target machine
2. Note the Machine ID from the error message
3. Use the Machine Manager tool:
   ```bash
   python machine_manager.py
   ```

### Managing Authorized Machines
- Use the Machine Manager tool for easy management
- Export machine list for backup
- Add/remove machines as needed

## 📁 File Structure

```
├── invoicegeneratorforphramacy    # Main application
├── machine_id_validator.py        # Machine ID validation
├── machine_manager.py             # Machine management tool
├── build_exe.py                   # Build script
├── requirements.txt               # Dependencies
├── medicines.xlsx                # Medicine database
└── authorized_machines.json       # Authorized machines (auto-created)
```

## ⌨️ Keyboard Shortcuts

- **F1**: Add to Invoice
- **F2**: Add/Update Stock
- **F3**: Generate PDF
- **F4**: Clear Invoice
- **F5**: Thermal Print
- **F6**: Preview Receipt
- **F11**: Toggle Fullscreen
- **Ctrl+N**: Add Stock
- **Ctrl+S**: Save Medicines
- **Ctrl+Q**: Quit Application

## 🎯 Usage Guide

### Adding Medicines
1. Click "Add/Update Stock" or press F2
2. Enter medicine name, price, and stock quantity
3. Click "Save" to update the database

### Creating Invoices
1. Search for medicine in the search box
2. Enter quantity and press Enter or click "Add to Invoice"
3. Enter customer name
4. Click "Generate PDF" or "Thermal Print"

### Stock Management
- Stock is automatically updated when items are added to invoices
- Use the stock management section to add new medicines
- Stock levels are tracked in real-time

## 🔧 Configuration

### Currency Settings
- Select currency from the dropdown (PKR, USD, EUR, GBP)
- Currency symbol updates automatically

### Machine Authorization
- Each machine has a unique ID based on hardware
- Only authorized machines can run the application
- Use Machine Manager to add/remove machines

## 📦 Distribution

### For Authorized Machines
1. Build the executable using `build_exe.py`
2. Copy the `dist` folder to target machine
3. Ensure `medicines.xlsx` is present
4. Add machine ID to authorized list

### Security Notes
- Keep `authorized_machines.json` secure
- Machine IDs are hardware-specific
- Application won't run on unauthorized machines

## 🐛 Troubleshooting

### Common Issues

1. **"Medicine not found"**
   - Check if medicine exists in `medicines.xlsx`
   - Ensure spelling matches exactly

2. **"Machine not authorized"**
   - Use Machine Manager to add current machine
   - Contact administrator for machine ID

3. **"Excel file not found"**
   - Ensure `medicines.xlsx` is in the same folder
   - Check file permissions

4. **Print issues**
   - Ensure thermal printer is connected
   - Check printer drivers

## 📞 Support

For technical support or questions:
- Check the build instructions in `BUILD_INSTRUCTIONS.md`
- Use Machine Manager for authorization issues
- Ensure all dependencies are installed

## 🔄 Updates

To update the application:
1. Replace the main application file
2. Update machine authorization if needed
3. Rebuild executable if necessary

---

**Note**: This application is protected by machine ID validation. Only authorized machines can run the application.
