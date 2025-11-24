# 🏗️ Build Instructions - Pharmacy Invoice Generator

## 📋 Prerequisites

1. **Python 3.7 or higher** installed on your system
2. **Windows OS** (recommended for thermal printing support)
3. **Administrator privileges** (for some installations)

## 🚀 Quick Build Process

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Build Executable
```bash
python build_exe.py
```

### Step 3: Test the Build
```bash
cd dist
PharmacyInvoiceGenerator.exe
```

## 🔧 Detailed Build Process

### Method 1: Using Build Script (Recommended)

1. **Run the build script:**
   ```bash
   python build_exe.py
   ```

2. **The script will:**
   - Install all required packages
   - Create PyInstaller spec file
   - Build the executable
   - Create distribution folder

3. **Output location:**
   - Executable: `dist/PharmacyInvoiceGenerator.exe`
   - All required files in `dist/` folder

### Method 2: Manual Build

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Build with basic settings:**
   ```bash
   pyinstaller --onefile --windowed --name PharmacyInvoiceGenerator invoicegeneratorforphramacy
   ```

3. **Build with advanced settings:**
   ```bash
   pyinstaller --onefile --windowed --name PharmacyInvoiceGenerator --add-data "medicines.xlsx;." --add-data "machine_id_validator.py;." invoicegeneratorforphramacy
   ```

## 📦 Distribution Setup

### For Single Machine
1. Copy the entire `dist` folder to target machine
2. Ensure `medicines.xlsx` is present
3. Run `PharmacyInvoiceGenerator.exe`

### For Multiple Machines
1. Build executable on development machine
2. Copy `dist` folder to each target machine
3. Use Machine Manager to add each machine ID
4. Distribute `authorized_machines.json` to all machines

## 🔒 Machine ID Management

### Adding Your Development Machine
1. Run the application first time
2. Note the Machine ID from error message
3. Use Machine Manager:
   ```bash
   python machine_manager.py
   ```
4. Select option 3 to add current machine

### Adding Client Machines
1. Send executable to client
2. Client runs application (will show error with Machine ID)
3. Client sends Machine ID to you
4. Use Machine Manager to add client's Machine ID
5. Send updated `authorized_machines.json` to client

### Machine Manager Usage
```bash
python machine_manager.py
```

Options:
- **1**: Show current machine info
- **2**: List authorized machines
- **3**: Add current machine
- **4**: Add remote machine
- **5**: Remove machine
- **6**: Export machine list
- **7**: Exit

## 🛠️ Advanced Configuration

### Custom Icon
1. Add icon file (`.ico` format)
2. Update `PharmacyInvoiceGenerator.spec`:
   ```python
   icon='path/to/your/icon.ico'
   ```

### Console Window
1. Edit `PharmacyInvoiceGenerator.spec`:
   ```python
   console=True  # Set to True for console window
   ```

### Additional Data Files
1. Edit `PharmacyInvoiceGenerator.spec`:
   ```python
   datas=[
       ('medicines.xlsx', '.'),
       ('machine_id_validator.py', '.'),
       ('your_file.txt', '.'),
   ],
   ```

## 🔍 Troubleshooting

### Build Issues

1. **"Module not found" errors:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **PyInstaller not found:**
   ```bash
   pip install pyinstaller
   ```

3. **Permission errors:**
   - Run command prompt as Administrator
   - Check antivirus software

### Runtime Issues

1. **"Machine not authorized":**
   - Use Machine Manager to add machine
   - Check `authorized_machines.json` file

2. **"Excel file not found":**
   - Ensure `medicines.xlsx` is in same folder as executable
   - Check file permissions

3. **Application crashes:**
   - Check all dependencies are installed
   - Run from command line to see error messages

## 📁 File Structure After Build

```
dist/
├── PharmacyInvoiceGenerator.exe    # Main executable
├── medicines.xlsx                   # Medicine database
├── authorized_machines.json         # Machine authorization
└── [other PyInstaller files]
```

## 🚀 Deployment Checklist

### Before Distribution
- [ ] Test executable on development machine
- [ ] Verify all features work correctly
- [ ] Check machine ID validation
- [ ] Ensure `medicines.xlsx` is included
- [ ] Test on clean Windows machine

### For Each Client Machine
- [ ] Copy entire `dist` folder
- [ ] Add machine ID to authorized list
- [ ] Send updated `authorized_machines.json`
- [ ] Provide usage instructions

## 🔐 Security Best Practices

1. **Keep `authorized_machines.json` secure**
2. **Don't share machine IDs publicly**
3. **Regularly update authorized machine list**
4. **Use strong machine names for identification**

## 📞 Support

If you encounter issues:
1. Check this build instructions file
2. Verify all requirements are met
3. Test on clean Windows installation
4. Check PyInstaller documentation

---

**Note**: The executable is protected by machine ID validation. Only machines in the authorized list can run the application.
