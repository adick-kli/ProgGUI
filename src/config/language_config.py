# -*- coding: utf-8 -*-
# src/config/language_config.py
"""
Multi-Language System
- Zentrale Übersetzungen
- Dynamischer Sprachen-Wechsel
- Unterstützung für Deutsch, English, etc.
"""

from enum import Enum
from typing import Dict, Callable, List


class Language(Enum):
    """Verfügbare Sprachen."""
    DEUTSCH = "de"
    ENGLISH = "en"


class LanguageStrings:
    """Alle Strings für eine Sprache."""
    
    def __init__(self):
        # ═══════════════════════════════════════════════════════
        # MENÜS
        # ═══════════════════════════════════════════════════════
        self.menu_file: str
        self.menu_programming: str
        self.menu_help: str
        
        # File Menu
        self.menu_home: str
        self.menu_settings: str
        self.menu_device_manager: str
        self.menu_exit: str
        
        # Programming Menu
        self.menu_jtag: str
        self.menu_bootloader: str
        
        # Help Menu
        self.menu_about: str
        self.menu_documentation: str
        
        # ═══════════════════════════════════════════════════════
        # BUTTONS
        # ═══════════════════════════════════════════════════════
        self.btn_start: str
        self.btn_cancel: str
        self.btn_save: str
        self.btn_close: str
        self.btn_browse: str
        self.btn_reset: str
        self.btn_ok: str
        self.btn_new: str
        self.btn_edit: str
        self.btn_delete: str
        
        # ═══════════════════════════════════════════════════════
        # LABELS
        # ═══════════════════════════════════════════════════════
        self.lbl_device: str
        self.lbl_language: str
        self.lbl_theme: str
        self.lbl_status: str
        self.lbl_progress: str
        self.lbl_logs: str
        
        # ═══════════════════════════════════════════════════════
        # PAGE TITLES
        # ═════════════════════════════════════���═════════════════
        self.page_home_title: str
        self.page_home_welcome: str
        self.page_settings_title: str
        self.page_devices_title: str
        self.page_jtag_title: str
        self.page_bootloader_title: str
        
        # ═══════════════════════════════════════════════════════
        # STATUS MESSAGES
        # ═══════════════════════════════════════════════════════
        self.status_ready: str
        self.status_programming: str
        self.status_success: str
        self.status_error: str
        
        # ═══════════════════════════════════════════════════════
        # ERROR MESSAGES
        # ═══════════════════════════════════════════════════════
        self.error_no_device: str
        self.error_no_file: str
        self.error_invalid_path: str
        
        # Custom Strings
        self.custom_strings: Dict[str, str] = {}


class LanguageConfig:
    """Komplette Sprach-Konfiguration."""
    
    def __init__(self, language: Language, strings: LanguageStrings):
        self.language = language
        self.strings = strings
        self.locale = language.value


class LanguageManager:
    """Verwaltet Sprachen und bietet API für Sprachen-Wechsel."""
    
    def __init__(self):
        """Initialisiert den Language Manager."""
        self._languages: Dict[Language, LanguageConfig] = {}
        self._current_language: LanguageConfig = None
        self._callbacks: List[Callable] = []  # Für Language-Change Listeners
        
        # Sprachen registrieren
        self._register_languages()
        
        # Deutsch als Standard
        self.set_language(Language.DEUTSCH)
    
    def _register_languages(self):
        """Registriert alle verfügbaren Sprachen."""
        self._languages[Language.DEUTSCH] = self._create_deutsch()
        self._languages[Language.ENGLISH] = self._create_english()
    
    def _create_deutsch(self) -> LanguageConfig:
        """Erstellt Deutsch-Strings."""
        strings = LanguageStrings()
        
        # ═════════════════════════════════════════════════════
        # MENÜS
        # ═════════════════════════════════════════════════════
        strings.menu_file = "Datei"
        strings.menu_programming = "Programmieren"
        strings.menu_help = "Hilfe"
        
        # File Menu
        strings.menu_home = "🏠 Startseite"
        strings.menu_settings = "⚙️ Einstellungen"
        strings.menu_device_manager = "🔧 Geräte verwalten"
        strings.menu_exit = "❌ Beenden"
        
        # Programming Menu
        strings.menu_jtag = "📌 JTAG Programmierer"
        strings.menu_bootloader = "🚀 Bootloader"
        
        # Help Menu
        strings.menu_about = "ℹ️ Über ProgGUI"
        strings.menu_documentation = "📖 Dokumentation"
        
        # ═════════════════════════════════════════════════════
        # BUTTONS
        # ═════════════════════════════════════════════════════
        strings.btn_start = "▶ Programmierung starten"
        strings.btn_cancel = "⏹ Abbrechen"
        strings.btn_save = "💾 Speichern"
        strings.btn_close = "Schließen"
        strings.btn_browse = "Durchsuchen..."
        strings.btn_reset = "Zurücksetzen"
        strings.btn_ok = "✓ OK"
        strings.btn_new = "+ Neu"
        strings.btn_edit = "✏️ Bearbeiten"
        strings.btn_delete = "🗑️ Löschen"
        
        # ═════════════════════════════════════════════════════
        # LABELS
        # ═════════════════════════════════════════════════════
        strings.lbl_device = "Gerät:"
        strings.lbl_language = "Sprache:"
        strings.lbl_theme = "Design:"
        strings.lbl_status = "Status:"
        strings.lbl_progress = "Fortschritt:"
        strings.lbl_logs = "Protokoll:"
        
        # ═════════════════════════════════════════════════════
        # PAGE TITLES
        # ═════════════════════════════════════════════════════
        strings.page_home_title = "🏠 Startseite"
        strings.page_home_welcome = "Willkommen bei ProgGUI"
        strings.page_settings_title = "⚙️ Einstellungen"
        strings.page_devices_title = "🔧 Geräte verwalten"
        strings.page_jtag_title = "📌 JTAG Programmierer"
        strings.page_bootloader_title = "🚀 Bootloader Programmierer"
        
        # ═════════════════════════════════════════════════════
        # STATUS MESSAGES
        # ═════════════════════════════════════════════════════
        strings.status_ready = "✅ Bereit"
        strings.status_programming = "⏳ Programmierung läuft..."
        strings.status_success = "✅ Programmierung erfolgreich!"
        strings.status_error = "❌ Fehler während Programmierung"
        
        # ═════════════════════════════════════════════════════
        # ERROR MESSAGES
        # ═════════════════════════════════════════════════════
        strings.error_no_device = "Kein Gerät ausgewählt"
        strings.error_no_file = "Keine Datei angegeben"
        strings.error_invalid_path = "Ungültiger Pfad"
        
        return LanguageConfig(Language.DEUTSCH, strings)
    
    def _create_english(self) -> LanguageConfig:
        """Erstellt English-Strings."""
        strings = LanguageStrings()
        
        # ═════════════════════════════════════════════════════
        # MENUS
        # ��════════════════════════════════════════════════════
        strings.menu_file = "File"
        strings.menu_programming = "Programming"
        strings.menu_help = "Help"
        
        # File Menu
        strings.menu_home = "🏠 Home"
        strings.menu_settings = "⚙️ Settings"
        strings.menu_device_manager = "🔧 Device Manager"
        strings.menu_exit = "❌ Exit"
        
        # Programming Menu
        strings.menu_jtag = "📌 JTAG Programmer"
        strings.menu_bootloader = "🚀 Bootloader"
        
        # Help Menu
        strings.menu_about = "ℹ️ About ProgGUI"
        strings.menu_documentation = "📖 Documentation"
        
        # ═════════════════════════════════════════════════════
        # BUTTONS
        # ═════════════════════════════════════════════════════
        strings.btn_start = "▶ Start Programming"
        strings.btn_cancel = "⏹ Cancel"
        strings.btn_save = "💾 Save"
        strings.btn_close = "Close"
        strings.btn_browse = "Browse..."
        strings.btn_reset = "Reset"
        strings.btn_ok = "✓ OK"
        strings.btn_new = "+ New"
        strings.btn_edit = "✏️ Edit"
        strings.btn_delete = "🗑️ Delete"
        
        # ═════════════════════════════════════════════════════
        # LABELS
        # ═════════════════════════════════════════════════════
        strings.lbl_device = "Device:"
        strings.lbl_language = "Language:"
        strings.lbl_theme = "Theme:"
        strings.lbl_status = "Status:"
        strings.lbl_progress = "Progress:"
        strings.lbl_logs = "Logs:"
        
        # ═════════════════════════════════════════════════════
        # PAGE TITLES
        # ═════════════════════════════════════════════════════
        strings.page_home_title = "🏠 Home"
        strings.page_home_welcome = "Welcome to ProgGUI"
        strings.page_settings_title = "⚙️ Settings"
        strings.page_devices_title = "🔧 Device Manager"
        strings.page_jtag_title = "📌 JTAG Programmer"
        strings.page_bootloader_title = "🚀 Bootloader Programmer"
        
        # ═════════════════════════════════════════════════════
        # STATUS MESSAGES
        # ═════════════════════════════════════════════════════
        strings.status_ready = "✅ Ready"
        strings.status_programming = "⏳ Programming..."
        strings.status_success = "✅ Programming successful!"
        strings.status_error = "❌ Error during programming"
        
        # ═════════════════════════════════════════════════════
        # ERROR MESSAGES
        # ═════════════════════════════════════════════════════
        strings.error_no_device = "No device selected"
        strings.error_no_file = "No file specified"
        strings.error_invalid_path = "Invalid path"
        
        return LanguageConfig(Language.ENGLISH, strings)
    
    def set_language(self, language: Language):
        """
        Wechselt zu einer anderen Sprache.
        
        Args:
            language: Language Enum (DEUTSCH oder ENGLISH)
        
        Raises:
            ValueError: Wenn Sprache nicht existiert
        """
        if language not in self._languages:
            raise ValueError(f"Sprache '{language}' existiert nicht!")
        
        self._current_language = self._languages[language]
        
        # Benachrichtige alle Listener
        self._notify_listeners()
    
    def get_current_language(self) -> LanguageConfig:
        """
        Gibt die aktuelle Sprach-Konfiguration zurück.
        
        Returns:
            LanguageConfig: Aktuelle Sprach-Konfiguration
        """
        return self._current_language
    
    def add_language_listener(self, callback: Callable[[LanguageConfig], None]):
        """
        Registriert Callback für Sprachen-Wechsel.
        
        Args:
            callback: Funktion mit LanguageConfig Parameter
        """
        self._callbacks.append(callback)
    
    def _notify_listeners(self):
        """Benachrichtigt alle Listener von Sprachen-Wechsel."""
        for callback in self._callbacks:
            try:
                callback(self._current_language)
            except Exception as e:
                print(f"[ERROR] Language listener failed: {e}")
    
    def get_string(self, string_key: str) -> str:
        """
        Gibt einen String aus der aktuellen Sprache.
        
        Args:
            string_key: Name des Strings (z.B. "btn_start", "menu_file")
        
        Returns:
            str: Übersetzter String
        
        Falls String nicht existiert: Rückgabe "[string_key]"
        """
        strings = self._current_language.strings
        if hasattr(strings, string_key):
            return getattr(strings, string_key)
        return f"[{string_key}]"  # Fallback
    
    def get_available_languages(self) -> List[Language]:
        """
        Gibt alle verfügbaren Sprachen zurück.
        
        Returns:
            List[Language]: Liste aller Sprachen
        """
        return list(self._languages.keys())
    
    def get_language_by_name(self, name: str) -> Language:
        """
        Gibt eine Sprache basierend auf String-Name zurück.
        
        Args:
            name: Sprachen-Name als String ("de" oder "en")
        
        Returns:
            Language: Entsprechendes Enum
        
        Raises:
            ValueError: Wenn Sprache nicht existiert
        """
        for language in Language:
            if language.value == name:
                return language
        raise ValueError(f"Sprache '{name}' nicht gefunden!")


# ═══════════════════════════════════════════════════════════
# GLOBALE INSTANZ
# ═══════════════════════════════════════════════════════════

language_manager = LanguageManager()


# ═══════════════════════════════════════════════════════════
# TEST-CODE
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Test 1: Manager erstellen
    print("Test 1: Manager erstellen")
    print(f"✅ language_manager erstellt")
    
    # Test 2: Deutsch testen
    print("\nTest 2: Deutsch")
    language_manager.set_language(Language.DEUTSCH)
    print(f"Menü Datei: {language_manager.get_string('menu_file')}")
    print(f"Button Start: {language_manager.get_string('btn_start')}")
    
    # Test 3: English testen
    print("\nTest 3: English")
    language_manager.set_language(Language.ENGLISH)
    print(f"Menu File: {language_manager.get_string('menu_file')}")
    print(f"Button Start: {language_manager.get_string('btn_start')}")
    
    # Test 4: Available Languages
    print("\nTest 4: Available Languages")
    for lang in language_manager.get_available_languages():
        print(f"- {lang.value}")
    
    print("\n✅ Alle Tests erfolgreich!")