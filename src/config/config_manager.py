# -*- coding: utf-8 -*-
# src/config/config_manager.py
"""
Configuration Manager
- settings.ini für App-Konfiguration
- Theme, Language, Fenster-Größe persistieren
- Benutzereinstellungen speichern/laden
"""

import configparser
from pathlib import Path


class ConfigManager:
    """Verwaltet die App-Konfiguration über INI-Datei."""
    
    def __init__(self, config_path: str = None):
        """Initialisiert den Config Manager."""
        if config_path is None:
            # Erstelle config im data/ Verzeichnis
            data_dir = Path(__file__).parent.parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            config_path = data_dir / "settings.ini"
        
        self.config_path = Path(config_path)
        self.config = configparser.ConfigParser()
        self._load_or_create_config()
    
    def _load_or_create_config(self):
        """Lädt Config oder erstellt Standard-Config."""
        if self.config_path.exists():
            self.config.read(self.config_path)
            print(f"[CONFIG] Konfiguration geladen: {self.config_path}")
        else:
            self._create_default_config()
            self.save()
            print(f"[CONFIG] Standard-Konfiguration erstellt: {self.config_path}")
    
    def _create_default_config(self):
        """Erstellt Standard-Konfiguration."""
        
        # APP Settings
        self.config['APP'] = {
            'version': '1.0.0',
            'app_name': 'ProgGUI',
            'auto_save': 'true',
            'show_startup_message': 'true'
        }
        
        # THEME Settings
        self.config['THEME'] = {
            'current_theme': 'dark',
            'auto_theme': 'false'
        }
        
        # LANGUAGE Settings
        self.config['LANGUAGE'] = {
            'current_language': 'deutsch',
            'auto_detect': 'false'
        }
        
        # WINDOW Settings
        self.config['WINDOW'] = {
            'width': '1200',
            'height': '700',
            'x_pos': '100',
            'y_pos': '100',
            'maximized': 'false'
        }
        
        # DEVICES Settings
        self.config['DEVICES'] = {
            'auto_detect': 'false',
            'default_device': 'Atmel-ICE',
            'timeout_seconds': '30'
        }
        
        # PROGRAMMER Settings
        self.config['PROGRAMMER'] = {
            'verify_after_program': 'true',
            'erase_before_program': 'false',
            'backup_before_program': 'true',
            'lock_after_program': 'false'
        }
        
        # BOOTLOADER Settings
        self.config['BOOTLOADER'] = {
            'default_type': 'sam-ba',
            'verify_after_program': 'true',
            'lock_after_program': 'false',
            'backup_before_program': 'true'
        }
        
        # PATHS Settings
        self.config['PATHS'] = {
            'firmware_dir': './firmware',
            'backup_dir': './backups',
            'export_dir': './export'
        }
        
        # LOGGING Settings
        self.config['LOGGING'] = {
            'log_level': 'info',
            'log_file': './logs/proggui.log',
            'keep_logs': 'true',
            'max_log_size_mb': '10'
        }
    
    # ═════════════════════════════════════════════════════
    # APP SETTINGS
    # ═════════════════════════════════════════════════════
    
    def get_app_version(self) -> str:
        """Holt die App-Version."""
        return self.get('APP', 'version', '1.0.0')
    
    def get_app_name(self) -> str:
        """Holt den App-Namen."""
        return self.get('APP', 'app_name', 'ProgGUI')
    
    def get_auto_save(self) -> bool:
        """Holt Auto-Save Einstellung."""
        return self.get_bool('APP', 'auto_save', True)
    
    def set_auto_save(self, value: bool):
        """Setzt Auto-Save Einstellung."""
        self.set('APP', 'auto_save', str(value).lower())
    
    # ═════════════════════════════════════════════════════
    # THEME SETTINGS
    # ═════════════════════════════════════════════════════
    
    def get_current_theme(self) -> str:
        """Holt das aktuelle Theme."""
        return self.get('THEME', 'current_theme', 'dark')
    
    def set_current_theme(self, theme: str):
        """Speichert das aktuelle Theme."""
        self.set('THEME', 'current_theme', theme)
    
    def get_auto_theme(self) -> bool:
        """Holt Auto-Theme Einstellung."""
        return self.get_bool('THEME', 'auto_theme', False)
    
    def set_auto_theme(self, value: bool):
        """Setzt Auto-Theme Einstellung."""
        self.set('THEME', 'auto_theme', str(value).lower())
    
    # ═════════════════════════════════════════════════════
    # LANGUAGE SETTINGS
    # ═════════════════════════════════════════════════════
    
    def get_current_language(self) -> str:
        """Holt die aktuelle Sprache."""
        return self.get('LANGUAGE', 'current_language', 'deutsch')
    
    def set_current_language(self, language: str):
        """Speichert die aktuelle Sprache."""
        self.set('LANGUAGE', 'current_language', language)
    
    def get_auto_detect_language(self) -> bool:
        """Holt Auto-Detect Sprache Einstellung."""
        return self.get_bool('LANGUAGE', 'auto_detect', False)
    
    # ═════════════════════════════════════════════════════
    # WINDOW SETTINGS
    # ═════════════════════════════════════════════════════
    
    def get_window_geometry(self) -> tuple:
        """Holt Fenster-Größe (width, height)."""
        width = self.get_int('WINDOW', 'width', 1200)
        height = self.get_int('WINDOW', 'height', 700)
        return (width, height)
    
    def set_window_geometry(self, width: int, height: int):
        """Speichert Fenster-Größe."""
        self.set('WINDOW', 'width', str(width))
        self.set('WINDOW', 'height', str(height))
    
    def get_window_position(self) -> tuple:
        """Holt Fenster-Position (x, y)."""
        x = self.get_int('WINDOW', 'x_pos', 100)
        y = self.get_int('WINDOW', 'y_pos', 100)
        return (x, y)
    
    def set_window_position(self, x: int, y: int):
        """Speichert Fenster-Position."""
        self.set('WINDOW', 'x_pos', str(x))
        self.set('WINDOW', 'y_pos', str(y))
    
    def get_window_maximized(self) -> bool:
        """Holt Fenster-Maximiert Status."""
        return self.get_bool('WINDOW', 'maximized', False)
    
    def set_window_maximized(self, value: bool):
        """Speichert Fenster-Maximiert Status."""
        self.set('WINDOW', 'maximized', str(value).lower())
    
    # ═════════════════════════════════════════════════════
    # DEVICES SETTINGS
    # ═════════════════════════════════════════════════════
    
    def get_default_device(self) -> str:
        """Holt Default-Device."""
        return self.get('DEVICES', 'default_device', 'Atmel-ICE')
    
    def set_default_device(self, device: str):
        """Speichert Default-Device."""
        self.set('DEVICES', 'default_device', device)
    
    def get_device_timeout(self) -> int:
        """Holt Device-Timeout in Sekunden."""
        return self.get_int('DEVICES', 'timeout_seconds', 30)
    
    def set_device_timeout(self, seconds: int):
        """Speichert Device-Timeout."""
        self.set('DEVICES', 'timeout_seconds', str(seconds))
    
    # ═════════════════════════════════════════════════════
    # PROGRAMMER SETTINGS
    # ═════════════════════════════════════════════════════
    
    def get_programmer_settings(self) -> dict:
        """Holt alle Programmer-Einstellungen."""
        return {
            'verify': self.get_bool('PROGRAMMER', 'verify_after_program', True),
            'erase': self.get_bool('PROGRAMMER', 'erase_before_program', False),
            'backup': self.get_bool('PROGRAMMER', 'backup_before_program', True),
            'lock': self.get_bool('PROGRAMMER', 'lock_after_program', False)
        }
    
    def set_programmer_settings(self, **kwargs):
        """Speichert Programmer-Einstellungen."""
        if 'verify' in kwargs:
            self.set('PROGRAMMER', 'verify_after_program', str(kwargs['verify']).lower())
        if 'erase' in kwargs:
            self.set('PROGRAMMER', 'erase_before_program', str(kwargs['erase']).lower())
        if 'backup' in kwargs:
            self.set('PROGRAMMER', 'backup_before_program', str(kwargs['backup']).lower())
        if 'lock' in kwargs:
            self.set('PROGRAMMER', 'lock_after_program', str(kwargs['lock']).lower())
    
    # ═════════════════════════════════════════════════════
    # BOOTLOADER SETTINGS
    # ═══════════════════════════════════════���═════════════
    
    def get_bootloader_settings(self) -> dict:
        """Holt alle Bootloader-Einstellungen."""
        return {
            'type': self.get('BOOTLOADER', 'default_type', 'sam-ba'),
            'verify': self.get_bool('BOOTLOADER', 'verify_after_program', True),
            'lock': self.get_bool('BOOTLOADER', 'lock_after_program', False),
            'backup': self.get_bool('BOOTLOADER', 'backup_before_program', True)
        }
    
    def set_bootloader_settings(self, **kwargs):
        """Speichert Bootloader-Einstellungen."""
        if 'type' in kwargs:
            self.set('BOOTLOADER', 'default_type', kwargs['type'])
        if 'verify' in kwargs:
            self.set('BOOTLOADER', 'verify_after_program', str(kwargs['verify']).lower())
        if 'lock' in kwargs:
            self.set('BOOTLOADER', 'lock_after_program', str(kwargs['lock']).lower())
        if 'backup' in kwargs:
            self.set('BOOTLOADER', 'backup_before_program', str(kwargs['backup']).lower())
    
    # ═════════════════════════════════════════════════════
    # PATHS SETTINGS
    # ═════════════════════════════════════════════════════
    
    def get_firmware_dir(self) -> str:
        """Holt Firmware-Verzeichnis."""
        return self.get('PATHS', 'firmware_dir', './firmware')
    
    def set_firmware_dir(self, path: str):
        """Speichert Firmware-Verzeichnis."""
        self.set('PATHS', 'firmware_dir', path)
    
    def get_backup_dir(self) -> str:
        """Holt Backup-Verzeichnis."""
        return self.get('PATHS', 'backup_dir', './backups')
    
    def set_backup_dir(self, path: str):
        """Speichert Backup-Verzeichnis."""
        self.set('PATHS', 'backup_dir', path)
    
    def get_export_dir(self) -> str:
        """Holt Export-Verzeichnis."""
        return self.get('PATHS', 'export_dir', './export')
    
    def set_export_dir(self, path: str):
        """Speichert Export-Verzeichnis."""
        self.set('PATHS', 'export_dir', path)
    
    # ═════════════════════════════════════════════════════
    # LOGGING SETTINGS
    # ═══���═════════════════════════════════════════════════
    
    def get_log_level(self) -> str:
        """Holt Log-Level."""
        return self.get('LOGGING', 'log_level', 'info')
    
    def set_log_level(self, level: str):
        """Speichert Log-Level."""
        self.set('LOGGING', 'log_level', level)
    
    def get_log_file(self) -> str:
        """Holt Log-Datei Pfad."""
        return self.get('LOGGING', 'log_file', './logs/proggui.log')
    
    # ═════════════════════════════════════════════════════
    # HELPER METHODS
    # ═════════════════════════════════════════════════════
    
    def get(self, section: str, key: str, default: str = None) -> str:
        """Holt einen String-Wert."""
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default
    
    def get_int(self, section: str, key: str, default: int = 0) -> int:
        """Holt einen Integer-Wert."""
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return default
    
    def get_bool(self, section: str, key: str, default: bool = False) -> bool:
        """Holt einen Boolean-Wert."""
        try:
            return self.config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return default
    
    def get_float(self, section: str, key: str, default: float = 0.0) -> float:
        """Holt einen Float-Wert."""
        try:
            return self.config.getfloat(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return default
    
    def set(self, section: str, key: str, value: str):
        """Speichert einen Wert."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
    
    def save(self):
        """Speichert Konfiguration in Datei."""
        try:
            with open(self.config_path, 'w') as f:
                self.config.write(f)
            print(f"[CONFIG] Konfiguration gespeichert")
        except Exception as e:
            print(f"[ERROR] Fehler beim Speichern der Konfiguration: {e}")
    
    def reset_to_defaults(self):
        """Setzt Konfiguration auf Standard zurück."""
        self.config.clear()
        self._create_default_config()
        self.save()
        print("[CONFIG] Konfiguration zurückgesetzt")
    
    def export_config(self, file_path: str) -> bool:
        """Exportiert Konfiguration."""
        try:
            with open(file_path, 'w') as f:
                self.config.write(f)
            print(f"[CONFIG] Konfiguration exportiert: {file_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Fehler beim Exportieren: {e}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """Importiert Konfiguration."""
        try:
            self.config.read(file_path)
            self.save()
            print(f"[CONFIG] Konfiguration importiert: {file_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Fehler beim Importieren: {e}")
            return False


# Global instance
_config_instance = None


def get_config() -> ConfigManager:
    """Holt die globale Config-Instanz."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance