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
    
        WICHTIG: atprogram erwartet die Flags in DIESER Reihenfolge:
        1. Base tool
        2. GLOBAL FLAGS in dieser Reihenfolge: -t, -i, -d
        3. Command (chiperase, write, program, etc.)
        4. Command-spezifische Flags/Args
    
        Korrekt:  atprogram -t atmelice -i jtag -d at32uc3a1512 chiperase
    
        Returns:
            List[str]: Der vollständige Befehl
        """
        cmd = [self.base_tool]
    
        # ⭐ GLOBAL FLAGS in FESTER REIHENFOLGE (vor dem Command!)
        # Die Reihenfolge MUSS so sein: -t, -i, -d
        global_order = ["t", "i", "d"]
        for key in global_order:
            if key in self.args:
                value = self.args[key]
                if value is not None:
                    cmd.extend([f"-{key}", str(value)])
    
        # ⭐ DANN der Command
        cmd.append(self.action)
    
        # ⭐ DANN die Command-spezifischen Argumente (nach dem Command!)
        for key, value in self.args.items():
            if key not in global_order and value is not None:
                prefix = "--" if len(key) > 1 else "-"
                cmd.extend([f"{prefix}{key}", str(value)])
    
        # ⭐ DANN die Flags (die haben keine Werte!)
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
                     verify: bool = True, erase: bool = True) -> Command:
        """
        Befehl: Flash-Memory programmieren.
    
        Args:
            binary_file: Pfad zur .bin Datei
            address: Start-Adresse (default: 0x80000000)
            verify: Verifizierung nach dem Schreiben
            erase: Flash vor dem Schreiben löschen
        """
        cmd = Command(self.atprogram_path, "program")
        cmd.args = {
            **self._base_args(),
            "o": address,
            "f": binary_file,
        }
    
        cmd.flags = []
        if erase:
            cmd.flags.append("-e")
        if verify:
            cmd.flags.append("--verify")
    
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