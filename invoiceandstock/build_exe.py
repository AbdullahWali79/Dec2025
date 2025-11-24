"""
Build script for creating executable file of Pharmacy Invoice Generator
This script uses PyInstaller to create a standalone .exe file
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_requirements():
    """Install required packages for building"""
    requirements = [
        'pyinstaller',
        'pandas',
        'reportlab',
        'openpyxl'
    ]
    
    print("Installing build requirements...")
    for package in requirements:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
            print(f"[OK] Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install {package}: {e}")
            return False
    return True

def create_spec_file():
    """Create PyInstaller spec file for custom build configuration"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['invoicegeneratorforphramacy'],
    pathex=[],
    binaries=[],
    datas=[
        ('medicines.xlsx', '.'),
        ('secure_machine_validator.py', '.'),
    ],
    hiddenimports=[
        'pandas',
        'reportlab',
        'openpyxl',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'secure_machine_validator',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PharmacyInvoiceGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
'''
    
    with open('PharmacyInvoiceGenerator.spec', 'w') as f:
        f.write(spec_content)
    print("[OK] Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    try:
        # Build using spec file
        subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'PharmacyInvoiceGenerator.spec'
        ], check=True)
        
        print("[OK] Executable built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
        return False

def create_requirements_txt():
    """Create requirements.txt file"""
    requirements = [
        'pandas>=1.3.0',
        'reportlab>=3.6.0',
        'openpyxl>=3.0.0',
        'pyinstaller>=4.0'
    ]
    
    with open('requirements.txt', 'w') as f:
        f.write('\n'.join(requirements))
    print("[OK] Created requirements.txt")

def create_build_instructions():
    """Create build instructions file"""
    instructions = """# Pharmacy Invoice Generator - Build Instructions

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
"""
    
    with open('BUILD_INSTRUCTIONS.md', 'w') as f:
        f.write(instructions)
    print("[OK] Created build instructions")

def main():
    """Main build process"""
    print("=" * 60)
    print("Pharmacy Invoice Generator - Build Script")
    print("=" * 60)
    
    # Check if main files exist
    if not os.path.exists('invoicegeneratorforphramacy'):
        print("[ERROR] Main application file not found!")
        return False
    
    if not os.path.exists('secure_machine_validator.py'):
        print("[ERROR] Machine ID validator not found!")
        return False
    
    # Install requirements
    if not install_requirements():
        print("[ERROR] Failed to install requirements!")
        return False
    
    # Create spec file
    create_spec_file()
    
    # Create requirements.txt
    create_requirements_txt()
    
    # Create build instructions
    create_build_instructions()
    
    # Build executable
    if build_executable():
        print("\n" + "=" * 60)
        print("BUILD SUCCESSFUL!")
        print("=" * 60)
        print("Executable location: dist/PharmacyInvoiceGenerator.exe")
        print("Copy the entire 'dist' folder to distribute the application")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("BUILD FAILED!")
        print("=" * 60)
        return False

if __name__ == "__main__":
    main()
