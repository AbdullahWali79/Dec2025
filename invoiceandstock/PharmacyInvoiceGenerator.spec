# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['invoicegeneratorforphramacy'],
    pathex=[],
    binaries=[],
    datas=[('medicines.xlsx', '.'), ('secure_machine_validator.py', '.')],
    hiddenimports=['pandas', 'reportlab', 'openpyxl', 'tkinter', 'secure_machine_validator'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PharmacyInvoiceGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
