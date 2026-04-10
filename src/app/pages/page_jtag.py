# -*- coding: utf-8 -*-
# src/app/pages/page_jtag.py
"""JTAG Programmer Seite (Placeholder)."""

import tkinter as tk
from ...config.constants import theme_manager


class PageJTAG(tk.Frame):
    """JTAG Programmer Seite."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=theme_manager.get_color("background"))
        
        header = tk.Label(
            self,
            text="📌 JTAG PROGRAMMER",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("primary"),
            font=("Arial", 20, "bold"),
            pady=15
        )
        header.pack(fill=tk.X)
        
        placeholder = tk.Label(
            self,
            text="📌 JTAG Programmer\n\n[Coming Soon - Schritt 11]",
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("muted"),
            font=("Arial", 14),
            padx=20,
            pady=40
        )
        placeholder.pack(fill=tk.BOTH, expand=True)