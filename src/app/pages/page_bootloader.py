# -*- coding: utf-8 -*-
# src/app/pages/page_bootloader.py
"""Bootloader Programmer Seite (Placeholder)."""

import tkinter as tk
from ...config.constants import theme_manager


class PageBootloader(tk.Frame):
    """Bootloader Programmer Seite."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=theme_manager.get_color("background"))
        
        header = tk.Label(
            self,
            text="🚀 BOOTLOADER PROGRAMMER",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("primary"),
            font=("Arial", 20, "bold"),
            pady=15
        )
        header.pack(fill=tk.X)
        
        placeholder = tk.Label(
            self,
            text="🚀 Bootloader Programmer\n\n[Coming Soon - Future]",
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("muted"),
            font=("Arial", 14),
            padx=20,
            pady=40
        )
        placeholder.pack(fill=tk.BOTH, expand=True)