# -*- coding: utf-8 -*-
# build_spec.spec
"""
PyInstaller Spec File für ProgGUI
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent

block_cipher = None

a = Analysis(
    [str(project_root / "run.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(project_root / "data"), "data"),
        (str(project_root / "src"), "src"),
    ],
    hiddenimports=[
        "tkinter",
        "tkinter.ttk",
        "sqlite3",
        "configparser",
        "logging",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
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
    name="ProgGUI",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No Console
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / "data" / "icon.png"),
)