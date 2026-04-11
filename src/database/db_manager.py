# -*- coding: utf-8 -*-
# src/database/db_manager.py
"""
Datenbank Manager
- SQLite Datenbank für Devices
- Settings Persistierung
- CRUD Operationen
"""

import sqlite3
import json
import os
from pathlib import Path


class DatabaseManager:
    """SQLite Datenbank Manager."""
    
    def __init__(self, db_path: str = None):
        """Initialisiert den Datenbank Manager."""
        if db_path is None:
            # Erstelle Datenbank im data/ Verzeichnis
            data_dir = Path(__file__).parent.parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = data_dir / "proggui.db"
        
        self.db_path = db_path
        self.connection = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialisiert die Datenbank und erstellt Tabellen."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            cursor = self.connection.cursor()
            
            # Devices Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    type TEXT NOT NULL,
                    port TEXT NOT NULL,
                    status TEXT DEFAULT 'Disconnected',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Settings Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Programming History Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS programming_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id INTEGER NOT NULL,
                    firmware_file TEXT NOT NULL,
                    status TEXT NOT NULL,
                    duration_seconds REAL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (device_id) REFERENCES devices(id)
                )
            """)
            
            # Backups Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS backups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id INTEGER NOT NULL,
                    backup_file TEXT NOT NULL,
                    backup_type TEXT NOT NULL,
                    size_bytes INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (device_id) REFERENCES devices(id)
                )
            """)
            
            self.connection.commit()
            print(f"[DB] Datenbank initialisiert: {self.db_path}")
        
        except sqlite3.Error as e:
            print(f"[ERROR] Datenbank Fehler: {e}")
            raise
    
    # ═════════════════════════════════════════════════════
    # DEVICES
    # ═════════════════════════════════════════════════════
    
    def add_device(self, name: str, device_type: str, port: str, status: str = "Disconnected") -> int:
        """Fügt ein neues Device hinzu."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO devices (name, type, port, status)
                VALUES (?, ?, ?, ?)
            """, (name, device_type, port, status))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"[ERROR] Device '{name}' existiert bereits!")
            return None
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Hinzufügen des Devices: {e}")
            return None
    
    def get_device(self, device_id: int) -> dict:
        """Holt ein Device."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Abrufen des Devices: {e}")
            return None
    
    def get_all_devices(self) -> list:
        """Holt alle Devices."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM devices ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Abrufen der Devices: {e}")
            return []
    
    def update_device(self, device_id: int, **kwargs) -> bool:
        """Aktualisiert ein Device."""
        try:
            allowed_fields = {'name', 'type', 'port', 'status'}
            fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            if not fields:
                return False
            
            fields['updated_at'] = 'CURRENT_TIMESTAMP'
            
            set_clause = ", ".join([f"{k} = ?" if k != 'updated_at' else f"{k} = {k}" 
                                   for k in fields.keys()])
            values = [v for k, v in fields.items() if k != 'updated_at']
            values.append(device_id)
            
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE devices SET {set_clause} WHERE id = ?", values)
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Aktualisieren des Devices: {e}")
            return False
    
    def delete_device(self, device_id: int) -> bool:
        """Löscht ein Device."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM devices WHERE id = ?", (device_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Löschen des Devices: {e}")
            return False
    
    # ═════════════════════════════════════════════════════
    # SETTINGS
    # ═════════════════════════════════════════════════════
    
    def set_setting(self, key: str, value) -> bool:
        """Speichert eine Einstellung."""
        try:
            if not isinstance(value, str):
                value = json.dumps(value)
            
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO settings (key, value)
                VALUES (?, ?)
            """, (key, value))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Speichern der Einstellung: {e}")
            return False
    
    def get_setting(self, key: str, default=None):
        """Holt eine Einstellung."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            
            if row:
                try:
                    return json.loads(row['value'])
                except json.JSONDecodeError:
                    return row['value']
            return default
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Abrufen der Einstellung: {e}")
            return default
    
    def get_all_settings(self) -> dict:
        """Holt alle Einstellungen."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT key, value FROM settings")
            rows = cursor.fetchall()
            
            result = {}
            for row in rows:
                try:
                    result[row['key']] = json.loads(row['value'])
                except json.JSONDecodeError:
                    result[row['key']] = row['value']
            return result
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Abrufen der Einstellungen: {e}")
            return {}
    
    # ═════════════════════════════════════════════════════
    # PROGRAMMING HISTORY
    # ═════════════════════════════════════════════════════
    
    def add_programming_record(self, device_id: int, firmware_file: str, 
                               status: str, duration_seconds: float = None, 
                               notes: str = None) -> int:
        """Fügt einen Programmier-Eintrag hinzu."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO programming_history 
                (device_id, firmware_file, status, duration_seconds, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (device_id, firmware_file, status, duration_seconds, notes))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Hinzufügen des Programmier-Eintrags: {e}")
            return None
    
    def get_programming_history(self, device_id: int = None, limit: int = 50) -> list:
        """Holt die Programmier-Historie."""
        try:
            cursor = self.connection.cursor()
            
            if device_id:
                cursor.execute("""
                    SELECT * FROM programming_history 
                    WHERE device_id = ? 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (device_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM programming_history 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Abrufen der Programmier-Historie: {e}")
            return []
    
    # ═════════════════════════════════════════════════════
    # BACKUPS
    # ═════════════════════════════════════════════════════
    
    def add_backup_record(self, device_id: int, backup_file: str, 
                         backup_type: str, size_bytes: int = None) -> int:
        """Fügt einen Backup-Eintrag hinzu."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO backups 
                (device_id, backup_file, backup_type, size_bytes)
                VALUES (?, ?, ?, ?)
            """, (device_id, backup_file, backup_type, size_bytes))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Hinzufügen des Backup-Eintrags: {e}")
            return None
    
    def get_backups(self, device_id: int = None, limit: int = 50) -> list:
        """Holt die Backups."""
        try:
            cursor = self.connection.cursor()
            
            if device_id:
                cursor.execute("""
                    SELECT * FROM backups 
                    WHERE device_id = ? 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (device_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM backups 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Abrufen der Backups: {e}")
            return []
    
    # ══════════════════════════════════════���══════════════
    # DATABASE MANAGEMENT
    # ═════════════════════════════════════════════════════
    
    def close(self):
        """Schließt die Datenbankverbindung."""
        if self.connection:
            self.connection.close()
            print("[DB] Datenbankverbindung geschlossen")
    
    def reset_database(self):
        """Setzt die Datenbank zurück (VORSICHT!)."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS backups")
            cursor.execute("DROP TABLE IF EXISTS programming_history")
            cursor.execute("DROP TABLE IF EXISTS settings")
            cursor.execute("DROP TABLE IF EXISTS devices")
            self.connection.commit()
            print("[DB] Datenbank zurückgesetzt")
            self._initialize_database()
        except sqlite3.Error as e:
            print(f"[ERROR] Fehler beim Zurücksetzen der Datenbank: {e}")
    
    def export_devices(self, file_path: str) -> bool:
        """Exportiert Devices zu JSON."""
        try:
            devices = self.get_all_devices()
            with open(file_path, 'w') as f:
                json.dump(devices, f, indent=2)
            print(f"[DB] Devices exportiert: {file_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Fehler beim Exportieren: {e}")
            return False
    
    def import_devices(self, file_path: str) -> bool:
        """Importiert Devices aus JSON."""
        try:
            with open(file_path, 'r') as f:
                devices = json.load(f)
            
            for device in devices:
                self.add_device(
                    device['name'],
                    device['type'],
                    device['port'],
                    device.get('status', 'Disconnected')
                )
            print(f"[DB] {len(devices)} Devices importiert")
            return True
        except Exception as e:
            print(f"[ERROR] Fehler beim Importieren: {e}")
            return False


# Global instance
_db_instance = None


def get_database() -> DatabaseManager:
    """Holt die globale Datenbankinstanz."""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance


def close_database():
    """Schließt die globale Datenbankinstanz."""
    global _db_instance
    if _db_instance:
        _db_instance.close()
        _db_instance = None