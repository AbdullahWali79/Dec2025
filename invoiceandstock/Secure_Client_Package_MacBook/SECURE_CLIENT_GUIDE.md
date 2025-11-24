# 🔒 Secure Pharmacy Invoice Generator - Client Package

## 🛡️ Security Features
This is a **SECURE** version of the Pharmacy Invoice Generator with the following security measures:

- ✅ **Hardcoded Machine IDs**: Machine authorization is embedded in the code
- ✅ **No JSON Files**: Client cannot modify authorization files
- ✅ **Tamper-Proof**: Client cannot add unauthorized machines
- ✅ **Secure Validation**: Machine IDs are hardcoded and cannot be changed

## 📦 Package Contents
- `invoicegeneratorforphramacy` - Main application
- `medicines.xlsx` - Medicine database
- `secure_machine_validator.py` - Secure machine validation (CANNOT be modified)
- `SECURE_CLIENT_GUIDE.md` - This guide
- `requirements.txt` - Python dependencies

## 🚀 Installation

### Step 1: Install Python
1. Download Python from https://www.python.org/downloads/
2. Install Python 3.8 or higher
3. Make sure to check "Add Python to PATH" during installation

### Step 2: Install Dependencies
```bash
pip install pandas reportlab openpyxl
```

### Step 3: Run Application
```bash
python invoicegeneratorforphramacy
```

## 🔐 Security Information

### Authorized Machine
- **Machine ID**: `ac:c9:06:09:93:e5` (MacBook Client)
- **Status**: Pre-authorized and embedded in code
- **Security**: Cannot be modified by client

### What Client CANNOT Do:
- ❌ Cannot modify machine IDs
- ❌ Cannot add new machines
- ❌ Cannot change authorization
- ❌ Cannot run on unauthorized machines

### What Client CAN Do:
- ✅ Use the application normally
- ✅ Add medicines and create invoices
- ✅ Export data (if authorized)
- ✅ Update medicine stock

## 🎯 Features
- **Invoice Generation**: Create professional PDF receipts
- **Medicine Management**: Add, update, and track medicine stock
- **Multi-Currency**: Support for PKR, USD, EUR, GBP
- **Export Data**: Export client data in multiple formats
- **Thermal Printing**: Direct thermal printer support
- **Keyboard Shortcuts**: Fast operation with F-keys

## 🔧 Troubleshooting

### "Unauthorized Machine" Error
- This means the application is running on an unauthorized machine
- Contact your system administrator
- Provide your Machine ID for authorization

### Application Won't Start
1. Check Python installation: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure all files are in the same folder

## 📞 Support
For technical support, contact your system administrator with:
- Your Machine ID: `ac:c9:06:09:93:e5`
- Error messages (if any)
- System information

## ⚠️ Important Security Notes
- **DO NOT** attempt to modify `secure_machine_validator.py`
- **DO NOT** try to add machine IDs to the code
- **DO NOT** share this package with unauthorized users
- Any unauthorized modifications will be detected

---
**Client**: MacBook Client  
**Machine ID**: `ac:c9:06:09:93:e5`  
**Security Level**: Maximum  
**Package Version**: Secure 1.0
