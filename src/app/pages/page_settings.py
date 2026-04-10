# -*- coding: utf-8 -*-
# src/app/pages/page_settings.py
"""
Settings / Einstellungen Seite
- GeneralTab: Sprache, Auto-Save
- AppearanceTab: Theme + Farben
- ToolsTab: Placeholder
- AboutTab: Placeholder
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ...config.constants import theme_manager, language_manager, ThemeName, Language


class GeneralTab(tk.Frame):
    """TAB 1: Allgemeine Einstellungen."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=theme_manager.get_color("surface"))
        self.parent = parent
        theme_manager.add_theme_listener(self._on_theme_changed)
        language_manager.add_theme_listener(self._on_language_changed)
        self._create_widgets()
        self._load_settings()
    
    def _create_widgets(self):
        main_frame = tk.Frame(self, bg=theme_manager.get_color("surface"))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # SPRACHEN-AUSWAHL
        language_frame = tk.LabelFrame(
            main_frame,
            text="🌐 Language / Sprache",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 10, "bold")
        )
        language_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            language_frame,
            text="Select the user interface language:",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        self.language_var = tk.StringVar()
        self.language_map = {
            "🇩🇪 Deutsch": Language.DEUTSCH,
            "🇬🇧 English": Language.ENGLISH
        }
        
        self.language_dropdown = ttk.Combobox(
            language_frame,
            textvariable=self.language_var,
            values=list(self.language_map.keys()),
            state="readonly",
            width=40,
            font=("Arial", 10)
        )
        self.language_dropdown.pack(fill=tk.X, pady=5)
        self.language_dropdown.bind("<<ComboboxSelected>>", self._on_language_select)
        
        description = tk.Label(
            language_frame,
            text="Choose the language for the user interface.",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("muted"),
            font=("Arial", 9),
            justify=tk.LEFT,
            wraplength=400
        )
        description.pack(anchor=tk.W, pady=5)
        
        # OPTIONS
        options_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Options",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 10, "bold")
        )
        options_frame.pack(fill=tk.X, pady=10)
        
        self.autosave_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Automatically save settings on exit",
            variable=self.autosave_var,
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            selectcolor=theme_manager.get_color("primary"),
            font=("Arial", 10),
            activebackground=theme_manager.get_color("surface"),
            activeforeground=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, pady=5)
        
        self.confirm_exit_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Show confirmation dialog on exit",
            variable=self.confirm_exit_var,
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            selectcolor=theme_manager.get_color("primary"),
            font=("Arial", 10),
            activebackground=theme_manager.get_color("surface"),
            activeforeground=theme_manager.get_color("foreground")
        ).pack(anchor=tk.W, pady=5)
    
    def _load_settings(self):
        current_lang = language_manager.get_current_language().language
        for display_name, lang_enum in self.language_map.items():
            if lang_enum == current_lang:
                self.language_var.set(display_name)
                break
    
    def _on_language_select(self, event=None):
        selected = self.language_var.get()
        if selected in self.language_map:
            new_language = self.language_map[selected]
            language_manager.set_language(new_language)
            messagebox.showinfo("Language Changed", f"Language changed to {selected}.")
    
    def _on_theme_changed(self, new_theme):
        pass
    
    def _on_language_changed(self, new_language):
        pass


class AppearanceTab(tk.Frame):
    """TAB 2: Erscheinungs-Einstellungen."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=theme_manager.get_color("surface"))
        self.parent = parent
        self.theme_buttons = {}
        theme_manager.add_theme_listener(self._on_theme_changed)
        self._create_widgets()
        self._load_settings()
    
    def _create_widgets(self):
        main_frame = tk.Frame(self, bg=theme_manager.get_color("surface"))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # THEME-AUSWAHL
        theme_frame = tk.LabelFrame(
            main_frame,
            text="🎨 Design Theme",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 10, "bold")
        )
        theme_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            theme_frame,
            text="Choose a design theme:",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        self.theme_var = tk.StringVar()
        
        themes = theme_manager.get_available_themes()
        theme_labels = {
            ThemeName.DARK: "🌙 Dark (Dunkel)",
            ThemeName.LIGHT: "☀️ Light (Hell)"
        }
        
        for theme in themes:
            btn = tk.Radiobutton(
                theme_frame,
                text=theme_labels[theme],
                variable=self.theme_var,
                value=theme.value,
                bg=theme_manager.get_color("surface"),
                fg=theme_manager.get_color("foreground"),
                selectcolor=theme_manager.get_color("primary"),
                command=self._on_theme_select,
                font=("Arial", 10),
                activebackground=theme_manager.get_color("surface"),
                activeforeground=theme_manager.get_color("foreground")
            )
            btn.pack(anchor=tk.W, pady=5)
            self.theme_buttons[theme.value] = btn
        
        # FARBEN-VORSCHAU
        preview_frame = tk.LabelFrame(
            main_frame,
            text="🎨 Color Palette",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            padx=15,
            pady=15,
            font=("Arial", 10, "bold")
        )
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        colors_to_show = [
            ("Primary Color", "primary"),
            ("Background", "background"),
            ("Success", "success"),
            ("Error", "error"),
            ("Warning", "warning"),
            ("Info", "info"),
        ]
        
        for color_label, color_key in colors_to_show:
            self._create_color_preview(preview_frame, color_label, color_key)
    
    def _create_color_preview(self, parent, label, color_key):
        frame = tk.Frame(parent, bg=theme_manager.get_color("surface"))
        frame.pack(fill=tk.X, pady=5)
        
        try:
            color = theme_manager.get_color(color_key)
        except KeyError:
            color = "#000000"
        
        color_box = tk.Canvas(
            frame,
            width=30,
            height=30,
            bg=color,
            highlightthickness=1,
            highlightbackground=theme_manager.get_color("border")
        )
        color_box.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            frame,
            text=f"{label}: {color}",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("foreground"),
            font=("Arial", 9),
            width=40,
            anchor=tk.W
        ).pack(side=tk.LEFT)
    
    def _load_settings(self):
        current_theme = theme_manager.get_current_theme().name.value
        self.theme_var.set(current_theme)
    
    def _on_theme_select(self):
        selected = self.theme_var.get()
        for theme_name in ThemeName:
            if theme_name.value == selected:
                theme_manager.set_theme(theme_name)
                break
    
    def _on_theme_changed(self, new_theme):
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
        self._load_settings()


class ToolsTab(tk.Frame):
    """TAB 3: Tool-Pfade (Placeholder)."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=theme_manager.get_color("surface"))
        placeholder_label = tk.Label(
            self,
            text="🔧 Tools Configuration\n\n[Coming Soon]",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("muted"),
            font=("Arial", 14),
            padx=20,
            pady=20
        )
        placeholder_label.pack(fill=tk.BOTH, expand=True)


class AboutTab(tk.Frame):
    """TAB 4: Über ProgGUI (Placeholder)."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=theme_manager.get_color("surface"))
        placeholder_label = tk.Label(
            self,
            text="ℹ️ About ProgGUI\n\n[Coming Soon]",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("muted"),
            font=("Arial", 14),
            padx=20,
            pady=20
        )
        placeholder_label.pack(fill=tk.BOTH, expand=True)


class SettingsNotebook(ttk.Notebook):
    """Haupt-Notebook für Settings-Tabs."""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=theme_manager.get_color("surface"))
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        self.general_tab = GeneralTab(self)
        self.appearance_tab = AppearanceTab(self)
        self.tools_tab = ToolsTab(self)
        self.about_tab = AboutTab(self)
        
        self.add(self.general_tab, text="📋 General")
        self.add(self.appearance_tab, text="🎨 Appearance")
        self.add(self.tools_tab, text="🔧 Tools")
        self.add(self.about_tab, text="ℹ️ About")


class PageSettings(tk.Frame):
    """Settings / Einstellungen Seite."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=theme_manager.get_color("background"))
        self._create_widgets()
        theme_manager.add_theme_listener(self._on_theme_changed)
    
    def _create_widgets(self):
        header = tk.Label(
            self,
            text="⚙️ SETTINGS",
            bg=theme_manager.get_color("surface"),
            fg=theme_manager.get_color("primary"),
            font=("Arial", 20, "bold"),
            pady=15
        )
        header.pack(fill=tk.X)
        
        self.notebook = SettingsNotebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        button_frame = tk.Frame(self, bg=theme_manager.get_color("background"))
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        button_style = {
            "bg": theme_manager.get_color("button_bg"),
            "fg": theme_manager.get_color("button_fg"),
            "activebackground": theme_manager.get_color("button_hover"),
            "activeforeground": theme_manager.get_color("button_fg"),
            "padx": 20,
            "pady": 10,
            "font": ("Arial", 10),
            "relief": tk.RAISED,
            "cursor": "hand2"
        }
        
        tk.Button(
            button_frame,
            text="💾 Save",
            **button_style,
            command=self._save_settings
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            bg=theme_manager.get_color("button_disabled"),
            fg=theme_manager.get_color("button_fg"),
            activebackground=theme_manager.get_color("button_hover"),
            activeforeground=theme_manager.get_color("button_fg"),
            padx=20,
            pady=10,
            font=("Arial", 10),
            relief=tk.RAISED,
            cursor="hand2",
            command=self._close
        ).pack(side=tk.LEFT, padx=5)
    
    def _save_settings(self):
        messagebox.showinfo("Settings Saved", "Settings have been saved successfully!")
    
    def _close(self):
        self.destroy()
    
    def _on_theme_changed(self, new_theme):
        self.configure(bg=theme_manager.get_color("background"))