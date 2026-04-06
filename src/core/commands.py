# -*- coding: utf-8 -*-
# src/core/commands.py
"""
Command Builder für atprogram Befehle
- Erstellt sichere, validierte Befehle
- Verhindert Command Injection
- Lesbar und wartbar
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Command:
    """Repräsentiert einen atprogram-Befehl."""
    
    base_tool: str  # z.B. "atprogram.exe"
    action: str     # z.B. "chiperase", "write", "program"
    args: Dict[str, Any] = field(default_factory=dict)
    flags: List[str] = field(default_factory=list)
    
    def build(self) -> List[str]:
        """
        Erstellt den Befehl als Liste von Strings.
    
        atprogram erwartet: -t (nicht --t), -i (nicht --i), etc.
    
        Returns:
            List[str]: Der vollständige Befehl
        """
        cmd = [self.base_tool, self.action]
    
        # Argumente hinzufügen (-key value, nicht --key!)
        for key, value in self.args.items():
            if value is not None:
                cmd.extend([f"-{key}", str(value)])  # ← WICHTIG: Nur EIN Minus!
    
        # Flags hinzufügen (ohne Wert)
        cmd.extend(self.flags)
    
        return cmd
    
    def __repr__(self) -> str:
        return " ".join(self.build())


class CommandBuilder:
    """Builder für atprogram-Befehle mit Device-Parametern."""
    
    def __init__(self, atprogram_path: str, device: str, 
                 interface: str, programmer: str):
        """
        Initialisiert den CommandBuilder.
        
        Args:
            atprogram_path: Pfad zu atprogram.exe
            device: Device Name (z.B. "at32uc3a1512")
            interface: Interface (z.B. "jtag")
            programmer: Programmer (z.B. "atmelice")
        """
        self.atprogram_path = atprogram_path
        self.device = device
        self.interface = interface
        self.programmer = programmer
    
    def build(self) -> List[str]:
        """
        Erstellt den Befehl als Liste von Strings.
    
        WICHTIG: atprogram erwartet die Flags VOR dem Command!
    
        Korrekt:  atprogram -t atmelice -i jtag -d at32uc3a1512 chiperase
        Falsch:   atprogram chiperase -t atmelice -i jtag -d at32uc3a1512
    
        Returns:
            List[str]: Der vollständige Befehl
        """
        cmd = [self.base_tool]
    
        # ⭐ WICHTIG: Argumente ZUERST (vor dem Command!)
        for key, value in self.args.items():
            if value is not None:
                cmd.extend([f"-{key}", str(value)])
    
        # ⭐ DANN der Command
        cmd.append(self.action)
    
        # ⭐ DANN die Flags
        cmd.extend(self.flags)
    
        return cmd
    
    def chiperase(self) -> Command:
        """Befehl: Flash komplett löschen."""
        cmd = Command(self.atprogram_path, "chiperase")
        cmd.args = self._base_args()
        return cmd
    
    def erase_user_page(self) -> Command:
        """Befehl: User Page löschen."""
        cmd = Command(self.atprogram_path, "erase")
        cmd.args = self._base_args()
        cmd.flags = ["-up"]  # User Page Flag
        return cmd
    
    def write_user_page(self, address: str, values: str) -> Command:
        """
        Befehl: User Page schreiben.
        
        Args:
            address: Hex-Adresse (z.B. "0x808001FC")
            values: Hex-Werte (z.B. "E11EFFD7")
        """
        cmd = Command(self.atprogram_path, "write")
        cmd.args = {
            **self._base_args(),
            "o": address,
            "values": values,
        }
        return cmd
    
    def write_fuse(self, address: str, values: str) -> Command:
        """
        Befehl: Fuse Bits schreiben.
        
        Args:
            address: Offset (üblicherweise "0x0")
            values: Hex-Werte
        """
        cmd = Command(self.atprogram_path, "write")
        cmd.args = {
            **self._base_args(),
            "o": address,
            "values": values,
        }
        cmd.flags = ["-fs"]  # Fuse Bits Flag
        return cmd
    
    def program_flash(self, binary_file: str, address: str = "0x80000000",
                     verify: bool = True) -> Command:
        """
        Befehl: Flash-Memory programmieren.
        
        Args:
            binary_file: Pfad zur .bin Datei
            address: Start-Adresse (default: 0x80000000)
            verify: Verifizierung nach dem Schreiben
        """
        cmd = Command(self.atprogram_path, "program")
        cmd.args = {
            **self._base_args(),
            "o": address,
            "f": binary_file,
        }
        if verify:
            cmd.flags = ["--verify"]
        return cmd

    def _base_args(self) -> Dict[str, str]:
        """Gibt Standard-Argumente zurück."""
        return {
            "t": self.programmer,
            "i": self.interface,
            "d": self.device,
        }
    
    def secure(self) -> Command:
        """Befehl: Security Bit setzen."""
        cmd = Command(self.atprogram_path, "secure")
        cmd.args = self._base_args()
        return cmd


# Beispiel-Verwendung:
# builder = CommandBuilder("atprogram.exe", "at32uc3a1512", "jtag", "atmelice")
# cmd = builder.chiperase()
# print(cmd.build())  # ['atprogram.exe', 'chiperase', '-t', 'atmelice', ...]
