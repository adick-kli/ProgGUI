# -*- coding: utf-8 -*-
# src/app/pages/page_bootloader.py
"""
Bootloader Programmer Seite
"""

import tkinter as tk
from ...config.constants import BG, TEXT, FONT_MAIN
from ...core.product_manager import ProductManager


class PageBootloader(tk.Frame):
    """Bootloader Programmer Seite."""
    
    def __init__(self, parent, product_manager: ProductManager, controller):
        super().__init__(parent, bg=BG)
        self.product_manager = product_manager
        self.controller = controller
        
        # Placeholder
        tk.Label(
            self, text="🔄 BOOTLOADER PROGRAMMER\n\n(In Entwicklung...)",
            font=FONT_MAIN, bg=BG, fg=TEXT
        ).pack(expand=True)