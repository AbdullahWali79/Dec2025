# Pharmacy Invoice Generator - Build Instructions

## Prerequisites
1. Python 3.7 or higher
2. All required packages (see requirements.txt)

## Building the Executable

### Method 1: Using this build script
```bash
python build_exe.py
```

### Method 2: Manual build
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Build executable:
   ```bash
   pyinstaller --onefile --windowed --name PharmacyInvoiceGenerator invoicegeneratorforphramacy
   ```

## Machine ID Management

### Adding New Machines
1. Run the application on the target machine
2. Note the Machine ID shown in the error message
3. Add the Machine ID to `authorized_machines.json`

### Managing Authorized Machines
- Edit `authorized_machines.json` to add/remove machine IDs
- Each machine ID should be associated with a descriptive name

## Distribution
1. Copy the entire `dist` folder to the target machine
2. Ensure `medicines.xlsx` is present
3. Run `PharmacyInvoiceGenerator.exe`

## Security Notes
- Keep `authorized_machines.json` secure
- Machine IDs are generated based on hardware characteristics
- The application will not run on unauthorized machines
