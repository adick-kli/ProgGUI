# -*- coding: utf-8 -*-
# src/app/windows/main_window.py
"""
Haupt-Fenster von ProgGUI
- Menübar (File, Programming, Help)
- Toolbar mit Tab-Navigation
- Content-Frame für dynamische Seiten
- Statusleiste
- Theme-Integration
- Sprach-Integration
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable

from ...config.constants import theme_manager, language_manager


class MainWindow:
    """Haupt-Fenster von ProgGUI."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialisiert das Haupt-Fenster.
        
        Args:
            root: Tkinter Root-Fenster
        """
        self.root = root
        self.root.title("⚡ ProgGUI - AT32UC3 Programmer")
        self.root.geometry("1200x800")
        self.root.minsize(1024, 768)
        
        # Farben aus Theme-Manager
        self.bg_color = theme_manager.get_color("background")
        self.fg_color = theme_manager.get_color("foreground")
        self.surface_color = theme_manager.get_color("surface")
        
        self.root.configure(bg=self.bg_color)
        
        # Tracker für aktuelle Seite
        self.current_page = None
        
        # Listener registrieren
        theme_manager.add_theme_listener(self._on_theme_changed)
        language_manager.add_language_listener(self._on_language_changed)
        
        # UI bauen
        self._create_menu_bar()
        self._create_toolbar()
        self._create_content_frame()
        self._create_status_bar()
    
    # ═══════════════════════════════════════════════════════════
    # MENÜBAR
    # ═══════════════════════════════════════════════════════════
    
    def _create_menu_bar(self):
        """Erstellt die Menübar mit File, Programming, Help."""
        self.menubar = tk.Menu(
            self.root,
            bg=theme_manager.get_color("menubar_bg"),
            fg=theme_manager.get_color("menubar_fg"),
            activebackground=theme_manager.get_color("primary"),
            activeforeground=theme_manager.get_color("button_fg")
        )
        self.root.config(menu=self.menubar)
        
        # ════════════════════════════════════════════════════
        # FILE MENU
        # ════════════════════════════════════════════════════
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(
            label=language_manager.get_string("menu_file"),
            menu=self.file_menu
        )
        
        self.file_menu.add_command(
            label=language_manager.get_string("menu_home"),
            command=self.show_home
        )
        self.file_menu.add_command(
            label=language_manager.get_string("menu_settings"),
            command=self.show_settings
        )
        self.file_menu.add_command(
            label=language_manager.get_string("menu_device_manager"),
            command=self.show_devices
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=language_manager.get_string("menu_exit"),
            command=self.root.quit
        )
        
        # ════════════════════════════════════════════════════
        # PROGRAMMING MENU
        # ════════════════════════════════════════════════════
        self.prog_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(
            label=language_manager.get_string("menu_programming"),
            menu=self.prog_menu
        )
        
        self.prog_menu.add_command(
            label=language_manager.get_string("menu_jtag"),
            command=self.show_jtag
        )
        self.prog_menu.add_command(
            label=language_manager.get_string("menu_bootloader"),
            command=self.show_bootloader
        )
        
        # ════════════════════════════════════════════════════
        # HELP MENU
        # ════════════════════════════════════════════════════
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(
            label=language_manager.get_string("menu_help"),
            menu=self.help_menu
        )
        
        self.help_menu.add_command(
            label=language_manager.get_string("menu_about"),
            command=self.show_about
        )
        self.help_menu.add_command(
            label=language_manager.get_string("menu_documentation"),
            command=self.show_documentation
        )
    
    # ═══════════════════════════════════════════════════════════
    # TOOLBAR MIT TABS
    # ═══════════════════════════════════════════════════════════
    
    def _create_toolbar(self):
        """Erstellt Toolbar mit Tab-Navigation."""
        self.toolbar = tk.Frame(
            self.root,
            bg=theme_manager.get_color("surface"),
            height=50
        )
        self.toolbar.pack(fill=tk.X, padx=0, pady=0)
        self.toolbar.pack_propagate(False)
        
        # Button-Stil
        button_style = {
            "bg": theme_manager.get_color("surface"),
            "fg": theme_manager.get_color("foreground"),
            "activebackground": theme_manager.get_color("button_hover"),
            "activeforeground": theme_manager.get_color("highlight"),
            "border": 0,
            "padx": 15,
            "pady": 12,
            "font": ("Arial", 11),
            "highlightthickness": 0,
            "relief": tk.FLAT,
            "cursor": "hand2"
        }
        
        # Tabs
        self.home_btn = tk.Button(
            self.toolbar,
            text="🏠 Home",
            command=self.show_home,
            **button_style
        )
        self.home_btn.pack(side=tk.LEFT, padx=5)
        
        self.settings_btn = tk.Button(
            self.toolbar,
            text="⚙️ Settings",
            command=self.show_settings,
            **button_style
        )
        self.settings_btn.pack(side=tk.LEFT, padx=5)
        
        self.devices_btn = tk.Button(
            self.toolbar,
            text="🔧 Devices",
            command=self.show_devices,
            **button_style
        )
        self.devices_btn.pack(side=tk.LEFT, padx=5)
        
        self.jtag_btn = tk.Button(
            self.toolbar,
            text="📌 JTAG",
            command=self.show_jtag,
            **button_style
        )
        self.jtag_btn.pack(side=tk.LEFT, padx=5)
        
        self.bootloader_btn = tk.Button(
            self.toolbar,
            text="🚀 Bootloader",
            command=self.show_bootloader,
            **button_style
        )
        self.bootloader_btn.pack(side=tk.LEFT, padx=5)
    
    # ═══════════════════════════════════════════════════════════
    # CONTENT FRAME
    # ═══════════════════════════════════════════════════════════
    
    def _create_content_frame(self):
        """Erstellt den Content-Frame für dynamische Seiten."""
        self.content_frame = tk.Frame(
            self.root,
            bg=theme_manager.get_color("background")
        )
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    # ═══════════════════════════════════════════════════════════
    # STATUSBAR
    # ═══════════════════════════════════════════════════════════
    
    def _create_status_bar(self):
        """Erstellt die Statusleiste."""
        self.status_bar = tk.Frame(
            self.root,
            bg=theme_manager.get_color("statusbar_bg"),
            height=25
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_bar,
            text="✅ Ready",
            bg=theme_manager.get_color("statusbar_bg"),
            fg=theme_manager.get_color("statusbar_fg"),
            font=("Arial", 9),
            padx=10,
            pady=3
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Device Info
        self.device_label = tk.Label(
            self.status_bar,
            text="Device: None",
            bg=theme_manager.get_color("statusbar_bg"),
            fg=theme_manager.get_color("statusbar_fg"),
            font=("Arial", 9),
            padx=10,
            pady=3
        )
        self.device_label.pack(side=tk.RIGHT)
    
    # ═════════════════════════════���════════════════════════��════
    # PAGE SWITCHING
    # ═══════════════════════════════════════════════════════════
    
    def _switch_page(self, page_class):
        """
        Wechselt zu einer anderen Seite.
        
        Args:
            page_class: Seiten-Klasse (z.B. PageHome)
        """
        # Lösche alte Seite
        if self.current_page:
            self.current_page.destroy()
        
        # Erstelle neue Seite
        try:
            self.current_page = page_class(self.content_frame)
            self.current_page.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"[ERROR] Fehler beim Laden der Seite: {e}")
    
    def show_home(self):
        """Zeigt Home-Seite."""
        from ..pages.page_home import PageHome
        self._switch_page(PageHome)
    
    def show_settings(self):
        """Zeigt Settings-Seite."""
        from ..pages.page_settings import PageSettings
        self._switch_page(PageSettings)
    
    def show_devices(self):
        """Zeigt Device Manager-Seite."""
        from ..pages.page_devices import PageDevices
        self._switch_page(PageDevices)
    
    def show_jtag(self):
        """Zeigt JTAG Programmer-Seite."""
        from ..pages.page_jtag import PageJTAG
        self._switch_page(PageJTAG)
    
    def show_bootloader(self):
        """Zeigt Bootloader Programmer-Seite."""
        from ..pages.page_bootloader import PageBootloader
        self._switch_page(PageBootloader)
    
    def show_about(self):
        """Zeigt About Dialog."""
        # Placeholder für später
        print("[INFO] About Dialog - TODO")
    
    def show_documentation(self):
        """Zeigt Dokumentation."""
        # Placeholder für später
        print("[INFO] Documentation - TODO")
    
    # ═══════════════════════════════════════════════════════════
    # THEME & LANGUAGE UPDATES
    # ═══════════════════════════════════════════════════════════
    
    def _on_theme_changed(self, new_theme):
        """Wird aufgerufen wenn Theme gewechselt wird."""
        self._update_colors()
    
    def _on_language_changed(self, new_language):
        """Wird aufgerufen wenn Sprache gewechselt wird."""
        self._update_labels()
    
    def _update_colors(self):
        """Aktualisiert alle Farben basierend auf aktuellem Theme."""
        # Root
        bg = theme_manager.get_color("background")
        self.root.configure(bg=bg)
        
        # Toolbar
        self.toolbar.configure(bg=theme_manager.get_color("surface"))
        
        # Status Bar
        self.status_bar.configure(bg=theme_manager.get_color("statusbar_bg"))
        self.status_label.configure(
            bg=theme_manager.get_color("statusbar_bg"),
            fg=theme_manager.get_color("statusbar_fg")
        )
        self.device_label.configure(
            bg=theme_manager.get_color("statusbar_bg"),
            fg=theme_manager.get_color("statusbar_fg")
        )
        
        # Content Frame
        self.content_frame.configure(bg=bg)
    
    def _update_labels(self):
        """Aktualisiert alle Labels basierend auf aktuellem Language."""
        # Menüs
        try:
            self.menubar.delete(0, tk.END)
            self._create_menu_bar()
        except:
            pass
        
        # Toolbar Buttons
        self.home_btn.config(text="🏠 Home")
        self.settings_btn.config(text="⚙️ Settings")
        self.devices_btn.config(text="🔧 Devices")
        self.jtag_btn.config(text="📌 JTAG")
        self.bootloader_btn.config(text="🚀 Bootloader")
    
    def set_status(self, message: str):
        """
        Setzt die Status-Nachricht.
        
        Args:
            message: Status-Text
        """
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def set_device(self, device_name: str):
        """
        Setzt das Gerät-Label.
        
        Args:
            device_name: Geräte-Name
        """
        self.device_label.config(text=f"Device: {device_name}")
        self.root.update_idletasks()