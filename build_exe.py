# -*- coding: utf-8 -*-
# build_exe.py
"""
PyInstaller Build Script
- Erstellt standalone EXE für ProgGUI
- Bundelt alle Dependencies
"""

import PyInstaller.__main__
import sys
from pathlib import Path

def build_exe():
    """Erstellt die EXE mit PyInstaller."""
    
    print("=" * 60)
    print("ProgGUI PyInstaller Build")
    print("=" * 60)
    
    # Projekt-Root
    project_root = Path(__file__).parent
    
    # Pfade
    main_script = project_root / "run.py"
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    
    # PyInstaller Arguments
    args = [
        str(main_script),
        
        # Output
        f"--distpath={dist_dir}",
        f"--workpath={build_dir}",
        
        # Mode
        "--onefile",  # Single EXE
        "--windowed",  # Keine Console
        
        # Icon (optional - wenn vorhanden)
        # f"--icon={project_root / 'data' / 'icon.png'}",
        
        # Zusätzliche Files
        f"--add-data={project_root / 'data'};data",
        
        # Zusätzliche Module
        "--hidden-import=tkinter",
        "--hidden-import=sqlite3",
        "--hidden-import=configparser",
        
        # Optimierungen
        "--optimize=2",
        
        # Cleanup
        "--noconfirm",
        
        # Name
        "--name=ProgGUI",
    ]
    
    try:
        print("\n[BUILD] Starte PyInstaller...")
        print(f"[BUILD] Input: {main_script}")
        print(f"[BUILD] Output: {dist_dir}")
        print(f"[BUILD] Temp: {build_dir}")
        print()
        
        PyInstaller.__main__.run(args)
        
        exe_path = dist_dir / "ProgGUI.exe"
        
        if exe_path.exists():
            file_size_mb = exe_path.stat().st_size / (1024*1024)
            
            print()
            print("=" * 60)
            print("BUILD ERFOLGREICH!")
            print("=" * 60)
            print(f"✅ EXE erstellt: {exe_path}")
            print(f"✅ Größe: {file_size_mb:.1f} MB")
            print()
            print("Du kannst ProgGUI.exe jetzt starten!")
            print()
            print(f"Kommando: .\\dist\\ProgGUI.exe")
            return True
        else:
            print()
            print("[ERROR] EXE wurde nicht erstellt!")
            return False
            
    except Exception as e:
        print(f"[ERROR] Build fehlgeschlagen: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)