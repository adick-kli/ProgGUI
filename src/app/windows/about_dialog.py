# -*- coding: utf-8 -*-
# src/app/windows/about_dialog.py
"""
About Dialog
- App-Information
- Version
- Author
- Links
- Scrollbar für großen Inhalt
"""

import tkinter as tk
from tkinter import ttk
from ...config.constants import theme_manager


class ScrollableFrame(tk.Frame):
    """Frame mit automatischem Scrollbar."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Canvas + Scrollbar
        self.canvas = tk.Canvas(
            self,
            bg=theme_manager.get_color("background"),
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg=theme_manager.get_color("background")
        )
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _on_mousewheel(self, event):
        """Scrolling mit Mausrad."""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")


class AboutDialog(tk.Toplevel):
    """About Dialog für ProgGUI - mit Scrollbar."""
    
    def __init__(self, parent):
        """Initialisiert den About Dialog."""
        super().__init__(parent)
        
        self.title("About ProgGUI")
        self.geometry("600x500")
        self.resizable(True, True)
        
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
        # HEADER (NICHT scrollbar)
        # ═════════════════════════════════════════════════════
        
        header_frame = tk.Frame(self, bg=surface, height=120)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="⚡ ProgGUI",
            bg=surface,
            fg=primary,
            font=("Arial", 28, "bold"),
            pady=10
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Professional AT32UC3 Microcontroller Programmer",
            bg=surface,
            fg=fg,
            font=("Arial", 11),
            pady=5
        )
        subtitle_label.pack()
        
        version_label = tk.Label(
            header_frame,
            text="Version 1.0.0 (Release)",
            bg=surface,
            fg=primary,
            font=("Arial", 9, "bold")
        )
        version_label.pack()
        
        # ═════════════════════════════════════════════════════
        # SCROLLABLE CONTENT
        # ═════════════════════════════════════════════════════
        
        scrollable = ScrollableFrame(self, bg=bg)
        scrollable.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        content_frame = scrollable.scrollable_frame
        content_frame.configure(padx=20, pady=20)
        
        # ═ Author ═
        tk.Label(
            content_frame,
            text="Author",
            bg=bg,
            fg=primary,
            font=("Arial", 11, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))
        
        tk.Label(
            content_frame,
            text="ProgGUI Development Team\nCopyright © 2026",
            bg=bg,
            fg=fg,
            font=("Arial", 10),
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # ═ Description ═
        tk.Label(
            content_frame,
            text="Description",
            bg=bg,
            fg=primary,
            font=("Arial", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        desc_text = tk.Text(
            content_frame,
            height=5,
            width=60,
            bg=theme_manager.get_color("surface"),
            fg=fg,
            font=("Arial", 9),
            relief=tk.FLAT,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        desc_text.pack(fill=tk.X, pady=(0, 15))
        
        desc_text.config(state=tk.NORMAL)
        desc_text.insert(tk.END, 
            "ProgGUI ist eine professionelle Programmierungssoftware "
            "für AT32UC3 Mikrocontroller. Mit ProgGUI können Sie "
            "Firmware schnell und einfach auf Ihre Geräte programmieren."
        )
        desc_text.config(state=tk.DISABLED)
        
        # ═ Features ═
        tk.Label(
            content_frame,
            text="Features",
            bg=bg,
            fg=primary,
            font=("Arial", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        features_text = tk.Text(
            content_frame,
            height=8,
            width=60,
            bg=theme_manager.get_color("surface"),
            fg=fg,
            font=("Arial", 9),
            relief=tk.FLAT,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        features_text.pack(fill=tk.X, pady=(0, 15))
        
        features_text.config(state=tk.NORMAL)
        features_text.insert(tk.END,
            "• JTAG Programmer - Schnelle Firmware-Programmierung\n"
            "• Bootloader Manager - Sichere Bootloader-Updates\n"
            "• Device Manager - Verwaltung mehrerer Geräte\n"
            "• Dark/Light Theme - Augen-freundliche Bedienung\n"
            "• Multi-Language Support - Deutsch & English\n"
            "• Auto-Backup - Automatische Sicherungen\n"
            "• Logging System - Detaillierte Debug-Informationen\n"
            "• Settings Persistence - Einstellungen werden gespeichert"
        )
        features_text.config(state=tk.DISABLED)
        
        # ═ System Requirements ═
        tk.Label(
            content_frame,
            text="System Requirements",
            bg=bg,
            fg=primary,
            font=("Arial", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        req_text = tk.Text(
            content_frame,
            height=4,
            width=60,
            bg=theme_manager.get_color("surface"),
            fg=fg,
            font=("Arial", 9),
            relief=tk.FLAT,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        req_text.pack(fill=tk.X, pady=(0, 15))
        
        req_text.config(state=tk.NORMAL)
        req_text.insert(tk.END,
            "• Python 3.9+\n"
            "• Tkinter\n"
            "• SQLite3\n"
            "• Windows/Linux/macOS"
        )
        req_text.config(state=tk.DISABLED)
        
        # ═ License ═
        tk.Label(
            content_frame,
            text="License",
            bg=bg,
            fg=primary,
            font=("Arial", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        tk.Label(
            content_frame,
            text="MIT License - Open Source\nSee LICENSE file for details",
            bg=bg,
            fg=fg,
            font=("Arial", 9, "italic"),
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # ═ Links ═
        tk.Label(
            content_frame,
            text="Links",
            bg=bg,
            fg=primary,
            font=("Arial", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        tk.Label(
            content_frame,
            text="GitHub: https://github.com/adick-kli/ProgGUI\nDocumentation: Coming Soon",
            bg=bg,
            fg=primary,
            font=("Arial", 9),
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # ═════════════════════════════════════════════════════
        # FOOTER BUTTONS (NICHT scrollbar)
        # ═════════════════════════════════════════════════════
        
        button_frame = tk.Frame(self, bg=bg)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Button(
            button_frame,
            text="Close",
            bg=theme_manager.get_color("button_bg"),
            fg=theme_manager.get_color("button_fg"),
            activebackground=theme_manager.get_color("button_hover"),
            activeforeground=theme_manager.get_color("button_fg"),
            padx=30,
            pady=8,
            font=("Arial", 10),
            command=self.destroy
        ).pack(side=tk.RIGHT)