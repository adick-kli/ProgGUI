# -*- coding: utf-8 -*-
# src/app/gui.py
"""
Tkinter GUI für ProgGUI
- Reine Präsentationslogik
- Ruft nur den Controller auf
- Keine Business-Logik hier!
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading

from ..config.constants import (
    BG, BG2, BG3, ACCENT, ACCENT2, GREEN, RED, YELLOW, TEXT, SUBTEXT,
    FONT_MAIN, FONT_TITLE, FONT_STEP, FONT_MONO,
    DEVICE, INTERFACE, PROGRAMMER,
    MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, LOG_TAGS
)
from ..config.settings import settings
from ..utils.validators import Validator, ValidationError
from ..utils.logging import LogEntry
from .controller import ProgrammerController


class ProgGUI(tk.Tk):
    """Hauptfenster für ProgGUI."""
    
    def __init__(self):
        super().__init__()
        self.title("⚡ AT32UC3A1512 Programmer")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
    
        # Controller
        self.controller = ProgrammerController()
    
        # ⭐ Variablen ZUERST initialisieren
        self._init_variables()
    
        # ⭐ Callbacks NUR EINMAL registrieren - HIER, nicht später!
        self.controller.set_log_callback(self._on_log)
        self.controller.set_status_callback(self._on_status)
        self.controller.set_progress_callback(self._on_progress)
    
        # DANN UI bauen
        self._build_ui()
    
    def _init_variables(self):
        """Initialisiert alle Tkinter-Variablen."""
        # String-Variablen
        self.hex_file_var = tk.StringVar(value=settings.get("hex_file", ""))
        self.val_1fc_var = tk.StringVar(value=settings.get("val_1fc", ""))
        self.val_1f8_var = tk.StringVar(value=settings.get("val_1f8", ""))
        self.fuse_val_var = tk.StringVar(value=settings.get("fuse_val", ""))
        
        self.atprogram_var = tk.StringVar(value=settings.get("atprogram_path", ""))
        self.atbackend_var = tk.StringVar(value=settings.get("atbackend_path", ""))
        self.objcopy_var = tk.StringVar(value=settings.get("objcopy_path", ""))
        
        # Boolean-Variablen (für Checkboxen)
        self.steps = {
            "chip_erase": tk.BooleanVar(value=settings.get("chip_erase", True)),
            "user_erase": tk.BooleanVar(value=settings.get("user_erase", True)),
            "user_write": tk.BooleanVar(value=settings.get("user_write", True)),
            "flash_write": tk.BooleanVar(value=settings.get("flash_write", True)),
            "fuse_write": tk.BooleanVar(value=settings.get("fuse_write", True)),
            "secure": tk.BooleanVar(value=settings.get("secure", False)),
        }
        
        # Trace-Callbacks zum Auto-Speichern
        for var in [self.hex_file_var, self.val_1fc_var, self.val_1f8_var,
                    self.fuse_val_var, self.atprogram_var, self.atbackend_var,
                    self.objcopy_var]:
            var.trace_add("write", lambda *args: self._save_settings())
        
        for bv in self.steps.values():
            bv.trace_add("write", lambda *args: self._save_settings())
    
    def _build_ui(self):
        """Baut die komplette UI auf."""
        # Title Bar
        title_frame = tk.Frame(self, bg=ACCENT, height=4)
        title_frame.pack(fill="x")
        
        # Header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=20, pady=(12, 4))
        tk.Label(header, text="⚡ AT32UC3A1512 Programmer",
                font=FONT_TITLE, bg=BG, fg=ACCENT).pack(side="left")
        tk.Label(header, text=f"  {PROGRAMMER.upper()} · {INTERFACE.upper()} · {DEVICE}",
                font=FONT_MAIN, bg=BG, fg=SUBTEXT).pack(side="left", padx=12)
        
        # Main Content
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=16, pady=6)
        
        self.left = tk.Frame(main, bg=BG)
        self.left.pack(side="left", fill="y", padx=(0, 10))
        
        self.right = tk.Frame(main, bg=BG)
        self.right.pack(side="left", fill="both", expand=True)
        
        self._build_left()
        self._build_right()
        self._build_bottom()
    
    def _build_left(self):
        """Linke Spalte: Schritte, Memory-Werte, Tool-Status."""
        # Programmier-Schritte
        box = self._make_frame(self.left, "📋  Programmier-Schritte")
        box.pack(fill="x", pady=(0, 10))
        
        steps_info = [
            ("chip_erase", "1. Flash löschen (ChipErase)"),
            ("user_erase", "2. User Page löschen"),
            ("user_write", "3. User Page schreiben"),
            ("flash_write", "4. Bootloader schreiben"),
            ("fuse_write", "5. Fuse Bits setzen"),
            ("secure", "6. Security Bit setzen"),
        ]
        
        for key, label in steps_info:
            row = tk.Frame(box, bg=BG2)
            row.pack(fill="x", pady=2)
            tk.Checkbutton(row, text=label, variable=self.steps[key],
                          bg=BG2, fg=TEXT, selectcolor=BG3,
                          activebackground=BG2, activeforeground=ACCENT,
                          font=FONT_MAIN).pack(side="left", padx=8, pady=3)
        
        # Memory-Werte
        mem = self._make_frame(self.left, "🔧  Memory / User Page")
        mem.pack(fill="x", pady=(0, 10))
        self._make_entry_row(mem, "Wert → 0x808001FC :", self.val_1fc_var)
        self._make_entry_row(mem, "Wert → 0x808001F8 :", self.val_1f8_var)
        
        # Fuse Bits
        fuse = self._make_frame(self.left, "🔩  Fuse Bits")
        fuse.pack(fill="x", pady=(0, 10))
        self._make_entry_row(fuse, "Fuse Wert (Hex)  :", self.fuse_val_var)
        
        # Tool-Status
        self.tool_frame = self._make_frame(self.left, "🛠  Tool-Status")
        self.tool_frame.pack(fill="x")
        self._validate_tools()
    
    def _build_right(self):
        """Rechte Spalte: Tool-Pfade, HEX-Datei, Log."""
        # Tool-Pfade
        paths = self._make_frame(self.right, "📂  Tool-Pfade")
        paths.pack(fill="x", pady=(0, 10))
        
        self._make_path_row(paths, "atprogram.exe :", self.atprogram_var)
        self._make_path_row(paths, "atbackend.exe :", self.atbackend_var)
        self._make_path_row(paths, "avr32-objcopy :", self.objcopy_var)
        
        # HEX-Datei
        file_box = self._make_frame(self.right, "📁  Bootloader HEX-Datei")
        file_box.pack(fill="x", pady=(0, 10))
        
        ff = tk.Frame(file_box, bg=BG2)
        ff.pack(fill="x", padx=6, pady=6)
        
        tk.Entry(ff, textvariable=self.hex_file_var,
                bg=BG3, fg=TEXT, insertbackground=TEXT,
                relief="flat", font=FONT_MONO).pack(
            side="left", fill="x", expand=True, ipady=5, padx=(0, 6))
        
        tk.Button(ff, text="Browse…", command=self._browse_hex,
                 bg=ACCENT2, fg=BG, relief="flat",
                 font=FONT_MAIN, cursor="hand2", padx=10).pack(side="right")
        
        # Log-Bereich
        log_box = self._make_frame(self.right, "📜  Ausgabe / Log")
        log_box.pack(fill="both", expand=True)
        
        self.log = scrolledtext.ScrolledText(
            log_box, bg="#11111b", fg=TEXT,
            font=FONT_MONO, relief="flat",
            state="disabled", wrap="none")
        self.log.pack(fill="both", expand=True, padx=6, pady=6)
        
        # Log-Tags konfigurieren
        for tag, config in LOG_TAGS.items():
            self.log.tag_config(tag, foreground=config["color"])
        
        # Log-Buttons
        btn_row = tk.Frame(log_box, bg=BG2)
        btn_row.pack(fill="x", padx=6, pady=(0, 6))
        
        tk.Button(btn_row, text="🗑  Log leeren", command=self._clear_log,
                 bg=BG3, fg=SUBTEXT, relief="flat",
                 font=FONT_MAIN, cursor="hand2", padx=10).pack(side="right", padx=4)
        
        tk.Button(btn_row, text="💾  Log speichern", command=self._save_log,
                 bg=BG3, fg=SUBTEXT, relief="flat",
                 font=FONT_MAIN, cursor="hand2", padx=10).pack(side="right", padx=4)
    
    def _build_bottom(self):
        """Untere Leiste: Progress-Bar und Start/Stop Buttons."""
        bottom = tk.Frame(self, bg=BG2, pady=10)
        bottom.pack(fill="x", padx=16, pady=(0, 12))
        
        # Progress-Bar
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("green.Horizontal.TProgressbar",
                       troughcolor=BG3, background=GREEN, thickness=14)
        
        self.progress = ttk.Progressbar(
            bottom, style="green.Horizontal.TProgressbar",
            mode="determinate", maximum=100)
        self.progress.pack(fill="x", padx=10, pady=(0, 8))
        
        # Buttons
        btn_frame = tk.Frame(bottom, bg=BG2)
        btn_frame.pack()
        
        self.start_btn = tk.Button(
            btn_frame, text="▶  PROGRAMMIERUNG STARTEN",
            command=self._start, bg=GREEN, fg=BG,
            font=("Consolas", 11, "bold"),
            relief="flat", cursor="hand2", padx=20, pady=8)
        self.start_btn.pack(side="left", padx=8)
        
        self.stop_btn = tk.Button(
            btn_frame, text="⏹  ABBRECHEN",
            command=self._stop, bg=RED, fg=BG,
            font=("Consolas", 11, "bold"),
            relief="flat", cursor="hand2", padx=20, pady=8, state="disabled")
        self.stop_btn.pack(side="left", padx=8)
        
        # Status-Label
        self.status_var = tk.StringVar(value="Bereit")
        tk.Label(bottom, textvariable=self.status_var,
                bg=BG2, fg=SUBTEXT, font=FONT_MAIN).pack(pady=(6, 0))
    
    # ──────────────────────────────────────────────────────────────
    # Helper Methods
    # ──────────────────────────────────────────────────────────────
    
    def _make_frame(self, parent, title):
        """Erstellt einen stilisierten Frame mit Titel."""
        outer = tk.Frame(parent, bg=BG2, bd=0)
        tk.Label(outer, text=title, bg=BG2, fg=ACCENT2,
                font=FONT_STEP, anchor="w").pack(fill="x", padx=8, pady=(6, 2))
        tk.Frame(outer, bg=BG3, height=1).pack(fill="x", padx=6)
        return outer
    
    def _make_entry_row(self, parent, label, var):
        """Erstellt eine Reihe mit Label und Entry."""
        row = tk.Frame(parent, bg=BG2)
        row.pack(fill="x", padx=6, pady=3)
        tk.Label(row, text=label, bg=BG2, fg=SUBTEXT,
                font=FONT_MAIN, width=22, anchor="w").pack(side="left")
        tk.Entry(row, textvariable=var, bg=BG3, fg=TEXT,
                insertbackground=TEXT, relief="flat",
                font=FONT_MONO, width=20).pack(side="left", ipady=4, padx=(4, 0))
    
    def _make_path_row(self, parent, label, var):
        """Erstellt eine Reihe mit Label, Entry und Browse-Button."""
        row = tk.Frame(parent, bg=BG2)
        row.pack(fill="x", padx=6, pady=3)
        tk.Label(row, text=label, bg=BG2, fg=SUBTEXT,
                font=FONT_MAIN, width=16, anchor="w").pack(side="left")
        tk.Entry(row, textvariable=var, bg=BG3, fg=TEXT,
                insertbackground=TEXT, relief="flat",
                font=FONT_MONO).pack(side="left", fill="x", expand=True,
                                    ipady=4, padx=(4, 6))
        tk.Button(row, text="…", command=lambda v=var: self._browse_tool(v),
                 bg=BG3, fg=ACCENT, relief="flat", cursor="hand2",
                 font=FONT_MAIN, padx=6).pack(side="right")
    
    def _validate_tools(self):
        """Validiert und zeigt Tool-Status an."""
        # Alte Labels löschen
        for w in self.tool_frame.winfo_children():
            if isinstance(w, tk.Frame):
                w.destroy()
        
        tools = {
            "atprogram.exe": self.atprogram_var.get(),
            "atbackend.exe": self.atbackend_var.get(),
            "avr32-objcopy": self.objcopy_var.get(),
        }
        
        for name, path in tools.items():
            import os
            exists = os.path.isfile(path)
            color = GREEN if exists else RED
            icon = "✅" if exists else "❌"
            
            row = tk.Frame(self.tool_frame, bg=BG2)
            row.pack(fill="x", padx=6, pady=2)
            tk.Label(row, text=f"{icon} {name}", bg=BG2, fg=color,
                    font=FONT_MONO).pack(side="left", padx=4)
    
    def _browse_hex(self):
        """Öffnet Dialog zur HEX-Datei-Auswahl."""
        path = filedialog.askopenfilename(
            filetypes=[("HEX Dateien", "*.hex"), ("Alle", "*.*")])
        if path:
            self.hex_file_var.set(path)
    
    def _browse_tool(self, var):
        """Öffnet Dialog zur Tool-Auswahl."""
        path = filedialog.askopenfilename(
            title="Tool auswählen",
            filetypes=[("Ausführbare Dateien", "*.exe"), ("Alle", "*.*")])
        if path:
            var.set(path)
            self._validate_tools()
    
    def _save_settings(self):
        """Speichert alle Einstellungen in settings.json."""
        settings.update({
            "atprogram_path": self.atprogram_var.get(),
            "atbackend_path": self.atbackend_var.get(),
            "objcopy_path": self.objcopy_var.get(),
            "hex_file": self.hex_file_var.get(),
            "val_1fc": self.val_1fc_var.get(),
            "val_1f8": self.val_1f8_var.get(),
            "fuse_val": self.fuse_val_var.get(),
            "chip_erase": self.steps["chip_erase"].get(),
            "user_erase": self.steps["user_erase"].get(),
            "user_write": self.steps["user_write"].get(),
            "flash_write": self.steps["flash_write"].get(),
            "fuse_write": self.steps["fuse_write"].get(),
            "secure": self.steps["secure"].get(),
        })
    
    def _clear_log(self):
        """Löscht den Log."""
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
    
    def _save_log(self):
        """Speichert Log in Datei."""
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textdatei", "*.txt"), ("Alle", "*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.log.get("1.0", "end"))
    
    # ──────────────────────────────────────────────────────────────
    # Controller Callbacks
    # ──────────────────────────────────────────────────────────────
    
    def _on_log(self, entry: LogEntry):
        """Wird aufgerufen wenn etwas geloggt wird."""
        self.log.configure(state="normal")
        self.log.insert("end", entry.message + "\n", entry.tag)
        self.log.see("end")
        self.log.configure(state="disabled")
    
    def _on_status(self, message: str):
        """Aktualisiert Status-Text."""
        self.status_var.set(message)
        self.update_idletasks()
    
    def _on_progress(self, percent: float):
        """Aktualisiert Progress-Bar."""
        self.progress["value"] = percent
        self.update_idletasks()
    
    def _start(self):
        """Startet die Programmierung in separatem Thread."""
        self._clear_log()
        self.progress["value"] = 0
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.controller.abort_requested = False
        
        # In separatem Thread laufen lassen
        threading.Thread(target=self.controller.run, daemon=True).start()
    
    def _stop(self):
        """Fordert Abbruch an."""
        self.controller.request_abort()


def main():
    """Entry Point für die GUI."""
    app = ProgGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
