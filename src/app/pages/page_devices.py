# -*- coding: utf-8 -*-
# src/app/pages/page_devices.py
"""
Device Manager Seite
- Geräteliste anzeigen
- Gerät hinzufügen/bearbeiten/löschen
- Device-Details anzeigen
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from ...config.constants import theme_manager


class PageDevices(tk.Frame):
    """Device Manager Seite."""
    
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=theme_manager.get_color("background")
        )
        
        # Mock-Daten (später aus Datenbank)
        self.devices = [
            {"id": 1, "name": "Atmel-ICE", "type": "JTAG", "port": "USB", "status": "Connected"},
            {"id": 2, "name": "SAM-ICE", "type": "JTAG", "port": "USB", "status": "Disconnected"},
            {"id": 3, "name": "J-Link", "type": "SWD", "port": "USB", "status": "Connected"},
        ]
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Erstellt alle Widgets für die Device Manager Seite."""
        
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
            text="🔧 DEVICE MANAGER",
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
        # TOOLBAR BUTTONS
        # ═════════════════════════════════════════════════════
        
        toolbar_frame = tk.Frame(main_frame, bg=theme_manager.get_color("background"))
        toolbar_frame.pack(fill=tk.X, pady=(0, 20))
        
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
            toolbar_frame,
            text="➕ Add Device",
            **button_style,
            command=self._add_device
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar_frame,
            text="✏️ Edit Device",
            **button_style,
            command=self._edit_device
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar_frame,
            text="🗑️ Delete Device",
            **button_style,
            command=self._delete_device
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar_frame,
            text="🔄 Refresh",
            **button_style,
            command=self._refresh_devices
        ).pack(side=tk.LEFT, padx=5)
        
        # ════════════════════════��════════════════════════════
        # DEVICE LIST (Treeview)
        # ═════════════════════════════════════════════════════
        
        list_frame = tk.LabelFrame(
            main_frame,
            text="📋 Connected Devices",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 11, "bold")
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Name", "Type", "Port", "Status"),
            height=12,
            yscrollcommand=scrollbar.set
        )
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.W, width=40)
        self.tree.column("Name", anchor=tk.W, width=150)
        self.tree.column("Type", anchor=tk.W, width=100)
        self.tree.column("Port", anchor=tk.W, width=80)
        self.tree.column("Status", anchor=tk.W, width=100)
        
        # Configure headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Name", text="Device Name", anchor=tk.W)
        self.tree.heading("Type", text="Type", anchor=tk.W)
        self.tree.heading("Port", text="Port", anchor=tk.W)
        self.tree.heading("Status", text="Status", anchor=tk.W)
        
        # Add devices to tree
        self._populate_tree()
        
        # ═════════════════════════════════════════════════════
        # INFO FRAME
        # ═════════════════════════════════════════════════════
        
        info_frame = tk.LabelFrame(
            main_frame,
            text="ℹ️ Device Information",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 10, "bold")
        )
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.info_label = tk.Label(
            info_frame,
            text="Select a device to view its details",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("muted"),
            font=("Arial", 10),
            justify=tk.LEFT
        )
        self.info_label.pack(anchor=tk.W)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self._on_device_select)
    
    def _populate_tree(self):
        """Füllt die Treeview mit Devices."""
        # Löschen Sie alte Items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fügen Sie neue Items hinzu
        for device in self.devices:
            status_color = "✅" if device["status"] == "Connected" else "❌"
            self.tree.insert(
                "",
                "end",
                values=(
                    device["id"],
                    device["name"],
                    device["type"],
                    device["port"],
                    f"{status_color} {device['status']}"
                )
            )
    
    def _on_device_select(self, event):
        """Wird aufgerufen wenn ein Device ausgewählt wird."""
        selection = self.tree.selection()
        
        if not selection:
            return
        
        # Get selected item
        item = selection[0]
        values = self.tree.item(item, "values")
        
        if values:
            device_id = int(values[0])
            device = next((d for d in self.devices if d["id"] == device_id), None)
            
            if device:
                info_text = (
                    f"📌 Device ID: {device['id']}\n"
                    f"📛 Name: {device['name']}\n"
                    f"🔌 Type: {device['type']}\n"
                    f"🖇️ Port: {device['port']}\n"
                    f"🔋 Status: {device['status']}"
                )
                self.info_label.config(text=info_text)
    
    def _add_device(self):
        """Fügt ein neues Device hinzu."""
        dialog = tk.Toplevel(self)
        dialog.title("Add Device")
        dialog.geometry("400x300")
        dialog.configure(bg=theme_manager.get_color("background"))
        
        # Labels und Entry-Felder
        tk.Label(
            dialog,
            text="Device Name:",
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        name_entry = tk.Entry(dialog, width=40)
        name_entry.pack(padx=20, pady=(0, 15))
        
        tk.Label(
            dialog,
            text="Device Type:",
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, padx=20, pady=(0, 5))
        
        type_var = tk.StringVar(value="JTAG")
        type_dropdown = ttk.Combobox(
            dialog,
            textvariable=type_var,
            values=["JTAG", "SWD", "ISP"],
            state="readonly",
            width=37
        )
        type_dropdown.pack(padx=20, pady=(0, 15))
        
        tk.Label(
            dialog,
            text="Port:",
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, padx=20, pady=(0, 5))
        
        port_var = tk.StringVar(value="USB")
        port_dropdown = ttk.Combobox(
            dialog,
            textvariable=port_var,
            values=["USB", "COM", "LPT"],
            state="readonly",
            width=37
        )
        port_dropdown.pack(padx=20, pady=(0, 20))
        
        def save_device():
            name = name_entry.get()
            if not name:
                messagebox.showerror("Error", "Please enter a device name!")
                return
            
            new_device = {
                "id": max([d["id"] for d in self.devices]) + 1,
                "name": name,
                "type": type_var.get(),
                "port": port_var.get(),
                "status": "Connected"
            }
            
            self.devices.append(new_device)
            self._populate_tree()
            messagebox.showinfo("Success", f"Device '{name}' added successfully!")
            dialog.destroy()
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=theme_manager.get_color("background"))
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(
            button_frame,
            text="Save",
            command=save_device,
            bg=theme_manager.get_color("button_bg"),
            fg=theme_manager.get_color("button_fg"),
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=theme_manager.get_color("button_disabled"),
            fg=theme_manager.get_color("button_fg"),
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
    
    def _edit_device(self):
        """Bearbeitet das ausgewählte Device."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a device to edit!")
            return
        
        item = selection[0]
        values = self.tree.item(item, "values")
        device_id = int(values[0])
        device = next((d for d in self.devices if d["id"] == device_id), None)
        
        if not device:
            return
        
        dialog = tk.Toplevel(self)
        dialog.title("Edit Device")
        dialog.geometry("400x300")
        dialog.configure(bg=theme_manager.get_color("background"))
        
        tk.Label(
            dialog,
            text="Device Name:",
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        name_entry = tk.Entry(dialog, width=40)
        name_entry.insert(0, device["name"])
        name_entry.pack(padx=20, pady=(0, 15))
        
        tk.Label(
            dialog,
            text="Device Type:",
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, padx=20, pady=(0, 5))
        
        type_var = tk.StringVar(value=device["type"])
        type_dropdown = ttk.Combobox(
            dialog,
            textvariable=type_var,
            values=["JTAG", "SWD", "ISP"],
            state="readonly",
            width=37
        )
        type_dropdown.pack(padx=20, pady=(0, 15))
        
        tk.Label(
            dialog,
            text="Port:",
            bg=theme_manager.get_color("background"),
            fg=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, padx=20, pady=(0, 5))
        
        port_var = tk.StringVar(value=device["port"])
        port_dropdown = ttk.Combobox(
            dialog,
            textvariable=port_var,
            values=["USB", "COM", "LPT"],
            state="readonly",
            width=37
        )
        port_dropdown.pack(padx=20, pady=(0, 20))
        
        def save_changes():
            device["name"] = name_entry.get()
            device["type"] = type_var.get()
            device["port"] = port_var.get()
            self._populate_tree()
            messagebox.showinfo("Success", "Device updated successfully!")
            dialog.destroy()
        
        button_frame = tk.Frame(dialog, bg=theme_manager.get_color("background"))
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(
            button_frame,
            text="Save",
            command=save_changes,
            bg=theme_manager.get_color("button_bg"),
            fg=theme_manager.get_color("button_fg"),
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=theme_manager.get_color("button_disabled"),
            fg=theme_manager.get_color("button_fg"),
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
    
    def _delete_device(self):
        """Löscht das ausgewählte Device."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a device to delete!")
            return
        
        item = selection[0]
        values = self.tree.item(item, "values")
        device_id = int(values[0])
        device = next((d for d in self.devices if d["id"] == device_id), None)
        
        if not device:
            return
        
        if messagebox.askyesno("Confirm", f"Delete device '{device['name']}'?"):
            self.devices.remove(device)
            self._populate_tree()
            self.info_label.config(text="Select a device to view its details")
            messagebox.showinfo("Success", "Device deleted successfully!")
    
    def _refresh_devices(self):
        """Aktualisiert die Geräteliste."""
        self._populate_tree()
        messagebox.showinfo("Refresh", "Device list refreshed!")