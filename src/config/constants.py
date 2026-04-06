# src/config/constants.py
"""
Zentrale Konstanten für ProgGUI
- Farben & Styles
- Tool-Pfade
- Device-Konfiguration
- ...
"""

# ═════════════════════════════════════════════════════════════════════════════
# 🎨 FARBEN & DESIGN (Catppuccin Theme - Mocha)
# ═════════════════════════════════════════════════════════════════════════════

BG          = "#1e1e2e"     # Haupthintergrund (dunkelgrau)
BG2         = "#2a2a3e"     # Sekundär-Hintergrund
BG3         = "#313145"     # Tertär-Hintergrund
ACCENT      = "#89b4fa"     # Blau (Hauptakzent)
ACCENT2     = "#cba6f7"     # Lila (Sekundär-Akzent)
GREEN       = "#a6e3a1"     # Grün (Success)
RED         = "#f38ba8"     # Rot (Error)
YELLOW      = "#f9e2af"     # Gelb (Warning)
TEXT        = "#cdd6f4"     # Normaltext
SUBTEXT     = "#a6adc8"     # Subtext (gedimmt)

# ════════════════════════════════���════════════════════════════════════════════
# 🔤 SCHRIFTARTEN
# ═════════════════════════════════════════════════════════════════════════════

FONT_MAIN   = ("Consolas", 10)
FONT_TITLE  = ("Consolas", 13, "bold")
FONT_STEP   = ("Consolas", 10, "bold")
FONT_MONO   = ("Consolas", 9)

# ═════════════════════════════════════════════════════════════════════════════
# 🔧 TOOL-PFADE (Windows-only)
# ═════════════════════════════════════════════════════════════════════════════

DEFAULT_ATPROGRAM = r"C:\Program Files (x86)\Atmel\Studio\7.0\atbackend\atprogram.exe"
DEFAULT_ATBACKEND = r"C:\Program Files (x86)\Atmel\Studio\7.0\atbackend\atbackend.exe"
DEFAULT_OBJCOPY   = r"C:\Program Files (x86)\Atmel\Studio\7.0\toolchain\avr32\avr32-gnu-toolchain\bin\avr32-objcopy.exe"

# ═════════════════════════════════════════════════════════════════════════════
# 🎯 DEVICE-KONFIGURATION
# ════════════��════════════════════════════════════════════════════════════════

DEVICE      = "at32uc3a1512"  # Prozessor-Typ
INTERFACE   = "jtag"          # Debug-Interface
PROGRAMMER  = "atmelice"      # Programmer-Hardware

# ═════════════════════════════════════════════════════════════════════════════
# 💾 STANDARD-EINSTELLUNGEN
# ═════════════════════════════════════════════════════════════════════════════

DEFAULT_SETTINGS = {
    "atprogram_path": DEFAULT_ATPROGRAM,
    "atbackend_path": DEFAULT_ATBACKEND,
    "objcopy_path": DEFAULT_OBJCOPY,
    "hex_file": "",
    "val_1fc": "E11EFFD7",
    "val_1f8": "929E0977",
    "fuse_val": "F675FFFF",
    "chip_erase": True,
    "user_erase": True,
    "user_write": True,
    "flash_write": True,
    "fuse_write": True,
    "secure": False,
}

# ═════════════════════════════════════════════════════════════════════════════
# 📝 PROGRAMMIER-SCHRITTE
# ═════════════════════════════════════════════════════════════════════════════

PROGRAMMING_STEPS = [
    {"key": "chip_erase", "number": 1, "label": "Flash löschen (ChipErase)"},
    {"key": "user_erase", "number": 2, "label": "User Page löschen"},
    {"key": "user_write", "number": 3, "label": "User Page schreiben"},
    {"key": "flash_write", "number": 4, "label": "Bootloader schreiben"},
    {"key": "fuse_write", "number": 5, "label": "Fuse Bits setzen"},
    {"key": "secure", "number": 6, "label": "Security Bit setzen"},
]

# ═════════════════════════════════════════════════════════════════════════════
# 📊 UI-DIMENSIONEN
# ═════════════════════════════════════════════════════════════════════════════

MIN_WINDOW_WIDTH = 860
MIN_WINDOW_HEIGHT = 680