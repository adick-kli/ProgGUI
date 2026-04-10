# -*- coding: utf-8 -*-
# src/app/pages/page_jtag.py
"""
JTAG Programmer Seite
- Geräte-Auswahl
- Firmware-Datei auswählen
- Programmierung starten/stoppen
- Progress-Bar + Logs
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time

from ...config.constants import theme_manager


class PageJTAG(tk.Frame):
    """JTAG Programmer Seite."""
    
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=theme_manager.get_color("background")
        )
        
        self.is_programming = False
        self.selected_file = None
        self.programming_thread = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Erstellt alle Widgets für die JTAG Programmer Seite."""
        
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
            text="📌 JTAG PROGRAMMER",
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
        
        # ═════════════════════════════════════════════════════
        # DEVICE SELECTION
        # ═════════════════════════════════════════════════════
        
        device_frame = tk.LabelFrame(
            main_frame,
            text="🔧 Select Device",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 11, "bold")
        )
        device_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            device_frame,
            text="Device:",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        self.device_var = tk.StringVar(value="Atmel-ICE")
        device_dropdown = ttk.Combobox(
            device_frame,
            textvariable=self.device_var,
            values=["Atmel-ICE", "SAM-ICE", "J-Link"],
            state="readonly",
            width=40,
            font=("Arial", 10)
        )
        device_dropdown.pack(fill=tk.X, pady=5)
        
        # ═════════════════════════════════════════════════════
        # FILE SELECTION
        # ═════════════════════════════════════════════════════
        
        file_frame = tk.LabelFrame(
            main_frame,
            text="📁 Select Firmware File",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 11, "bold")
        )
        file_frame.pack(fill=tk.X, pady=10)
        
        file_button_frame = tk.Frame(file_frame, bg=theme_manager.get_color("surface"))
        file_button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            file_button_frame,
            text="📂 Browse File...",
            bg=theme_manager.get_color("button_bg"),
            fg=theme_manager.get_color("button_fg"),
            activebackground=theme_manager.get_color("button_hover"),
            activeforeground=theme_manager.get_color("button_fg"),
            padx=15,
            pady=8,
            font=("Arial", 10),
            relief=tk.RAISED,
            cursor="hand2",
            command=self._browse_file
        ).pack(side=tk.LEFT, padx=5)
        
        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("muted"),
            font=("Arial", 10)
        )
        self.file_label.pack(anchor=tk.W, pady=10)
        
        # ═════════════════════════════════════════════════════
        # PROGRAMMING OPTIONS
        # ═════════════════════════════════════════════════════
        
        options_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Programming Options",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 11, "bold")
        )
        options_frame.pack(fill=tk.X, pady=10)
        
        self.verify_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Verify after programming",
            variable=self.verify_var,
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            selectcolor=theme_manager.get_color("primary"),
            font=("Arial", 10),
            activebackground=theme_manager.get_color("surface"),
            activeforeground=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, pady=5)
        
        self.erase_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            options_frame,
            text="Erase before programming",
            variable=self.erase_var,
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            selectcolor=theme_manager.get_color("primary"),
            font=("Arial", 10),
            activebackground=theme_manager.get_color("surface"),
            activeforeground=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, pady=5)
        
        # ═════════════════════════════════════════════════════
        # PROGRESS BAR
        # ═════════════════════════════════════════════════════
        
        progress_frame = tk.LabelFrame(
            main_frame,
            text="📊 Progress",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 11, "bold")
        )
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            font=("Arial", 10)
        )
        self.progress_label.pack(anchor=tk.W)
        
        # ═════════════════════════════════════════════════════
        # LOG OUTPUT
        # ═════════════════════════════════════════════════════
        
        log_frame = tk.LabelFrame(
            main_frame,
            text="📋 Log Output",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 11, "bold")
        )
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar für Log
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text Widget für Logs
        self.log_text = tk.Text(
            log_frame,
            height=8,
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("foreground"),
            yscrollcommand=scrollbar.set,
            font=("Courier", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Clear Logs Button
        tk.Button(
            log_frame,
            text="🗑️ Clear Logs",
            bg=theme_manager.get_color("button_bg"),
            fg=theme_manager.get_color("button_fg"),
            activebackground=theme_manager.get_color("button_hover"),
            activeforeground=theme_manager.get_color("button_fg"),
            padx=10,
            pady=5,
            font=("Arial", 9),
            relief=tk.RAISED,
            cursor="hand2",
            command=self._clear_logs
        ).pack(anchor=tk.W, pady=(5, 0))
        
        # ═════════════════════════════════════════════════════
        # ACTION BUTTONS
        # ═════════════════════════════════════════════════════
        
        button_frame = tk.Frame(main_frame, bg=theme_manager.get_color("background"))
        button_frame.pack(fill=tk.X, pady=20)
        
        button_style = {
            "padx": 20,
            "pady": 10,
            "font": ("Arial", 10),
            "relief": tk.RAISED,
            "cursor": "hand2"
        }
        
        self.start_button = tk.Button(
            button_frame,
            text="▶️ Start Programming",
            bg=theme_manager.get_color("button_bg"),
            fg=theme_manager.get_color("button_fg"),
            activebackground=theme_manager.get_color("button_hover"),
            activeforeground=theme_manager.get_color("button_fg"),
            **button_style,
            command=self._start_programming
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹️ Stop",
            bg=theme_manager.get_color("button_disabled"),
            fg=theme_manager.get_color("button_fg"),
            activebackground=theme_manager.get_color("button_hover"),
            activeforeground=theme_manager.get_color("button_fg"),
            **button_style,
            command=self._stop_programming,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Initial log message
        self._log("JTAG Programmer initialized")
        self._log(f"Device: {self.device_var.get()}")
        self._log("Ready to program")
    
    def _browse_file(self):
        """Öffnet einen File Browser."""
        file_path = filedialog.askopenfilename(
            title="Select Firmware File",
            filetypes=[("Binary Files", "*.bin"), ("Hex Files", "*.hex"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.selected_file = file_path
            file_name = file_path.split("/")[-1]
            self.file_label.config(
                text=f"✅ {file_name}",
                fg=theme_manager.get_color("success")
            )
            self._log(f"[FILE] Selected: {file_name}")
    
    def _start_programming(self):
        """Startet die Programmierung."""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a firmware file first!")
            return
        
        self.is_programming = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self._log("[START] Programming started...")
        
        # Starte Programmierung in separatem Thread
        self.programming_thread = threading.Thread(target=self._simulate_programming, daemon=True)
        self.programming_thread.start()
    
    def _simulate_programming(self):
        """Simuliert den Programmierungsprozess mit korrektem Thread-Handling."""
        device = self.device_var.get()
        
        try:
            self._log(f"[DEVICE] Connecting to {device}...")
            time.sleep(0.5)
            self._log("[DEVICE] Connected")
            time.sleep(0.5)
            
            if self.erase_var.get():
                self._log("[ERASE] Erasing flash memory...")
                for i in range(0, 101, 10):
                    if not self.is_programming:
                        return
                    self.progress_var.set(i)
                    self.progress_label.config(text=f"Erasing: {i}%")
                    time.sleep(0.3)
                self._log("[ERASE] Flash memory erased")
            
            self._log("[PROGRAM] Programming...")
            for i in range(0, 101, 5):
                if not self.is_programming:
                    return
                self.progress_var.set(i)
                self.progress_label.config(text=f"Programming: {i}%")
                time.sleep(0.15)
            
            if self.verify_var.get():
                self._log("[VERIFY] Verifying...")
                for i in range(0, 101, 10):
                    if not self.is_programming:
                        return
                    self.progress_var.set(i)
                    self.progress_label.config(text=f"Verifying: {i}%")
                    time.sleep(0.3)
                self._log("[VERIFY] Verification successful")
            
            if self.is_programming:
                self.progress_var.set(100)
                self.progress_label.config(
                    text="✅ Programming completed successfully!",
                    fg=theme_manager.get_color("success")
                )
                self._log("[SUCCESS] Programming completed!")
                messagebox.showinfo("Success", "Programming completed successfully!")
            else:
                self.progress_label.config(text="Stopped by user")
                self._log("[STOPPED] Programming stopped by user")
                
        except Exception as e:
            self._log(f"[ERROR] {str(e)}")
            messagebox.showerror("Error", f"Programming failed: {str(e)}")
        
        finally:
            self.is_programming = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def _stop_programming(self):
        """Stoppt die Programmierung."""
        self.is_programming = False
        self._log("[STOP] Programming stopped")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def _log(self, message):
        """Fügt eine Log-Nachricht hinzu."""
        try:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        except:
            pass
    
    def _clear_logs(self):
        """Löscht alle Logs."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self._log("Logs cleared")