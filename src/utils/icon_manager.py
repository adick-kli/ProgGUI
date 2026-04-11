# -*- coding: utf-8 -*-
# src/utils/icon_manager.py
"""
Icon Manager
- Erstellt und managed App-Icons
- SVG zu PNG Konvertierung
- Icon Caching
"""

import base64
import io
from pathlib import Path


class IconManager:
    """Verwaltet Icons für ProgGUI."""
    
    # App-Icon als Base64-codiertes PNG (16x16 Pixel)
    APP_ICON_BASE64 = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA"
        "WElEQVR42mNkYGD4z8DAwMjExMjIxMTMyMDAwMDAwMDAwMDAwMDA"
        "wMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAw"
        "MDAwMDAwMDAwMDAwMDAwMDA/AEPSQEBm0qYkgAAAABJRU5ErkJggg=="
    )
    
    @staticmethod
    def get_icon_path() -> Path:
        """Holt oder erstellt das App-Icon."""
        data_dir = Path(__file__).parent.parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        
        icon_path = data_dir / "icon.png"
        
        if not icon_path.exists():
            IconManager._create_icon(icon_path)
        
        return icon_path
    
    @staticmethod
    def _create_icon(icon_path: Path):
        """Erstellt das App-Icon aus Base64."""
        try:
            # Dekodiere Base64
            icon_data = base64.b64decode(IconManager.APP_ICON_BASE64)
            
            # Schreibe zu Datei
            with open(icon_path, 'wb') as f:
                f.write(icon_data)
            
            print(f"[ICON] App-Icon erstellt: {icon_path}")
        except Exception as e:
            print(f"[ERROR] Fehler beim Erstellen des Icons: {e}")
    
    @staticmethod
    def apply_icon_to_window(root):
        """Wendet das Icon auf ein Tkinter-Fenster an."""
        try:
            icon_path = IconManager.get_icon_path()
            if icon_path.exists():
                root.iconphoto(False, tk.PhotoImage(file=str(icon_path)))
                print(f"[ICON] Icon auf Fenster angewendet")
        except Exception as e:
            print(f"[WARNING] Fehler beim Anwenden des Icons: {e}")


# Einfacher App-Icon als Python-Code (für bessere Kompatibilität)
def create_simple_icon():
    """Erstellt einen einfachen App-Icon."""
    import tkinter as tk
    
    # Erstelle ein 16x16 Pixel Bild (grüner Kreis mit Blitz)
    icon = tk.PhotoImage(width=16, height=16)
    
    # Setze Pixel zu einem einfachen Muster
    for x in range(16):
        for y in range(16):
            if (x - 8)**2 + (y - 8)**2 <= 36:
                icon.put("green", (x, y))
    
    return icon