# -*- coding: utf-8 -*-
# src/utils/logging.py
"""
Logging-System für ProgGUI
- Strukturierte Logs mit Tags
- Farbcodierte Ausgabe
- Log-Speicherung
"""

from enum import Enum
from typing import Callable, Optional
from datetime import datetime


class LogLevel(Enum):
    """Log-Level Enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class LogEntry:
    """Einzelner Log-Eintrag."""
    
    def __init__(self, level: LogLevel, message: str, tag: str = ""):
        self.timestamp = datetime.now()
        self.level = level
        self.message = message
        self.tag = tag
    
    def __repr__(self) -> str:
        return (f"[{self.timestamp.strftime('%H:%M:%S')}] "
                f"[{self.level.value}] {self.message}")


class Logger:
    """Zentrale Logging-Klasse."""
    
    def __init__(self):
        """Initialisiert den Logger."""
        self.entries: list[LogEntry] = []
        self.callbacks: list[Callable[[LogEntry], None]] = []
    
    def add_callback(self, callback: Callable[[LogEntry], None]):
        """
        Registriert einen Callback für jeden Log-Eintrag.
        
        Wird verwendet um Logs in die GUI zu schreiben.
        
        Args:
            callback: Funktion mit LogEntry Parameter
        """
        self.callbacks.append(callback)
    
    def _emit(self, entry: LogEntry):
        """Sendet einen Log-Eintrag an alle Callbacks."""
        self.entries.append(entry)
        for callback in self.callbacks:
            try:
                callback(entry)
            except Exception as e:
                print(f"[ERROR] Callback fehlgeschlagen: {e}")
    
    def debug(self, message: str, tag: str = ""):
        """Debug-Nachricht."""
        self._emit(LogEntry(LogLevel.DEBUG, message, tag))
    
    def info(self, message: str, tag: str = ""):
        """Info-Nachricht."""
        self._emit(LogEntry(LogLevel.INFO, message, tag))
    
    def success(self, message: str, tag: str = "ok"):
        """Erfolgs-Nachricht."""
        self._emit(LogEntry(LogLevel.SUCCESS, message, tag))
    
    def warning(self, message: str, tag: str = "warn"):
        """Warn-Nachricht."""
        self._emit(LogEntry(LogLevel.WARNING, message, tag))
    
    def error(self, message: str, tag: str = "err"):
        """Error-Nachricht."""
        self._emit(LogEntry(LogLevel.ERROR, message, tag))
    
    def header(self, message: str):
        """Header-Nachricht (für Sektionen)."""
        self._emit(LogEntry(LogLevel.INFO, "═" * 62, "head"))
        self._emit(LogEntry(LogLevel.INFO, f"   {message}", "head"))
        self._emit(LogEntry(LogLevel.INFO, "═" * 62, "head"))
    
    def separator(self):
        """Trennlinie."""
        self._emit(LogEntry(LogLevel.INFO, "─" * 62, "dim"))
    
    def get_all_text(self) -> str:
        """
        Gibt alle Logs als Text zurück.
        
        Returns:
            str: Alle Log-Einträge
        """
        return "\n".join(str(entry) for entry in self.entries)
    
    def clear(self):
        """Löscht alle Log-Einträge."""
        self.entries.clear()
    
    def __repr__(self) -> str:
        return f"Logger(entries={len(self.entries)})"


# Globale Logger-Instanz
logger = Logger()
