# -*- coding: utf-8 -*-
# src/utils/icon_manager.py
"""
Icon Manager
- Erstellt und managed App-Icons
- Icon Caching
"""

import base64
import tkinter as tk
from pathlib import Path


class IconManager:
    """Verwaltet Icons für ProgGUI."""
    
    @staticmethod
    def get_icon_path() -> Path:
        """Holt oder erstellt das App-Icon."""
        data_dir = Path(__file__).parent.parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        return data_dir / "icon.png"
    
    @staticmethod
    def apply_icon_to_window(root):
        """Wendet das Icon auf ein Tkinter-Fenster an."""
        try:
            # Versuche PNG zu laden
            icon_path = IconManager.get_icon_path()
            if icon_path.exists():
                root.iconphoto(False, tk.PhotoImage(file=str(icon_path)))
                print(f"[ICON] Icon auf Fenster angewendet")
        except Exception as e:
            # Fallback: Erstelle einfaches PhotoImage-Icon
            try:
                icon = tk.PhotoImage(width=32, height=32)
                # Setze grüne Pixel zu einem Kreis-Muster
                for x in range(32):
                    for y in range(32):
                        if (x - 16)**2 + (y - 16)**2 <= 144:
                            icon.put("green", (x, y))
                root.iconphoto(False, icon)
                print(f"[ICON] Fallback-Icon erstellt und angewendet")
            except Exception as fallback_error:
                print(f"[WARNING] Icon konnte nicht angewendet werden: {fallback_error}")


def create_simple_icon():
    """Erstellt einen einfachen App-Icon."""
    # Erstelle ein 32x32 Pixel grüner Kreis
    icon = tk.PhotoImage(width=32, height=32)
    
    for x in range(32):
        for y in range(32):
            if (x - 16)**2 + (y - 16)**2 <= 144:
                icon.put("green", (x, y))
    
    return icon