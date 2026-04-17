# -*- coding: utf-8 -*-
# src/app/pages/page_jtag.py

import tkinter as tk
from tkinter import ttk, scrolledtext
from ...config.constants import (
    theme_manager, BG, BG2, BG3, ACCENT, ACCENT2, GREEN, RED, YELLOW, TEXT, SUBTEXT,
    FONT_MAIN, FONT_TITLE, FONT_STEP, FONT_MONO
)
from ...core.product_manager import ProductManager

class PageJTAG(tk.Frame):
    def __init__(self, parent, product_manager: ProductManager):
        super().__init__(parent, bg=theme_manager.get_color("background"))
        self.product_manager = product_manager
        self.selected_product = None
        self._build_ui()
        # Optional: weitere Initialisierung
    
    def _build_ui(self):
        # HEADER
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=20, pady=(12, 4))
        tk.Label(header, text="⚡ JTAG PROGRAMMER", font=FONT_TITLE, bg=BG, fg=ACCENT).pack(side="left")
        tk.Label(header, text="Programmierung & Analyse via JTAG-Schnittstelle", font=FONT_MAIN, bg=BG, fg=SUBTEXT).pack(side="left", padx=12)
        
        # Produkt-Auswahl
        product_box = tk.LabelFrame(self, text="📦 PRODUKT-AUSWAHL", bg=BG2, fg=ACCENT2, font=FONT_STEP, relief="flat")
        product_box.pack(fill="x", padx=24, pady=10)
        # Hier: Dropdown/Liste der Produkte aus dem ProductManager
        # + Anzeigen von Controller, Boot-Hex etc. Analog PageProducts
        
        # Ausführungsbereich (Ablauf-Steuerung & Steps)
        exec_box = tk.LabelFrame(self, text="⚙️  AUSFÜHRUNG", bg=BG2, fg=ACCENT2, font=FONT_STEP, relief="flat")
        exec_box.pack(fill="x", padx=24, pady=10)
        # Start/Stop Buttons, Status-Label, Steps-Anzeige (mit Symbolen [ ], [⏳], [✅], ...)
        # Fortschritt (ProgressBar + Zeitangabe)
        
        # LOG-Bereich
        log_box = tk.LabelFrame(self, text="📜 AUSGABE / LOGS", bg=BG2, fg=ACCENT2, font=FONT_STEP, relief="flat")
        log_box.pack(fill="both", expand=True, padx=24, pady=10)
        self.log = scrolledtext.ScrolledText(
            log_box, bg="#11111b", fg=TEXT, font=FONT_MONO, relief="flat", state="disabled", wrap="none"
        )
        self.log.pack(fill="both", expand=True, padx=12, pady=8)
        # Clear/Save-Buttons
        
        # Den Rest kannst du Schritt für Schritt nach Wunsch ausbauen!