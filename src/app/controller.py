# -*- coding: utf-8 -*-
# src/app/controller.py
"""
Application Controller - Herzstück der Programmier-Logik
- Koordiniert alle Schritte
- Verwaltet den Programmier-Prozess
- Trennt UI von Business-Logik
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional

from ..config.constants import (
    DEVICE, INTERFACE, PROGRAMMER, PROGRAMMING_STEPS
)
from ..config.settings import settings
from ..core.commands import CommandBuilder
from ..core.device import DEFAULT_DEVICE
from ..utils.validators import Validator, ValidationError
from ..utils.logging import logger, LogEntry


class ProgrammerController:
    """
    Hauptcontroller für den Programmier-Prozess.
    
    Orchestriert:
    - Validierung von Einstellungen
    - Ausführung von Programmier-Schritten
    - Error-Handling
    - Progress-Tracking
    """
    
    def __init__(self):
        """Initialisiert den Controller."""
        self.abort_requested = False
        self.current_step = 0
        self.total_steps = 0
        
        # Callbacks für UI-Updates
        self.on_progress: Optional[Callable[[float], None]] = None
        self.on_status: Optional[Callable[[str], None]] = None
        self.on_log: Optional[Callable[[LogEntry], None]] = None
    
    def set_progress_callback(self, callback: Callable[[float], None]):
        """Registriert Callback für Progress-Updates."""
        self.on_progress = callback
        logger.add_callback(self.on_log or (lambda x: None))
    
    def set_status_callback(self, callback: Callable[[str], None]):
        """Registriert Callback für Status-Updates."""
        self.on_status = callback
    
    def set_log_callback(self, callback: Callable[[LogEntry], None]):
        """Registriert Callback für Log-Updates."""
        self.on_log = callback
        logger.add_callback(callback)
    
    def _update_progress(self, step: int, total: int):
        """Aktualisiert Progress."""
        if self.on_progress:
            progress = (step / max(total, 1)) * 100
            self.on_progress(progress)
    
    def _update_status(self, message: str):
        """Aktualisiert Status-Text."""
        if self.on_status:
            self.on_status(message)
    
    def validate_settings(self) -> tuple[bool, list[str]]:
        """
        Validiert alle aktuellen Einstellungen.
        
        Returns:
            tuple: (is_valid, error_list)
        """
        logger.separator()
        logger.info("Validiere Einstellungen...")
        logger.separator()
        
        is_valid, errors = Validator.validate_all_settings(settings.data)
        
        if is_valid:
            logger.success("✅ Alle Einstellungen OK")
        else:
            for error in errors:
                logger.error(f"❌ {error}")
        
        return is_valid, errors
    
    def prepare(self) -> bool:
        """
        Bereitet die Programmierung vor.
        
        Returns:
            bool: True wenn erfolgreich vorbereitet
        """
        logger.header("VORBEREITUNG")
        
        # Validierung
        is_valid, errors = self.validate_settings()
        if not is_valid:
            return False
        
        # Berechne Anzahl Schritte
        self.total_steps = self._count_active_steps()
        
        logger.info(f"📋 {self.total_steps} Schritte werden ausgeführt")
        logger.separator()
        
        return True
    
    def _count_active_steps(self) -> int:
        """Zählt wie viele Schritte aktiv sind."""
        count = 0
        
        # Normale Schritte
        for step in PROGRAMMING_STEPS:
            if settings.get(step["key"], False):
                count += 1
        
        # Zusätzliche Unter-Schritte
        if settings.get("user_write", False):
            count += 1  # zwei Unter-Schritte (1FC und 1F8)
        
        if settings.get("flash_write", False):
            count += 1  # objcopy Konvertierung
        
        return count
    
    def request_abort(self):
        """Fordert Abbruch an."""
        self.abort_requested = True
        logger.warning("⚠  Abbruch angefordert")
    
    def run(self) -> bool:
        """
        Startet den kompletten Programmier-Prozess.
        
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if not self.prepare():
            return False
        
        self._update_status("⏳ Programmierung läuft...")
        
        try:
            # Initialisiere Command Builder
            builder = CommandBuilder(
                atprogram_path=settings.get("atprogram_path"),
                device=DEVICE,
                interface=INTERFACE,
                programmer=PROGRAMMER
            )
            
            step_num = 0
            
            # ════════════════════════════════════════════════════════
            # 1. Chip Erase
            # ════════════════════════════════════════════════════════
            if self.abort_requested:
                return False
            
            if settings.get("chip_erase", False):
                step_num += 1
                logger.separator()
                logger.info(f"▶ Schritt {step_num}: Flash löschen (ChipErase)")
                self._update_status("🗑  Flash wird gelöscht...")
                
                cmd = builder.chiperase()
                if not self._run_command(cmd, "ChipErase"):
                    return False
                
                logger.success("✅ Flash gelöscht")
                self._update_progress(step_num, self.total_steps)
            
            # ════════════════════════════════════════════════════════
            # 2. User Page Erase
            # ════════════════════════════════════════════════════════
            if self.abort_requested:
                return False
            
            if settings.get("user_erase", False):
                step_num += 1
                logger.separator()
                logger.info(f"▶ Schritt {step_num}: User Page löschen")
                self._update_status("🗑  User Page wird gelöscht...")
                
                cmd = builder.erase_user_page()
                if not self._run_command(cmd, "User Page Erase"):
                    return False
                
                logger.success("✅ User Page gelöscht")
                self._update_progress(step_num, self.total_steps)
            
            # ════════════════════════════════════════════════════════
            # 3. User Page Write
            # ════════════════════════════════════════════════════════
            if self.abort_requested:
                return False
            
            if settings.get("user_write", False):
                # 3a. Write 0x808001FC
                step_num += 1
                logger.separator()
                logger.info(f"▶ Schritt {step_num}: User Page → 0x808001FC")
                self._update_status("✍  User Page 0x808001FC wird geschrieben...")
                
                cmd = builder.write_user_page(
                    address="0x808001FC",
                    values=settings.get("val_1fc", "")
                )
                if not self._run_command(cmd, "User Page Write 1FC"):
                    return False
                
                logger.success("✅ 0x808001FC geschrieben")
                self._update_progress(step_num, self.total_steps)
                
                # 3b. Write 0x808001F8
                if not self.abort_requested:
                    step_num += 1
                    logger.separator()
                    logger.info(f"▶ Schritt {step_num}: User Page → 0x808001F8")
                    self._update_status("✍  User Page 0x808001F8 wird geschrieben...")
                    
                    cmd = builder.write_user_page(
                        address="0x808001F8",
                        values=settings.get("val_1f8", "")
                    )
                    if not self._run_command(cmd, "User Page Write 1F8"):
                        return False
                    
                    logger.success("✅ 0x808001F8 geschrieben")
                    self._update_progress(step_num, self.total_steps)
            
            # ════════════════════════════════════════════════════════
            # 4. Flash Write (Bootloader)
            # ════════════════════════════════════════════════════════
            if self.abort_requested:
                return False
            
            if settings.get("flash_write", False):
                hex_file = settings.get("hex_file", "")
                
                if not hex_file:
                    logger.error("❌ Keine HEX-Datei angegeben!")
                    return False
                
                # 4a. HEX → BIN mit objcopy
                step_num += 1
                logger.separator()
                logger.info(f"▶ Schritt {step_num}: HEX → BIN konvertieren")
                self._update_status("⚙  HEX wird zu BIN konvertiert...")
                
                bin_file = self._convert_hex_to_bin(hex_file)
                if not bin_file:
                    return False
                
                logger.success(f"✅ BIN konvertiert: {bin_file}")
                self._update_progress(step_num, self.total_steps)
                
                # 4b. Flash programmieren
                if not self.abort_requested:
                    step_num += 1
                    logger.separator()
                    logger.info(f"▶ Schritt {step_num}: Bootloader schreiben")
                    self._update_status("⬆  Bootloader wird geschrieben...")
                    
                    cmd = builder.program_flash(
                        binary_file=bin_file,
                        address="0x80000000",
                        verify=True
                    )
                    if not self._run_command(cmd, "Flash Program"):
                        return False
                    
                    logger.success("✅ Bootloader geschrieben & verifiziert")
                    self._update_progress(step_num, self.total_steps)
            
            # ════════════════════════════════════════════════════════
            # 5. Fuse Bits
            # ════════════════════════════════════════════════════════
            if self.abort_requested:
                return False
            
            if settings.get("fuse_write", False):
                step_num += 1
                logger.separator()
                logger.info(f"▶ Schritt {step_num}: Fuse Bits setzen")
                self._update_status("🔩  Fuse Bits werden gesetzt...")
                
                cmd = builder.write_fuse(
                    address="0x0",
                    values=settings.get("fuse_val", "")
                )
                if not self._run_command(cmd, "Fuse Write"):
                    return False
                
                logger.success("✅ Fuse Bits gesetzt")
                self._update_progress(step_num, self.total_steps)
            
            # ════════════════════════════════════════════════════════
            # 6. Security Bit
            # ════════════════════════════════════════════════════════
            if self.abort_requested:
                return False
            
            if settings.get("secure", False):
                step_num += 1
                logger.separator()
                logger.info(f"▶ Schritt {step_num}: Security Bit setzen")
                self._update_status("🔒  Security Bit wird gesetzt...")
                
                cmd = builder.secure()
                if not self._run_command(cmd, "Secure"):
                    return False
                
                logger.success("✅ Security Bit gesetzt")
                self._update_progress(step_num, self.total_steps)
            
            # ════════════════════════════════════════════════════════
            # SUCCESS!
            # ════════════════════════════════════════════════════════
            logger.header("✅ PROGRAMMIERUNG ERFOLGREICH!")
            self._update_status("✅ Fertig - Programmierung erfolgreich!")
            self._update_progress(self.total_steps, self.total_steps)
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Unerwarteter Fehler: {e}")
            return False
    
    def _run_command(self, cmd, step_name: str) -> bool:
        """
        Führt einen atprogram-Befehl aus.
        
        Args:
            cmd: Command-Objekt
            step_name: Name des Schritts (für Logging)
        
        Returns:
            bool: True bei Erfolg
        """
        if self.abort_requested:
            return False
        
        try:
            cmd_list = cmd.build()
            logger.info(f"   $ {' '.join(cmd_list[:5])}{'...' if len(cmd_list) > 5 else ''}", 
                       tag="dim")
            
            proc = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=(subprocess.CREATE_NO_WINDOW
                              if sys.platform == "win32" else 0)
            )
            
            for line in proc.stdout:
                line = line.rstrip()
                if not line:
                    continue
                
                # Farbcodierung basierend auf Inhalt
                low = line.lower()
                if "[error]" in low or "error" in low:
                    logger.error(f"   {line}")
                elif "[warning]" in low or "warning" in low:
                    logger.warning(f"   {line}")
                elif any(w in low for w in ("success", "completed", "ok", "done")):
                    logger.success(f"   {line}")
                else:
                    logger.info(f"   {line}", tag="normal")
            
            proc.wait()
            logger.info(f"   → Exit Code: {proc.returncode}", tag="dim")
            
            if proc.returncode == 0:
                return True
            else:
                logger.error(f"❌ {step_name} FEHLER (Code {proc.returncode})")
                return False
        
        except FileNotFoundError:
            logger.error(f"❌ Tool nicht gefunden! Pfad: {cmd.base_tool}")
            return False
        except Exception as e:
            logger.error(f"❌ Fehler beim Ausführen: {e}")
            return False
    
    def _convert_hex_to_bin(self, hex_file: str) -> Optional[str]:
        """
        Konvertiert HEX-Datei zu BIN mit objcopy.
        
        Args:
            hex_file: Pfad zur .hex Datei
        
        Returns:
            str: Pfad zur erstellten .bin Datei, oder None bei Fehler
        """
        objcopy = settings.get("objcopy_path")
        
        if not os.path.isfile(objcopy):
            logger.error(f"❌ objcopy nicht gefunden: {objcopy}")
            return None
        
        bin_file = hex_file.replace(".hex", "_converted.bin")
        
        try:
            cmd = [objcopy, "-I", "ihex", "-O", "binary", hex_file, bin_file]
            
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=(subprocess.CREATE_NO_WINDOW
                              if sys.platform == "win32" else 0)
            )
            
            proc.wait()
            
            if proc.returncode == 0 and os.path.isfile(bin_file):
                return bin_file
            else:
                logger.error(f"❌ HEX-Konvertierung fehlgeschlagen")
                return None
        
        except Exception as e:
            logger.error(f"❌ Fehler bei HEX-Konvertierung: {e}")
            return None
