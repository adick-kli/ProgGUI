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
        super().__init__(parent, bg=BG)
        self.product_manager = product_manager
        self.selected_product = None

        # == SCROLL CANVAS-SETUP ==
        self.canvas = tk.Canvas(self, borderwidth=0, background=BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG)

        # Breite immer an Canvas anpassen
        self.scroll_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # == UI AUFBAU IM SCROLLFRAME ==
        self._build_ui(self.scrollable_frame)
        self._load_products()

        # MouseWheel unterstützt überall
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        # Canvas-Inhaltsbreite immer mit Fenster mitziehen (links bündig)
        self.canvas.itemconfig(self.scroll_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _build_ui(self, parent):
        # HEADER
        header = tk.Frame(parent, bg=BG)
        header.pack(fill="x", padx=20, pady=(10, 0), anchor="w")
        tk.Label(header, text="⚡ JTAG PROGRAMMER", font=FONT_TITLE, bg=BG, fg=ACCENT).pack(side="left", anchor="w")

        # PRODUKT-AUSWAHL
        prod_box = tk.LabelFrame(parent, text="📦 PRODUKT-AUSWAHL", bg=BG2, fg=ACCENT2,
                                 font=FONT_STEP, relief="flat", padx=16, pady=8)
        prod_box.pack(fill="x", padx=24, pady=(14, 4), anchor="w")

        select_row = tk.Frame(prod_box, bg=BG2)
        select_row.pack(fill="x")
        tk.Label(select_row, text="Produkt:", font=FONT_MAIN, bg=BG2, fg=TEXT, width=9, anchor="w").pack(side="left")
        self.product_var = tk.StringVar()
        self.product_dd = ttk.Combobox(
            select_row, textvariable=self.product_var, font=FONT_MAIN, state="readonly", width=32
        )
        self.product_dd.pack(side="left", padx=(0, 12))
        self.product_dd.bind("<<ComboboxSelected>>", self._on_product_selected)
        tk.Button(select_row, text="Manage >", font=FONT_MAIN, bg=ACCENT2, fg=BG, relief="flat", command=self._manage_products).pack(side="left")

        self.product_details = tk.LabelFrame(prod_box, bg=BG2, relief="flat")
        self.product_details.pack(fill="x", pady=(8, 0))
        self.detail_labels = {}
        for label in ["Controller", "Boot Hex", "User Hex", "Fuse Bits"]:
            row = tk.Frame(self.product_details, bg=BG2)
            row.pack(fill="x", anchor="w")
            tk.Label(row, text=label + ":", font=FONT_MONO, fg=SUBTEXT, bg=BG2, width=12, anchor="w").pack(side="left")
            val = tk.Label(row, text="---", font=FONT_MONO, fg=TEXT, bg=BG2, anchor="w")
            val.pack(side="left", padx=(4,0))
            self.detail_labels[label] = val

        # AUSFÜHRUNG
        exec_box = tk.LabelFrame(parent, text="⚙️  AUSFÜHRUNG", bg=BG2, fg=ACCENT2,
                                font=FONT_STEP, relief="flat", padx=16, pady=10)
        exec_box.pack(fill="x", padx=24, pady=(10,4), anchor="w")

        btn_row = tk.Frame(exec_box, bg=BG2)
        btn_row.pack(fill="x")
        self.btn_start = tk.Button(btn_row, text="▶ START PROGRAMMIERUNG",
                                  font=FONT_MAIN, bg=GREEN, fg=BG, relief="flat", padx=20, pady=7)
        self.btn_start.pack(side="left", padx=(0,6))
        self.btn_stop = tk.Button(btn_row, text="⏹ STOP",
                                  font=FONT_MAIN, bg=RED, fg=BG, relief="flat", padx=20, pady=7, state="disabled")
        self.btn_stop.pack(side="left")

        self.status_label = tk.Label(exec_box, text="Status: ✅ Bereit", font=FONT_MAIN, bg=BG2, fg=GREEN)
        self.status_label.pack(anchor="w", pady=(10,4))

        # SCHRITTE – LIVE TRACKING
        steps_frame = tk.LabelFrame(exec_box, text="📋 PROGRAMMIER-SCHRITTE",
                                   font=FONT_STEP, bg=BG3, fg=ACCENT2, relief="flat", padx=12, pady=7)
        steps_frame.pack(fill="x", pady=(10,2), anchor="w")
        self.step_vars = []
        self.step_labels = []
        step_names = [
            "1. Chip Erase",
            "2. User Page Erase",
            "3. User Page Write",
            "4. Flash Write (Bootloader)",
            "5. Fuse Bits Setzen",
            "6. Security Bit Setzen"
        ]
        for name in step_names:
            row = tk.Frame(steps_frame, bg=BG3)
            row.pack(fill="x", anchor="w")
            var = tk.StringVar(value="[ ]")
            lbl_icon = tk.Label(row, textvariable=var, font=FONT_MAIN, bg=BG3, fg=TEXT, width=3, anchor="w")
            lbl_icon.pack(side="left")
            lbl_txt = tk.Label(row, text=name, font=FONT_MAIN, bg=BG3, fg=TEXT)
            lbl_txt.pack(side="left", padx=(4,0))
            self.step_vars.append(var)
            self.step_labels.append(lbl_txt)

        # Fortschritt & Timer
        progress_row = tk.Frame(exec_box, bg=BG2)
        progress_row.pack(fill="x", pady=(10,2), anchor="w")
        self.progress_label = tk.Label(progress_row, text="⏱ 00:00 / 02:30", font=FONT_MONO, bg=BG2, fg=SUBTEXT)
        self.progress_label.pack(side="left")
        self.progressbar = ttk.Progressbar(progress_row, orient="horizontal", mode="determinate", length=320)
        self.progressbar.pack(side="left", fill="x", expand=True, padx=14)

        # LOGS
        log_box = tk.LabelFrame(parent, text="📜 AUSGABE / LOGS", bg=BG2, fg=ACCENT2, font=FONT_STEP, relief="flat", padx=16, pady=6)
        log_box.pack(fill="both", expand=True, padx=24, pady=(10,12), anchor="w")
        self.log = scrolledtext.ScrolledText(
            log_box, bg="#11111b", fg=TEXT, font=FONT_MONO, relief="flat", state="disabled", wrap="none", height=9
        )
        self.log.pack(fill="both", expand=True, padx=12, pady=8)
        log_btn_row = tk.Frame(log_box, bg=BG2)
        log_btn_row.pack(fill="x", pady=4)
        tk.Button(log_btn_row, text="Clear", font=FONT_MAIN, bg=BG3, fg=ACCENT2, relief="flat", command=self._clear_log).pack(side="right", padx=6)
        tk.Button(log_btn_row, text="Save", font=FONT_MAIN, bg=BG3, fg=ACCENT2, relief="flat", command=self._save_log).pack(side="right", padx=6)

    def _load_products(self):
        products = self.product_manager.read_all()
        names = [p.name for p in products]
        self.product_dd["values"] = names
        if names:
            self.product_var.set(names[0])
            self._show_product_details(names[0])

    def _on_product_selected(self, event):
        name = self.product_var.get()
        self._show_product_details(name)

    def _show_product_details(self, name):
        prod = next((p for p in self.product_manager.read_all() if p.name == name), None)
        if not prod:
            for label in self.detail_labels.values():
                label.config(text="---")
            return
        self.detail_labels["Controller"].config(text=prod.controller)
        self.detail_labels["Boot Hex"].config(text=prod.bootloader_hex)
        self.detail_labels["User Hex"].config(text=prod.userpage_hex)
        self.detail_labels["Fuse Bits"].config(text=prod.fuse_bits_value)

    def _manage_products(self):
        # Hier Bindung an show_products deiner MainWindow
        # Beispiel: self.master.master.show_products() falls Parent-Layout so ist
        pass

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _save_log(self):
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Textdatei", "*.txt"), ("Alle Dateien", "*.*")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.log.get("1.0", "end"))
