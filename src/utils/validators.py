# -*- coding: utf-8 -*-
# src/utils/validators.py
"""
Input-Validierung für ProgGUI
- Validiert Hex-Werte
- Validiert Dateipfade
- Validiert Tool-Pfade
"""

import os
from pathlib import Path
from typing import Tuple, Optional


class ValidationError(Exception):
    """Exception für Validierungs-Fehler."""
    pass


class Validator:
    """Zentrale Validierungs-Klasse."""
    
    @staticmethod
    def is_valid_hex(value: str, expected_length: Optional[int] = None) -> bool:
        """
        Prüft ob ein String ein gültiger Hex-Wert ist.
        
        Args:
            value: Zu prüfender String (z.B. "E11EFFD7")
            expected_length: Optional gewünschte Länge
        
        Returns:
            bool: True wenn gültig
        
        Raises:
            ValidationError: Bei ungültigen Werten
        """
        if not value:
            raise ValidationError("Hex-Wert darf nicht leer sein")
        
        # Entferne führendes "0x" falls vorhanden
        clean_value = value.replace("0x", "").replace("0X", "")
        
        # Prüfe ob nur Hex-Zeichen
        try:
            int(clean_value, 16)
        except ValueError:
            raise ValidationError(
                f"'{value}' ist kein gültiger Hex-Wert. "
                f"Verwende nur 0-9 und A-F"
            )
        
        # Prüfe Länge wenn gewünscht
        if expected_length and len(clean_value) != expected_length:
            raise ValidationError(
                f"Hex-Wert muss {expected_length} Zeichen lang sein, "
                f"ist aber {len(clean_value)}"
            )
        
        return True
    
    @staticmethod
    def validate_hex_address(address: str) -> str:
        """
        Validiert und normalisiert eine Hex-Adresse.
        
        Args:
            address: Adresse (z.B. "0x808001FC" oder "808001FC")
        
        Returns:
            str: Normalisierte Adresse mit "0x" Prefix
        
        Raises:
            ValidationError: Bei ungültiger Adresse
        """
        if not address:
            raise ValidationError("Adresse darf nicht leer sein")
        
        # Entferne Spaces
        address = address.strip()
        
        # Prüfe ob Hex gültig
        Validator.is_valid_hex(address)
        
        # Normalisiere zu "0x..." Format
        if not address.startswith("0x"):
            address = "0x" + address
        
        return address
    
    @staticmethod
    def is_valid_file(file_path: str, must_exist: bool = True) -> bool:
        """
        Validiert einen Dateipfad.
        
        Args:
            file_path: Zu prüfender Pfad
            must_exist: Muss die Datei existieren?
        
        Returns:
            bool: True wenn gültig
        
        Raises:
            ValidationError: Bei ungültiger Datei
        """
        if not file_path:
            raise ValidationError("Dateipfad darf nicht leer sein")
        
        path = Path(file_path)
        
        if must_exist and not path.exists():
            raise ValidationError(f"Datei nicht gefunden: {file_path}")
        
        if must_exist and not path.is_file():
            raise ValidationError(f"Das ist keine Datei: {file_path}")
        
        return True
    
    @staticmethod
    def is_valid_hex_file(file_path: str) -> bool:
        """
        Validiert eine HEX-Datei.
        
        Args:
            file_path: Pfad zur .hex Datei
        
        Returns:
            bool: True wenn gültig
        
        Raises:
            ValidationError: Bei ungültiger Datei
        """
        Validator.is_valid_file(file_path, must_exist=True)
        
        if not file_path.endswith(".hex"):
            raise ValidationError(
                f"Datei muss .hex Endung haben, ist aber: {file_path}"
            )
        
        # Optional: Prüfe ob Datei Hex-Inhalt hat
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if not first_line.startswith(":"):
                    raise ValidationError(
                        "Datei sieht nicht nach Intel HEX Format aus "
                        "(muss mit ':' starten)"
                    )
        except Exception as e:
            raise ValidationError(f"Fehler beim Lesen der Datei: {e}")
        
        return True
    
    @staticmethod
    def is_valid_tool_path(tool_path: str, tool_name: str = "") -> bool:
        """
        Validiert einen Tool-Pfad (atprogram.exe, etc).
        
        Args:
            tool_path: Pfad zum Tool
            tool_name: Name des Tools (für Error-Message)
        
        Returns:
            bool: True wenn gültig
        
        Raises:
            ValidationError: Bei ungültiger Pfad
        """
        Validator.is_valid_file(tool_path, must_exist=True)
        
        if not tool_path.endswith(".exe"):
            name = f"'{tool_name}'" if tool_name else "Tool"
            raise ValidationError(f"{name} muss .exe Datei sein")
        
        return True
    
    @staticmethod
    def validate_all_settings(settings_dict: dict) -> Tuple[bool, list]:
        """
        Validiert alle Einstellungen auf einmal.
        
        Args:
            settings_dict: Dictionary mit allen Einstellungen
        
        Returns:
            Tuple[bool, list]: (ist_valide, list_mit_errors)
        """
        errors = []
        
        # Tool-Pfade prüfen
        tools = {
            "atprogram_path": "atprogram.exe",
            "atbackend_path": "atbackend.exe",
            "objcopy_path": "avr32-objcopy.exe",
        }
        
        for key, tool_name in tools.items():
            if key in settings_dict:
                try:
                    Validator.is_valid_tool_path(
                        settings_dict[key],
                        tool_name
                    )
                except ValidationError as e:
                    errors.append(str(e))
        
        # HEX-Datei prüfen (nur wenn gesetzt)
        if settings_dict.get("hex_file"):
            try:
                Validator.is_valid_hex_file(settings_dict["hex_file"])
            except ValidationError as e:
                errors.append(str(e))
        
        # Hex-Werte prüfen
        hex_values = ["val_1fc", "val_1f8", "fuse_val"]
        for key in hex_values:
            if key in settings_dict:
                try:
                    Validator.is_valid_hex(settings_dict[key])
                except ValidationError as e:
                    errors.append(f"{key}: {str(e)}")
        
        return len(errors) == 0, errors
