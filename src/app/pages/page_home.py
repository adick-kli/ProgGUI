# -*- coding: utf-8 -*-
# src/app/pages/page_home.py
"""
Home / Startseite von ProgGUI
- Welcome Banner
- Quick Actions
- System Status
- Theme-dynamisch
- Sprach-dynamisch
"""

import tkinter as tk
from tkinter import ttk

from ...config.constants import theme_manager, language_manager


class PageHome(tk.Frame):
    """Home / Startseite."""
    
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=theme_manager.get_color("background")
        )
        
        theme_manager.add_theme_listener(self._on_theme_changed)
        language_manager.add_language_listener(self._on_language_changed)
        self._create_widgets()
    
    def _create_widgets(self):
        """Erstellt alle Widgets für die Home-Seite."""
        
        # HEADER
        header_frame = tk.Frame(
            self,
            bg=theme_manager.get_color("surface"),
            height=80
        )
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🏠 HOME",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("primary"),
            font=("Arial", 20, "bold"),
            padx=20,
            pady=15
        )
        title_label.pack(anchor=tk.W)
        
        # MAIN CONTENT
        main_frame = tk.Frame(
            self,
            bg=theme_manager.get_color("background")
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # WELCOME BANNER
        welcome_frame = tk.Frame(
            main_frame,
            bg=theme_manager.get_color("surface"),
            relief=tk.RAISED,
            bd=1
        )
        welcome_frame.pack(fill=tk.X, pady=10)
        
        welcome_label = tk.Label(
            welcome_frame,
            text="⚡ Welcome to ProgGUI",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("primary"),
            font=("Arial", 16, "bold"),
            padx=15,
            pady=10
        )
        welcome_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            welcome_frame,
            text="Professional AT32UC3 Microcontroller Programmer",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("muted"),
            font=("Arial", 11),
            padx=15,
            pady=10
        )
        subtitle_label.pack(anchor=tk.W)
        
        # QUICK ACTIONS
        actions_frame = tk.LabelFrame(
            main_frame,
            text="⚡ Quick Actions",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 11, "bold")
        )
        actions_frame.pack(fill=tk.X, pady=10)
        
        actions_button_frame = tk.Frame(
            actions_frame,
            bg=theme_manager.get_color("surface")
        )
        actions_button_frame.pack(fill=tk.X)
        
        button_style = {
            "bg": theme_manager.get_color("button_bg"),
            "fg": theme_manager.get_color("button_fg"),
            "activebackground": theme_manager.get_color("button_hover"),
            "activeforeground": theme_manager.get_color("button_fg"),
            "padx": 15,
            "pady": 8,
            "font": ("Arial", 10),
            "relief": tk.RAISED,
            "cursor": "hand2"
        }
        
        tk.Button(
            actions_button_frame,
            text="🔧 Settings",
            **button_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            actions_button_frame,
            text="📌 JTAG Programmer",
            **button_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            actions_button_frame,
            text="🚀 Bootloader",
            **button_style
        ).pack(side=tk.LEFT, padx=5)
        
        # SYSTEM STATUS
        status_frame = tk.LabelFrame(
            main_frame,
            text="📊 System Status",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 11, "bold")
        )
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        status_items = [
            ("Atmel-ICE", "Connected", "success"),
            ("Tools", "All OK", "success"),
            ("Database", "2 devices loaded", "success"),
            ("Theme", "Dark", "info"),
            ("Language", "Deutsch", "info"),
        ]
        
        for label, value, color_key in status_items:
            self._create_status_item(status_frame, label, value, color_key)
        
        # VERSION & ABOUT
        about_frame = tk.Frame(
            main_frame,
            bg=theme_manager.get_color("background")
        )
        about_frame.pack(fill=tk.X, pady=10)
        
        version_label = tk.Label(
            about_frame,
            text="ProgGUI v1.0.0 | © 2026 | Open Source",
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("muted"),
            font=("Arial", 9),
            justify=tk.CENTER
        )
        version_label.pack()
    
    def _create_status_item(self, parent, label, value, color_key):
        item_frame = tk.Frame(parent, bg=theme_manager.get_color("surface"))
        item_frame.pack(fill=tk.X, pady=5)
        
        color_map = {
            "success": theme_manager.get_color("success"),
            "warning": theme_manager.get_color("warning"),
            "error": theme_manager.get_color("error"),
            "info": theme_manager.get_color("info"),
        }
        color = color_map.get(color_key, theme_manager.get_color("muted"))
        
        icon_canvas = tk.Canvas(
            item_frame,
            width=20,
            height=20,
            bg=theme_manager.get_color("surface"),
            highlightthickness=0
        )
        icon_canvas.pack(side=tk.LEFT, padx=5)
        icon_canvas.create_oval(2, 2, 18, 18, fill=color, outline=color)
        
        label_label = tk.Label(
            item_frame,
            text=label,
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            font=("Arial", 10, "bold"),
            width=20,
            anchor=tk.W
        )
        label_label.pack(side=tk.LEFT, fill=tk.X)
        
        value_label = tk.Label(
            item_frame,
            text=value,
            bg=theme_manager.get_color("surface"),
            fg=color,
            font=("Arial", 10),
            anchor=tk.W
        )
        value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def _on_theme_changed(self, new_theme):
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
    
    def _on_language_changed(self, new_language):
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
