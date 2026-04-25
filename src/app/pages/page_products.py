# -*- coding: utf-8 -*-
# src/app/pages/page_products.py
"""
Products Management Page
- Zeigt alle Produkte in Liste
- CRUD-Operationen (Add/Edit/Delete)
- Integration mit ProductManager
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from datetime import datetime

from ...config.constants import (
    BG, BG2, BG3, ACCENT, ACCENT2, GREEN, RED, YELLOW, TEXT, SUBTEXT,
    FONT_MAIN, FONT_TITLE, FONT_STEP, FONT_MONO
)
from ...core.product import Product, ProgrammingStep
from ...core.product_manager import ProductManager


class PageProducts(tk.Frame):
    """Produkt-Management Seite."""
    
    def __init__(self, parent, product_manager: ProductManager):
        super().__init__(parent, bg=BG)
        
        self.product_manager = product_manager
        self.selected_product = None
        
        self._build_ui()
        self._refresh_products()
    
    def _build_ui(self):
        """Baut die UI auf."""
        # ─────────────────────────────────────────────────────
        # HEADER
        # ─────────────────────────────────────────────────────
        header = tk.Frame(self, bg=BG, height=60)
        header.pack(fill="x", padx=20, pady=(12, 4))
        
        title_frame = tk.Frame(header, bg=BG)
        title_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(
            title_frame, text="🔧 PRODUCTS",
            font=FONT_TITLE, bg=BG, fg=ACCENT
        ).pack(side="left")
        
        tk.Label(
            title_frame, text="Verwaltung aller programmierbaren Produkte",
            font=FONT_MAIN, bg=BG, fg=SUBTEXT
        ).pack(side="left", padx=12)
        
        # Button Bar
        btn_frame = tk.Frame(header, bg=BG)
        btn_frame.pack(side="right")
        
        tk.Button(
            btn_frame, text="➕ Add Product",
            command=self._add_product,
            bg=GREEN, fg=BG, relief="flat",
            font=FONT_MAIN, cursor="hand2", padx=15, pady=8
        ).pack(side="left", padx=4)
        
        tk.Button(
            btn_frame, text="🔄 Refresh",
            command=self._refresh_products,
            bg=ACCENT2, fg=BG, relief="flat",
            font=FONT_MAIN, cursor="hand2", padx=15, pady=8
        ).pack(side="left", padx=4)
        
        # ─────────────────────────────────────────────────────
        # MAIN CONTENT
        # ─────────────────────────────────────────────────────
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=16, pady=12)
        
        # Products List mit ScrollBar
        self._build_products_list(main)
    
    def _build_products_list(self, parent):
        canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # NEU: Mausrad-Scrolling binden
        def _on_mousewheel(event):
            # windows/mac vs. linux wheel delta
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # Windows/Mac
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux (event.delta ist immer 0, dafür wird event.num verwendet)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        self.products_frame = scrollable_frame

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _refresh_products(self):
        """Ladet alle Produkte und zeigt sie an."""
        # Lösche alte Widgets
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        
        # Lade Produkte aus DB
        products = self.product_manager.read_all()
        
        if not products:
            # Leerer Zustand
            tk.Label(
                self.products_frame,
                text="Keine Produkte vorhanden\n➕ Klicke 'Add Product' um zu starten",
                font=FONT_MAIN, bg=BG, fg=SUBTEXT,
                pady=40
            ).pack(fill="both", expand=True)
        else:
            # Zeige alle Produkte
            for product in products:
                self._create_product_card(self.products_frame, product)
    
    def _create_product_card(self, parent, product: Product):
        """Erstellt eine Produkt-Card."""
        card = tk.Frame(parent, bg=BG2, relief="flat", bd=0)
        card.pack(fill="x", pady=8, padx=2)
        
        # Header
        header = tk.Frame(card, bg=BG2)
        header.pack(fill="x", padx=12, pady=(8, 0))
        
        # Title + Buttons
        title_frame = tk.Frame(header, bg=BG2)
        title_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(
            title_frame, text=f"📦 {product.name}",
            font=FONT_STEP, bg=BG2, fg=ACCENT2
        ).pack(side="left", anchor="w")
        
        # Adapter/Interface anzeigen
        tk.Label(
            title_frame,
            text=f"Adapter: {getattr(product, 'adapter', 'atmelice')}  Interface: {getattr(product, 'interface', 'jtag')}",
            font=FONT_MONO, bg=BG2, fg=SUBTEXT
        ).pack(side="left", padx=(12,0))
        
        # Buttons
        button_frame = tk.Frame(header, bg=BG2)
        button_frame.pack(side="right")
        
        tk.Button(
            button_frame, text="✏️ Edit",
            command=lambda: self._edit_product(product),
            bg=ACCENT2, fg=BG, relief="flat",
            font=FONT_MAIN, cursor="hand2", padx=10
        ).pack(side="left", padx=2)
        
        tk.Button(
            button_frame, text="🗑 Delete",
            command=lambda: self._delete_product(product),
            bg=RED, fg=BG, relief="flat",
            font=FONT_MAIN, cursor="hand2", padx=10
        ).pack(side="left", padx=2)
        
        tk.Button(
            button_frame, text="⚡ Use",
            command=lambda: self._use_for_jtag(product),
            bg=GREEN, fg=BG, relief="flat",
            font=FONT_MAIN, cursor="hand2", padx=10
        ).pack(side="left", padx=2)
        
        # Content
        content = tk.Frame(card, bg=BG2)
        content.pack(fill="x", padx=12, pady=6)
        
        # Product Details
        details = [
            ("Controller:", product.controller),
            ("Boot HEX:", Path(product.bootloader_hex).name if product.bootloader_hex else "—"),
            ("User HEX:", Path(product.userpage_hex).name if product.userpage_hex else "—"),
            ("Fuse Bits:", product.fuse_bits_value),
        ]
        # UserWrites visualisieren
        if getattr(product, "user_writes", None):
            for idx, word in enumerate(product.user_writes, 1):
                details.append((f"UserWord{idx} Addr/Wert:", f"{word['address']} / {word['value']}"))
        
        for label, value in details:
            row = tk.Frame(content, bg=BG2)
            row.pack(fill="x", pady=2)
            
            tk.Label(
                row, text=label, width=20, anchor="w",
                bg=BG2, fg=SUBTEXT, font=FONT_MONO
            ).pack(side="left")
            
            tk.Label(
                row, text=value,
                bg=BG2, fg=TEXT, font=FONT_MONO
            ).pack(side="left", fill="x", expand=True)
        
        # Steps
        steps_line = tk.Frame(content, bg=BG2)
        steps_line.pack(fill="x", pady=6)
        
        enabled_steps = sum(1 for s in product.steps if s.enabled)
        
        tk.Label(
            steps_line, text="📋 Schritte:",
            bg=BG2, fg=SUBTEXT, font=FONT_MAIN
        ).pack(side="left", padx=(0, 8))
        
        for step in product.steps:
            symbol = "✅" if step.enabled else "❌"
            color = TEXT if step.enabled else SUBTEXT
            
            tk.Label(
                steps_line, text=f"{symbol}{step.number}",
                bg=BG2, fg=color, font=FONT_MONO
            ).pack(side="left", padx=2)
        
        # Footer (Last Programmed)
        footer = tk.Frame(card, bg=BG3)
        footer.pack(fill="x", padx=8, pady=(6, 8))
        
        if product.last_programmed:
            last_prog = product.last_programmed.strftime("%Y-%m-%d %H:%M")
            text = f"📅 Zuletzt programmiert: {last_prog}"
        else:
            text = "📅 Noch nicht programmiert"
        
        tk.Label(
            footer, text=text,
            bg=BG3, fg=SUBTEXT, font=FONT_MAIN, padx=8, pady=4
        ).pack(anchor="w")
    
    def _add_product(self):
        """Öffnet Dialog zum Hinzufügen eines neuen Produkts."""
        dialog = ProductEditDialog(self, self.product_manager, product=None)
        self.wait_window(dialog)
        self._refresh_products()
    
    def _edit_product(self, product: Product):
        """Öffnet Dialog zum Bearbeiten eines Produkts."""
        dialog = ProductEditDialog(self, self.product_manager, product=product)
        self.wait_window(dialog)
        self._refresh_products()
    
    def _delete_product(self, product: Product):
        """Löscht ein Produkt nach Bestätigung."""
        response = messagebox.askyesno(
            "Löschen bestätigen",
            f"Möchtest du '{product.name}' wirklich löschen?\nDiese Aktion kann nicht rückgängig gemacht werden."
        )
        if response:
            self.product_manager.delete(product.id)
            self._refresh_products()
            messagebox.showinfo("Erfolg", f"Produkt '{product.name}' gelöscht")
    
    def _use_for_jtag(self, product: Product):
        """Lädt Produkt für JTAG-Seite."""
        messagebox.showinfo(
            "Info",
            f"Produkt '{product.name}' wird für JTAG Programmierung verwendet.\n\n(Integration kommt später)"
        )

    # -------------------------
    # für EditDialog:
    # -------------------------

class ProductEditDialog(tk.Toplevel):
    """Dialog zum Bearbeiten/Erstellen von Produkten."""
    
    def __init__(self, parent, product_manager: ProductManager, product: Product = None):
        super().__init__(parent)
        self.product_manager = product_manager
        self.product = product
        self.is_new = product is None
        
        self.title("✏️ Produkt bearbeiten" if product else "➕ Neues Produkt")
        self.geometry("700x900")
        self.configure(bg=BG)
        
        self._build_ui()
        self.grab_set()
    
    def _build_ui(self):
        """Baut das Dialog-UI auf."""
        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Mausrad Scrollen erlauben
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main = tk.Frame(scrollable_frame, bg=BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.fields = {}
        
        # Name
        self._add_entry_field(main, "Produkt Name:", "name", 
                             self.product.name if self.product else "")
        # Description
        self._add_entry_field(main, "Beschreibung:", "description",
                             self.product.description if self.product else "")
        # Controller
        self._add_entry_field(main, "Controller:", "controller",
                             self.product.controller if self.product else "")
        # Boot HEX
        self._add_file_field(main, "Boot HEX Datei:", "bootloader_hex",
                            self.product.bootloader_hex if self.product else "")
        # User HEX
        self._add_file_field(main, "User Page HEX:", "userpage_hex",
                            self.product.userpage_hex if self.product else "")
        # Fuse Bits
        self._add_entry_field(main, "Fuse Bits (Hex):", "fuse_bits_value",
                             self.product.fuse_bits_value if self.product else "")
        
        # Adapter (Programmer)
        self._add_dropdown_field(main, "Adapter:", "adapter", 
            ["atmelice", "avrdragon"], getattr(self.product, "adapter", "atmelice") if self.product else "atmelice"
        )
        # Interface
        self._add_dropdown_field(main, "Interface:", "interface", 
            ["jtag", "swd"], getattr(self.product, "interface", "jtag") if self.product else "jtag"
        )

        # UserPage Word 1 (optional)
        uw = getattr(self.product, "user_writes", None)
        self._add_entry_field(main, "UserPage Word 1 Adresse (hex):", "user_word1_addr",
            uw[0]["address"] if (uw and len(uw)>0) else "")
        self._add_entry_field(main, "UserPage Word 1 Wert (hex):", "user_word1_value",
            uw[0]["value"] if (uw and len(uw)>0) else "")
        self._add_entry_field(main, "UserPage Word 2 Adresse (hex):", "user_word2_addr",
            uw[1]["address"] if (uw and len(uw)>1) else "")
        self._add_entry_field(main, "UserPage Word 2 Wert (hex):", "user_word2_value",
            uw[1]["value"] if (uw and len(uw)>1) else "")

        # Steps
        tk.Label(main, text="📋 Programmier-Schritte:", 
                bg=BG, fg=ACCENT2, font=FONT_STEP).pack(anchor="w", pady=(20, 10))
        self.step_vars = {}

        steps = self.product.steps if self.product else Product.create_default_steps()
        for step in steps:
            var = tk.BooleanVar(value=step.enabled)
            self.step_vars[step.number] = var
            tk.Checkbutton(
                main, text=f"{step.number}. {step.name}",
                variable=var, bg=BG, fg=TEXT,
                selectcolor=BG3, activebackground=BG,
                font=FONT_MAIN
            ).pack(anchor="w", pady=2)
        
        # Tools / Datei-Pfade
        self._add_file_field(
            main, "Pfad zu atprogram.exe:", "atprogram_path",
            self.product.atprogram_path if self.product else "",
            filetypes=[("Programmdateien", "*.exe"), ("Alle", "*.*")]
        )
        self._add_file_field(
            main, "Pfad zu atbackend.exe:", "atbackend_path",
            self.product.atbackend_path if self.product else "",
            filetypes=[("Programmdateien", "*.exe"), ("Alle", "*.*")]
        )
        self._add_file_field(
            main, "Pfad zu objcopy.exe:", "objcopy_path",
            self.product.objcopy_path if self.product else "",
            filetypes=[("Programmdateien", "*.exe"), ("Alle", "*.*")]
        )

        # Buttons
        btn_frame = tk.Frame(main, bg=BG)
        btn_frame.pack(fill="x", pady=(20, 0))
        tk.Button(
            btn_frame, text="✓ Speichern",
            command=self._save,
            bg=GREEN, fg=BG, relief="flat",
            font=FONT_MAIN, cursor="hand2", padx=20, pady=8
        ).pack(side="left", padx=4)
        tk.Button(
            btn_frame, text="✗ Abbrechen",
            command=self.destroy,
            bg=RED, fg=BG, relief="flat",
            font=FONT_MAIN, cursor="hand2", padx=20, pady=8
        ).pack(side="left", padx=4)
    
    def _add_entry_field(self, parent, label: str, key: str, value: str = ""):
        tk.Label(parent, text=label, bg=BG, fg=SUBTEXT,
                font=FONT_MAIN).pack(anchor="w", pady=(10, 2))
        entry = tk.Entry(parent, bg=BG3, fg=TEXT, insertbackground=TEXT,
                        relief="flat", font=FONT_MONO)
        entry.insert(0, value)
        entry.pack(fill="x", ipady=5)
        self.fields[key] = entry
    
    def _add_file_field(self, parent, label, key, value="", filetypes=None):
        tk.Label(parent, text=label, bg=BG, fg=SUBTEXT,
                 font=FONT_MAIN).pack(anchor="w", pady=(10, 2))
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", ipady=5)
        entry = tk.Entry(row, bg=BG3, fg=TEXT, insertbackground=TEXT,
                         relief="flat", font=FONT_MONO)
        entry.insert(0, value)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Button(
            row, text="Browse...",
            command=lambda: self._browse_file(entry, filetypes),
            bg=BG3, fg=ACCENT, relief="flat",
            font=FONT_MAIN, cursor="hand2", padx=10
        ).pack(side="right")
        self.fields[key] = entry

    def _add_dropdown_field(self, parent, label, key, options, value=None):
        tk.Label(parent, text=label, bg=BG, fg=SUBTEXT, font=FONT_MAIN).pack(anchor="w", pady=(10,2))
        var = tk.StringVar(value=value or options[0])
        dropdown = ttk.Combobox(parent, textvariable=var, values=options, state="readonly", font=FONT_MAIN)
        dropdown.pack(fill="x", pady=(0,4))
        self.fields[key] = dropdown

    def _browse_file(self, entry: tk.Entry, filetypes=None):
        if filetypes is None:
            filetypes = [("Alle Dateien", "*.*")]
        path = filedialog.askopenfilename(
            filetypes=filetypes
        )
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def _save(self):
        try:
            name = self.fields["name"].get().strip()
            if not name:
                messagebox.showerror("Fehler", "Produkt Name ist erforderlich!")
                return
            user_writes = []
            addr1 = self.fields["user_word1_addr"].get().strip()
            val1 = self.fields["user_word1_value"].get().strip()
            if addr1 and val1:
                user_writes.append({"address": addr1, "value": val1})
            addr2 = self.fields["user_word2_addr"].get().strip()
            val2 = self.fields["user_word2_value"].get().strip()
            if addr2 and val2:
                user_writes.append({"address": addr2, "value": val2})

            if self.is_new:
                product = Product(
                    id=None,
                    name=name,
                    description=self.fields["description"].get(),
                    controller=self.fields["controller"].get(),
                    bootloader_hex=self.fields["bootloader_hex"].get(),
                    userpage_hex=self.fields["userpage_hex"].get(),
                    fuse_bits_value=self.fields["fuse_bits_value"].get() if self.fields.get("fuse_bits_value") else "",
                    steps=self._get_steps(),
                    atprogram_path=self.fields["atprogram_path"].get(),
                    atbackend_path=self.fields["atbackend_path"].get(),
                    objcopy_path=self.fields["objcopy_path"].get(),
                    adapter=self.fields["adapter"].get(),
                    interface=self.fields["interface"].get(),
                    user_writes=user_writes,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    last_programmed=None
                )
                self.product_manager.create(product)
                messagebox.showinfo("Erfolg", f"Produkt '{name}' erstellt!")
            else:
                self.product.name = name
                self.product.description = self.fields["description"].get()
                self.product.controller = self.fields["controller"].get()
                self.product.bootloader_hex = self.fields["bootloader_hex"].get()
                self.product.userpage_hex = self.fields["userpage_hex"].get()
                self.product.fuse_bits_value = self.fields["fuse_bits_value"].get() if self.fields.get("fuse_bits_value") else ""
                self.product.steps = self._get_steps()
                self.product.adapter = self.fields["adapter"].get()
                self.product.interface = self.fields["interface"].get()
                self.product.user_writes = user_writes
                # NEU - Die 3 Pfadfelder VOR dem Speichern setzen:
                self.product.atprogram_path = self.fields["atprogram_path"].get()
                self.product.atbackend_path = self.fields["atbackend_path"].get()
                self.product.objcopy_path = self.fields["objcopy_path"].get()
                self.product.updated_at = datetime.now()
                self.product_manager.update(self.product)
                messagebox.showinfo("Erfolg", f"Produkt '{name}' aktualisiert!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Fehler", f"Speichern fehlgeschlagen:\n{e}")

    def _get_steps(self) -> list:
        default_steps = Product.create_default_steps()
        for step in default_steps:
            if self.step_vars.get(step.number):
                step.enabled = self.step_vars[step.number].get()
        return default_steps