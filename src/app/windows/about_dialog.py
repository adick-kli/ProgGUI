# -*- coding: utf-8 -*-
# src/app/windows/about_dialog.py
"""
About Dialog
- App-Information
- Version
- Author
- Links
"""

import tkinter as tk
from tkinter import ttk
from ...config.constants import theme_manager


class AboutDialog(tk.Toplevel):
    """About Dialog für ProgGUI."""
    
    def __init__(self, parent):
        """Initialisiert den About Dialog."""
        super().__init__(parent)
        
        self.title("About ProgGUI")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Zentriere Dialog über Parent
        self.transient(parent)
        self.grab_set()
        
        # Konfiguriere Farben
        bg = theme_manager.get_color("background")
        surface = theme_manager.get_color("surface")
        fg = theme_manager.get_color("foreground")
        primary = theme_manager.get_color("primary")
        
        self.configure(bg=bg)
        
        # ═════════════════════════════════════════════════════
        # HEADER
        # ═════════════════════════════════════════════════════
        
        header_frame = tk.Frame(self, bg=surface, height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="⚡ ProgGUI",
            bg=surface,
            fg=primary,
            font=("Arial", 24, "bold"),
            pady=15
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="AT32UC3 Microcontroller Programmer",
            bg=surface,
            fg=fg,
            font=("Arial", 10),
            pady=5
        )
        subtitle_label.pack()
        
        # ═════════════════════════════════════════════════════
        # CONTENT
        # ═════════════════════════════════════════════════════
        
        content_frame = tk.Frame(self, bg=bg)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Version
        tk.Label(
            content_frame,
            text="Version:",
            bg=bg,
            fg=primary,
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=5)
        
        tk.Label(
            content_frame,
            text="1.0.0 (Release)",
            bg=bg,
            fg=fg,
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        # Author
        tk.Label(
            content_frame,
            text="Author:",
            bg=bg,
            fg=primary,
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=5)
        
        tk.Label(
            content_frame,
            text="ProgGUI Development Team",
            bg=bg,
            fg=fg,
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        # Description
        tk.Label(
            content_frame,
            text="Description:",
            bg=bg,
            fg=primary,
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=5)
        
        desc_text = tk.Text(
            content_frame,
            height=5,
            width=50,
            bg=theme_manager.get_color("background"),
            fg=fg,
            font=("Arial", 9),
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        desc_text.pack(fill=tk.X, pady=5)
        
        desc_text.config(state=tk.NORMAL)
        desc_text.insert(tk.END, 
            "ProgGUI ist eine professionelle Programmierungssoftware "
            "fuer AT32UC3 Mikrocontroller.\n\n"
            "Features:\n"
            "* JTAG & Bootloader Programmierung\n"
            "* Dark/Light Theme Support\n"
            "* Multi-Language Support\n"
            "* Device Manager"
        )
        desc_text.config(state=tk.DISABLED)
        
        # License
        tk.Label(
            content_frame,
            text="License: Open Source (MIT)",
            bg=bg,
            fg=fg,
            font=("Arial", 9, "italic")
        ).pack(anchor=tk.W, pady=5)
        
        # ═════════════════════════════════════════════════════
        # BUTTONS
        # ═════════════════════════════════════════════════════
        
        button_frame = tk.Frame(self, bg=bg)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(
            button_frame,
            text="Close",
            bg=theme_manager.get_color("button_bg"),
            fg=theme_manager.get_color("button_fg"),
            padx=30,
            pady=8,
            font=("Arial", 10),
            command=self.destroy
        ).pack(side=tk.RIGHT)