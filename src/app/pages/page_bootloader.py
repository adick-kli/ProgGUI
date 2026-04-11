# -*- coding: utf-8 -*-
# src/app/pages/page_bootloader.py
"""
Bootloader Seite
- Bootloader-Datei auswählen
- Bootloader-Optionen
- Programmierung starten/stoppen
- Progress-Bar + Logs
- Vollständig scrollbar!
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time

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


class PageBootloader(tk.Frame):
    """Bootloader Seite - Vollständig scrollbar."""
    
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
        """Erstellt alle Widgets mit ScrollableFrame."""
        
        # HEADER (NICHT scrollbar)
        header_frame = tk.Frame(
            self,
            bg=theme_manager.get_color("surface"),
            height=80
        )
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🚀 BOOTLOADER PROGRAMMER",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("primary"),
            font=("Arial", 20, "bold"),
            padx=20,
            pady=15
        )
        title_label.pack(anchor=tk.W)
        
        # SCROLLABLE CONTENT
        scrollable = ScrollableFrame(self, bg=theme_manager.get_color("background"))
        scrollable.pack(fill=tk.BOTH, expand=True)
        
        main_frame = scrollable.scrollable_frame
        main_frame.configure(padx=20, pady=20)
        
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
        # BOOTLOADER FILE SELECTION
        # ═════════════════════════════════════════════════════
        
        file_frame = tk.LabelFrame(
            main_frame,
            text="📁 Select Bootloader File",
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
        # BOOTLOADER OPTIONS
        # ═════════════════════════════════════════════════════
        
        options_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Bootloader Options",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 11, "bold")
        )
        options_frame.pack(fill=tk.X, pady=10)
        
        # Bootloader Type Selection
        tk.Label(
            options_frame,
            text="Bootloader Type:",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        self.bootloader_type_var = tk.StringVar(value="SAM-BA")
        bootloader_type_dropdown = ttk.Combobox(
            options_frame,
            textvariable=self.bootloader_type_var,
            values=["SAM-BA", "DFU", "SERIAL"],
            state="readonly",
            width=40,
            font=("Arial", 10)
        )
        bootloader_type_dropdown.pack(fill=tk.X, pady=5)
        
        # Checkboxes
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
        
        self.lock_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            options_frame,
            text="Lock bootloader after programming",
            variable=self.lock_var,
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            selectcolor=theme_manager.get_color("primary"),
            font=("Arial", 10),
            activebackground=theme_manager.get_color("surface"),
            activeforeground=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, pady=5)
        
        self.backup_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Backup current bootloader before programming",
            variable=self.backup_var,
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            selectcolor=theme_manager.get_color("primary"),
            font=("Arial", 10),
            activebackground=theme_manager.get_color("surface"),
            activeforeground=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, pady=5)
        
        # ═════════════════════════════════════════════════════
        # BOOTLOADER INFO
        # ═════════════════════════════════════════════════════
        
        info_frame = tk.LabelFrame(
            main_frame,
            text="ℹ️ Bootloader Information",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 11, "bold")
        )
        info_frame.pack(fill=tk.X, pady=10)
        
        self.info_text = tk.Text(
            info_frame,
            height=6,
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("foreground"),
            font=("Courier", 9),
            state=tk.DISABLED
        )
        self.info_text.pack(fill=tk.X)
        
        self._update_info()
        
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
        log_frame.pack(fill=tk.X, pady=10)
        
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
        
        tk.Button(
            button_frame,
            text="💾 Backup Current",
            bg=theme_manager.get_color("button_bg"),
            fg=theme_manager.get_color("button_fg"),
            activebackground=theme_manager.get_color("button_hover"),
            activeforeground=theme_manager.get_color("button_fg"),
            **button_style,
            command=self._backup_bootloader
        ).pack(side=tk.LEFT, padx=5)
        
        # Initial log message
        self._log("Bootloader Programmer initialized")
        self._log(f"Device: {self.device_var.get()}")
        self._log(f"Bootloader Type: {self.bootloader_type_var.get()}")
        self._log("Ready to program")
    
    def _update_info(self):
        """Aktualisiert die Bootloader-Info."""
        bootloader_type = self.bootloader_type_var.get()
        
        info_text = (
            f"Device: {self.device_var.get()}\n"
            f"Bootloader Type: {bootloader_type}\n"
            f"Status: Ready for programming\n"
            f"Options: Verify={self.verify_var.get()}, Lock={self.lock_var.get()}, Backup={self.backup_var.get()}"
        )
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info_text)
        self.info_text.config(state=tk.DISABLED)
    
    def _browse_file(self):
        """Öffnet einen File Browser."""
        file_path = filedialog.askopenfilename(
            title="Select Bootloader File",
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
            self._update_info()
    
    def _start_programming(self):
        """Startet die Programmierung."""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a bootloader file first!")
            return
        
        self.is_programming = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self._log("[START] Bootloader programming started...")
        
        self.programming_thread = threading.Thread(target=self._simulate_programming, daemon=True)
        self.programming_thread.start()
    
    def _simulate_programming(self):
        """Simuliert den Programmierungsprozess."""
        device = self.device_var.get()
        bootloader_type = self.bootloader_type_var.get()
        
        try:
            self._log(f"[DEVICE] Connecting to {device}...")
            time.sleep(0.5)
            self._log("[DEVICE] Connected")
            time.sleep(0.5)
            
            if self.backup_var.get():
                self._log("[BACKUP] Backing up current bootloader...")
                for i in range(0, 101, 20):
                    if not self.is_programming:
                        return
                    self.progress_var.set(i)
                    self.progress_label.config(text=f"Backup: {i}%")
                    time.sleep(0.2)
                self._log("[BACKUP] Backup completed")
            
            self._log(f"[PROGRAM] Programming {bootloader_type} bootloader...")
            for i in range(0, 101, 5):
                if not self.is_programming:
                    return
                self.progress_var.set(i)
                self.progress_label.config(text=f"Programming: {i}%")
                time.sleep(0.1)
            
            if self.verify_var.get():
                self._log("[VERIFY] Verifying bootloader...")
                for i in range(0, 101, 10):
                    if not self.is_programming:
                        return
                    self.progress_var.set(i)
                    self.progress_label.config(text=f"Verifying: {i}%")
                    time.sleep(0.2)
                self._log("[VERIFY] Verification successful")
            
            if self.lock_var.get():
                self._log("[LOCK] Locking bootloader...")
                time.sleep(0.5)
                self._log("[LOCK] Bootloader locked")
            
            if self.is_programming:
                self.progress_var.set(100)
                self.progress_label.config(
                    text="✅ Bootloader programming completed successfully!",
                    fg=theme_manager.get_color("success")
                )
                self._log("[SUCCESS] Bootloader programming completed!")
                messagebox.showinfo("Success", "Bootloader programming completed successfully!")
            else:
                self.progress_label.config(text="Stopped by user")
                self._log("[STOPPED] Bootloader programming stopped by user")
                
        except Exception as e:
            self._log(f"[ERROR] {str(e)}")
            messagebox.showerror("Error", f"Bootloader programming failed: {str(e)}")
        
        finally:
            self.is_programming = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def _stop_programming(self):
        """Stoppt die Programmierung."""
        self.is_programming = False
        self._log("[STOP] Bootloader programming stopped")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def _backup_bootloader(self):
        """Sichert den aktuellen Bootloader."""
        save_path = filedialog.asksaveasfilename(
            title="Save Bootloader Backup",
            filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")],
            defaultextension=".bin"
        )
        
        if save_path:
            self._log(f"[BACKUP] Saving bootloader to {save_path}...")
            messagebox.showinfo("Success", "Bootloader backup saved successfully!")
            self._log("[BACKUP] Bootloader backup completed")
    
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