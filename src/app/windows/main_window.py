# -*- coding: utf-8 -*-
# src/app/windows/main_window.py
"""
ProgGUI Hauptfenster
- Toolbar Navigation
- Page Management
- Integration aller Komponenten
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

from ..pages.page_home import PageHome
from ..pages.page_settings import PageSettings
from ..pages.page_devices import PageDevices
from ..pages.page_products import PageProducts
from ..pages.page_jtag import PageJTAG
from ..pages.page_bootloader import PageBootloader

from ...config.constants import (
    BG, BG2, BG3, ACCENT, ACCENT2, GREEN, RED, YELLOW, TEXT, SUBTEXT,
    FONT_MAIN, FONT_TITLE, FONT_STEP, FONT_MONO,
    MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, APP_VERSION
)
from ...config.settings import settings
from ...core.product_manager import ProductManager
from ..controller import ProgrammerController


class MainWindow(tk.Tk):
    """Hauptfenster der ProgGUI Anwendung."""
    
    def __init__(self):
        super().__init__()
        
        # Window-Properties
        self.title("⚡ ProgGUI - JTAG & Bootloader Programmer")
        self.configure(bg=BG)
        self.geometry("1200x700")
        self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Initialisiere Manager
        self.product_manager = ProductManager()
        self.controller = ProgrammerController()
        
        # Pages Dictionary
        self.pages = {}
        self.current_page = None
        
        # Build UI
        self._build_ui()
        
        # Lade Home-Seite als Default
        self._show_page("home")
    
    def _build_ui(self):
        """Baut das komplette UI auf."""
        # ─────────────────────────────────────────────────────
        # HEADER BAR
        # ─────────────────────────────────────────────────────
        self._build_header()
        
        # ─────────────────────────────────────────────────────
        # TOOLBAR (Navigation)
        # ─────────────────────────────────────────────────────
        self._build_toolbar()
        
        # ─���───────────────────────────────────────────────────
        # MAIN CONTENT AREA (Pages)
        # ─────────────────────────────────────────────────────
        self.content_frame = tk.Frame(self, bg=BG)
        self.content_frame.pack(fill="both", expand=True)
        
        # ─────────────────────────────────────────────────────
        # BUILD ALL PAGES
        # ─────────────────────────────────────────────────────
        self._build_pages()
        
        # ─────────────────────────────────────────────────────
        # STATUSBAR (Bottom)
        # ─────────────────────────────────────────────────────
        self._build_statusbar()
    
    def _build_header(self):
        """Baut die Header-Bar."""
        header = tk.Frame(self, bg=ACCENT, height=50)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        # Logo/Title
        tk.Label(
            header, text="⚡ ProgGUI",
            font=(FONT_MAIN[0], 18, "bold"),
            bg=ACCENT, fg=BG
        ).pack(side="left", padx=20, pady=12)
        
        # Version
        tk.Label(
            header, text=f"v{APP_VERSION}",
            font=FONT_MAIN,
            bg=ACCENT, fg=BG
        ).pack(side="left", padx=2)
        
        # Spacer
        tk.Frame(header, bg=ACCENT).pack(side="left", fill="x", expand=True)
        
        # Help/Settings in Header (optional)
        tk.Button(
            header, text="?",
            bg=ACCENT2, fg=BG, relief="flat",
            font=FONT_MAIN, cursor="hand2", padx=10, pady=8
        ).pack(side="right", padx=4, pady=6)
    
    def _build_toolbar(self):
        """Baut die Toolbar mit Navigation Buttons."""
        toolbar = tk.Frame(self, bg=BG2, height=50)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)
        
        # Navigation Buttons
        buttons = [
            ("🏠 HOME", "home"),
            ("⚙️  SETTINGS", "settings"),
            ("🔧 PRODUCTS", "products"),
            ("⚡ JTAG", "jtag"),
            ("🔄 BOOTLOADER", "bootloader"),
        ]
        
        self.page_buttons = {}
        
        for btn_text, page_name in buttons:
            btn = tk.Button(
                toolbar, text=btn_text,
                font=FONT_MAIN,
                bg=BG2, fg=SUBTEXT, relief="flat", cursor="hand2",
                padx=15, pady=10,
                command=lambda p=page_name: self._show_page(p)
            )
            btn.pack(side="left", padx=4, pady=6)
            self.page_buttons[page_name] = btn
    
    def _build_pages(self):
        """Erstellt alle Pages."""
        # Home
        self.pages["home"] = PageHome(self.content_frame)
        
        # Settings
        self.pages["settings"] = PageSettings(self.content_frame)
        
        # Products (NEU!)
        self.pages["products"] = PageProducts(self.content_frame, self.product_manager)
        
        # JTAG
        self.pages["jtag"] = PageJTAG(self.content_frame, self.product_manager, self.controller)
        
        # Bootloader
        self.pages["bootloader"] = PageBootloader(self.content_frame, self.product_manager, self.controller)
    
    def _build_statusbar(self):
        """Baut die Status-Bar am unteren Rand."""
        statusbar = tk.Frame(self, bg=BG2, height=30)
        statusbar.pack(fill="x", side="bottom")
        statusbar.pack_propagate(False)
        
        tk.Label(
            statusbar, text="✅ Bereit",
            bg=BG2, fg=GREEN, font=FONT_MAIN, padx=20
        ).pack(side="left")
        
        tk.Label(
            statusbar, text="© 2026 ProgGUI",
            bg=BG2, fg=SUBTEXT, font=FONT_MAIN
        ).pack(side="right", padx=20)
    
    def _show_page(self, page_name: str):
        """
        Wechselt zur angegebenen Seite.
        
        Args:
            page_name: Name der Seite (home, settings, products, jtag, bootloader)
        """
        # Verstecke aktuelle Seite
        if self.current_page:
            self.pages[self.current_page].pack_forget()
            # Deaktiviere Button
            if self.current_page in self.page_buttons:
                self.page_buttons[self.current_page].configure(
                    bg=BG2, fg=SUBTEXT
                )
        
        # Zeige neue Seite
        if page_name in self.pages:
            self.pages[page_name].pack(fill="both", expand=True)
            self.current_page = page_name
            
            # Aktiviere Button
            if page_name in self.page_buttons:
                self.page_buttons[page_name].configure(
                    bg=ACCENT2, fg=BG
                )


def main():
    """Entry Point für die Anwendung."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()