# -*- coding: utf-8 -*-
# src/config/settings.py
"""
Settings Management für ProgGUI
- Lädt/speichert Einstellungen von/zu settings.json
- Verwaltet Pfade, Device-Konfiguration, Programmier-Optionen
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

from .constants import DEFAULT_SETTINGS


class SettingsManager:
    """
    Zentrale Verwaltung aller Einstellungen.
    
    Speichert Einstellungen persistent in settings.json
    neben der .exe oder .py Datei.
    """

    def __init__(self):
        """Initialisiert den SettingsManager und lädt Einstellungen."""
        self.settings_path = self._get_settings_path()
        self.data = self.load()

    @staticmethod
    def _get_settings_path() -> Path:
        """
        Gibt den Pfad zur settings.json zurück.
        
        - Wenn PyInstaller .exe: neben der .exe
        - Sonst: neben main.py
        
        Returns:
            Path: Pfad zu settings.json
        """
        if getattr(sys, "frozen", False):
            # PyInstaller .exe
            base_dir = Path(sys.executable).parent
        else:
            # Python-Datei
            base_dir = Path(__file__).parent.parent.parent  # Gehe zu ProgGUI/ Root

        return base_dir / "settings.json"

    def load(self) -> Dict[str, Any]:
        """
        Lädt Einstellungen aus settings.json.
        
        Falls Datei nicht existiert oder fehlende Keys:
        - Verwendet DEFAULT_SETTINGS als Fallback
        
        Returns:
            Dict: Alle Einstellungen
        """
        if self.settings_path.exists():
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Fehlende Keys mit Defaults auffüllen
                for key, value in DEFAULT_SETTINGS.items():
                    if key not in data:
                        data[key] = value
                
                return data
            
            except json.JSONDecodeError:
                print(f"[WARN] settings.json konnte nicht geparst werden")
                return DEFAULT_SETTINGS.copy()
            except Exception as e:
                print(f"[WARN] Fehler beim Laden von settings.json: {e}")
                return DEFAULT_SETTINGS.copy()
        
        return DEFAULT_SETTINGS.copy()

    def save(self) -> bool:
        """
        Speichert aktuelle Einstellungen in settings.json.
        
        Returns:
            bool: True wenn erfolgreich, False bei Fehler
        """
        try:
            # Stelle sicher, dass der Ordner existiert
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"[ERROR] Einstellungen konnten nicht gespeichert werden: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        Holt einen Einstellungs-Wert.
        
        Args:
            key: Schlüssel (z.B. "hex_file")
            default: Fallback-Wert wenn nicht gefunden
        
        Returns:
            Any: Der Wert oder default
        """
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Setzt einen Einstellungs-Wert und speichert sofort.
        
        Args:
            key: Schlüssel (z.B. "hex_file")
            value: Neuer Wert
        """
        self.data[key] = value
        self.save()

    def update(self, updates: Dict[str, Any]) -> None:
        """
        Aktualisiert mehrere Einstellungen auf einmal.
        
        Args:
            updates: Dictionary mit Key-Value Paaren
        """
        self.data.update(updates)
        self.save()

    def reset_to_defaults(self) -> None:
        """Setzt alle Einstellungen auf Defaults zurück."""
        self.data = DEFAULT_SETTINGS.copy()
        self.save()

    def __repr__(self) -> str:
        """String-Repräsentation für Debugging."""
        return f"SettingsManager(path={self.settings_path}, keys={list(self.data.keys())})"


# Globale Instanz (wird in main.py verwendet)
settings = SettingsManager()
