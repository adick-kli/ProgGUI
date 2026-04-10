# -*- coding: utf-8 -*-
# src/config/styles_config.py
"""
Theme & Styling System
- Zentrale Farbdefinitionen
- Dark & Light Themes
- Dynamischer Theme-Wechsel
- Konsistente UI-Styling
"""

from enum import Enum
from typing import Dict, Any, Callable, List


class ThemeName(Enum):
    """Verfügbare Themes."""
    DARK = "dark"
    LIGHT = "light"


class ColorPalette:
    """Farbpalette für ein Theme."""
    
    def __init__(self):
        # Primärfarben
        self.primary: str           # Hauptfarbe (Button, Links)
        self.primary_dark: str      # Dunkle Variante
        self.primary_light: str     # Helle Variante
        
        # Neutralfarben
        self.background: str        # Fenster-Hintergrund
        self.foreground: str        # Text-Farbe
        self.surface: str           # Panel/Widget-Hintergrund
        
        # Akzentfarben
        self.accent: str            # Hervorhebungen
        self.accent_dark: str
        self.accent_light: str
        
        # Semantische Farben
        self.success: str           # Grün (OK, Success)
        self.warning: str           # Orange (Warning)
        self.error: str             # Rot (Error)
        self.info: str              # Blau (Info)
        
        # UI-Farben
        self.border: str            # Rahmen
        self.border_light: str
        self.border_dark: str
        
        self.button_bg: str         # Button-Hintergrund
        self.button_fg: str         # Button-Text
        self.button_hover: str      # Button bei Hover
        self.button_active: str     # Button bei Klick
        self.button_disabled: str   # Button disabled
        
        self.input_bg: str          # Input-Feld Hintergrund
        self.input_fg: str          # Input-Feld Text
        self.input_border: str      # Input-Feld Rahmen
        
        self.statusbar_bg: str      # Statusleiste Hintergrund
        self.statusbar_fg: str      # Statusleiste Text
        
        self.menubar_bg: str        # Menüleiste Hintergrund
        self.menubar_fg: str        # Menüleiste Text
        
        self.highlight: str         # Hervorhebung
        self.muted: str             # Gedimmt/Grau
        
        # Custom Farben
        self.custom_colors: Dict[str, str] = {}


class ThemeConfig:
    """Komplettes Theme mit Farben, Fonts, Größen."""
    
    def __init__(self, name: ThemeName, palette: ColorPalette):
        self.name = name
        self.palette = palette
        
        # Font-Definitionen
        self.font_family_default: str = "Arial"
        self.font_family_mono: str = "Consolas"
        
        # Font-Größen
        self.font_size_small: int = 9
        self.font_size_normal: int = 10
        self.font_size_medium: int = 11
        self.font_size_large: int = 12
        self.font_size_title: int = 14
        self.font_size_heading: int = 16
        
        # Größen
        self.padding_small: int = 4
        self.padding_normal: int = 8
        self.padding_large: int = 12
        self.padding_xl: int = 16
        
        self.border_radius: int = 4
        self.border_width: int = 1
        
        # Window-Größe
        self.window_width: int = 1200
        self.window_height: int = 800
        self.window_min_width: int = 1024
        self.window_min_height: int = 768
        
        # Component-Größen
        self.button_height: int = 32
        self.button_width_small: int = 80
        self.button_width_medium: int = 120
        self.button_width_large: int = 160
        
        self.toolbar_height: int = 50
        self.statusbar_height: int = 25
        self.menubar_height: int = 25


class ThemeManager:
    """Verwaltet Themes und bietet API für Theme-Wechsel."""
    
    def __init__(self):
        """Initialisiert den Theme Manager."""
        self._themes: Dict[ThemeName, ThemeConfig] = {}
        self._current_theme: ThemeConfig = None
        self._callbacks: List[Callable] = []  # Für Theme-Change Listeners
        
        # Themes registrieren
        self._register_themes()
        
        # Dark als Standard
        self.set_theme(ThemeName.DARK)
    
    def _register_themes(self):
        """Registriert alle verfügbaren Themes."""
        self._themes[ThemeName.DARK] = self._create_dark_theme()
        self._themes[ThemeName.LIGHT] = self._create_light_theme()
    
    def _create_dark_theme(self) -> ThemeConfig:
        """Erstellt Dark Theme."""
        palette = ColorPalette()
        
        # Dark Theme Farben
        palette.background = "#1e1e1e"       # Sehr dunkel
        palette.foreground = "#e0e0e0"       # Helles Grau
        palette.surface = "#2b2b2b"          # Dunkelgrau
        
        palette.primary = "#00d4ff"          # Cyan/Türkis
        palette.primary_dark = "#0099cc"
        palette.primary_light = "#33e5ff"
        
        palette.accent = "#ff6b35"           # Orange
        palette.accent_dark = "#cc5429"
        palette.accent_light = "#ff9966"
        
        palette.success = "#4caf50"          # Grün
        palette.warning = "#ff9800"          # Orange
        palette.error = "#f44336"            # Rot
        palette.info = "#2196f3"             # Blau
        
        palette.border = "#404040"
        palette.border_light = "#505050"
        palette.border_dark = "#303030"
        
        palette.button_bg = "#0099cc"
        palette.button_fg = "#ffffff"
        palette.button_hover = "#00b8e6"
        palette.button_active = "#0077a3"
        palette.button_disabled = "#5a5a5a"
        
        palette.input_bg = "#3a3a3a"
        palette.input_fg = "#e0e0e0"
        palette.input_border = "#505050"
        
        palette.statusbar_bg = "#252525"
        palette.statusbar_fg = "#a0a0a0"
        
        palette.menubar_bg = "#2b2b2b"
        palette.menubar_fg = "#e0e0e0"
        
        palette.highlight = "#00d4ff"
        palette.muted = "#666666"
        
        return ThemeConfig(ThemeName.DARK, palette)
    
    def _create_light_theme(self) -> ThemeConfig:
        """Erstellt Light Theme."""
        palette = ColorPalette()
        
        # Light Theme Farben
        palette.background = "#f5f5f5"       # Sehr hell
        palette.foreground = "#212121"       # Sehr dunkel
        palette.surface = "#ffffff"          # Weiß
        
        palette.primary = "#1976d2"          # Blau
        palette.primary_dark = "#115293"
        palette.primary_light = "#42a5f5"
        
        palette.accent = "#f57c00"           # Orange
        palette.accent_dark = "#c56c00"
        palette.accent_light = "#ffb74d"
        
        palette.success = "#388e3c"          # Grün
        palette.warning = "#f57f17"          # Orange
        palette.error = "#d32f2f"            # Rot
        palette.info = "#1976d2"             # Blau
        
        palette.border = "#e0e0e0"
        palette.border_light = "#f0f0f0"
        palette.border_dark = "#d0d0d0"
        
        palette.button_bg = "#1976d2"
        palette.button_fg = "#ffffff"
        palette.button_hover = "#1565c0"
        palette.button_active = "#0d47a1"
        palette.button_disabled = "#bdbdbd"
        
        palette.input_bg = "#ffffff"
        palette.input_fg = "#212121"
        palette.input_border = "#e0e0e0"
        
        palette.statusbar_bg = "#f5f5f5"
        palette.statusbar_fg = "#616161"
        
        palette.menubar_bg = "#fafafa"
        palette.menubar_fg = "#212121"
        
        palette.highlight = "#1976d2"
        palette.muted = "#9e9e9e"
        
        return ThemeConfig(ThemeName.LIGHT, palette)
    
    def set_theme(self, theme_name: ThemeName):
        """
        Wechselt zu einem anderen Theme.
        
        Args:
            theme_name: ThemeName Enum (DARK oder LIGHT)
        
        Raises:
            ValueError: Wenn Theme nicht existiert
        """
        if theme_name not in self._themes:
            raise ValueError(f"Theme '{theme_name}' existiert nicht!")
        
        self._current_theme = self._themes[theme_name]
        
        # Benachrichtige alle Listener
        self._notify_listeners()
    
    def get_current_theme(self) -> ThemeConfig:
        """
        Gibt das aktuelle Theme zurück.
        
        Returns:
            ThemeConfig: Aktuelles Theme
        """
        return self._current_theme
    
    def add_theme_listener(self, callback: Callable[[ThemeConfig], None]):
        """
        Registriert Callback für Theme-Wechsel.
        
        Args:
            callback: Funktion mit ThemeConfig Parameter
        """
        self._callbacks.append(callback)
    
    def _notify_listeners(self):
        """Benachrichtigt alle Listener von Theme-Wechsel."""
        for callback in self._callbacks:
            try:
                callback(self._current_theme)
            except Exception as e:
                print(f"[ERROR] Theme listener failed: {e}")
    
    def get_palette(self) -> ColorPalette:
        """
        Gibt die Farbpalette des aktuellen Themes.
        
        Returns:
            ColorPalette: Farbpalette
        """
        return self._current_theme.palette
    
    def get_color(self, color_key: str) -> str:
        """
        Gibt eine Farbe aus dem aktuellen Theme.
        
        Args:
            color_key: Name der Farbe (z.B. "primary", "success")
        
        Returns:
            str: Hex-Farbcode (z.B. "#00d4ff")
        
        Raises:
            KeyError: Wenn Farbe nicht existiert
        """
        palette = self.get_palette()
        if hasattr(palette, color_key):
            return getattr(palette, color_key)
        raise KeyError(f"Farbe '{color_key}' nicht gefunden!")
    
    def get_available_themes(self) -> List[ThemeName]:
        """
        Gibt alle verfügbaren Themes zurück.
        
        Returns:
            List[ThemeName]: Liste aller Themes
        """
        return list(self._themes.keys())
    
    def get_theme_by_name(self, name: str) -> ThemeName:
        """
        Gibt ein Theme basierend auf String-Name zurück.
        
        Args:
            name: Theme-Name als String ("dark" oder "light")
        
        Returns:
            ThemeName: Entsprechendes Enum
        
        Raises:
            ValueError: Wenn Theme nicht existiert
        """
        for theme_name in ThemeName:
            if theme_name.value == name:
                return theme_name
        raise ValueError(f"Theme '{name}' nicht gefunden!")


# ═══════════════════════════════════════════════════════════
# GLOBALE INSTANZ
# ═══════════════════════════════════════════════════════════

theme_manager = ThemeManager()
