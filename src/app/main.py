# -*- coding: utf-8 -*-
# src/app/main.py
"""
ProgGUI - Main Entry Point
Startet die Anwendung und initialisiert das Haupt-Fenster.
"""

import tkinter as tk
import sys
import os

# Importiere Window
from .windows.main_window import MainWindow

# Importiere Config Manager
from ..config.constants import theme_manager, language_manager


def main():
    """Haupt-Funktion - Startet die Applikation."""
    
    # Tkinter Root-Fenster erstellen
    root = tk.Tk()
    
    # Icon setzen (optional - wenn Icon-Datei existiert)
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass  # Icon nicht vorhanden - ignorieren
    
    # Haupt-Fenster erstellen
    try:
        main_window = MainWindow(root)
        
        # Zeige Home-Seite beim Start
        main_window.show_home()
        
        # Event-Loop starten
        root.mainloop()
        
    except Exception as e:
        print(f"[ERROR] Fehler beim Starten der Anwendung: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()