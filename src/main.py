# -*- coding: utf-8 -*-
# src/main.py
"""
ProgGUI - Entry Point
Startet die Anwendung
"""

import sys
from pathlib import Path

# Stelle sicher, dass src/ im Python-Path ist
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from app.gui import main

if __name__ == "__main__":
    main()
