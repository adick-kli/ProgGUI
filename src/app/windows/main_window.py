# -*- coding: utf-8 -*-
# src/app/windows/main_window.py
"""
ProgGUI Hauptfenster - Minimal Integration
- Behält alte gui.py + controller.py
- Integriert neue ProductManager
"""

import tkinter as tk
from pathlib import Path

from ...config.constants import (
    BG, ACCENT, APP_VERSION
)
from ...core.product_manager import ProductManager
from ..gui import ProgGUI


class MainWindow(tk.Tk):
    """Hauptfenster der ProgGUI Anwendung."""
    
    def __init__(self):
        super().__init__()
        
        # Initialisiere ProductManager
        self.product_manager = ProductManager()
        
        # Erstelle alte GUI
        self.prog_gui = ProgGUI(self.product_manager)
        
        # Transfer Window-Eigenschaften
        self.title("⚡ ProgGUI - JTAG & Bootloader Programmer")
        self.configure(bg=BG)
        
        # Window wird von ProgGUI (tk.Tk) übernommen
        # Diese Klasse dient nur als Wrapper für ProductManager


def main():
    """Entry Point für die Anwendung."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()