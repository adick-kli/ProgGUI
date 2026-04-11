# -*- coding: utf-8 -*-
# run.py
"""
ProgGUI Starter
- Main Entry Point
"""

import tkinter as tk
import sys
from pathlib import Path

# Füge src/ zum Python Path hinzu
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.app.windows.main_window import MainWindow
from src.utils import get_logger

def main():
    """Startet ProgGUI."""
    
    logger = get_logger()
    logger.info("=" * 60)
    logger.info("ProgGUI wird gestartet...")
    logger.info("=" * 60)
    
    try:
        # Root Fenster erstellen
        root = tk.Tk()
        
        # MainWindow initialisieren (mit root!)
        main_window = MainWindow(root)
        logger.info("[OK] MainWindow erstellt")
        
        # Fenster-Icon
        try:
            from src.utils.icon_manager import IconManager
            IconManager.apply_icon_to_window(root)
        except Exception as e:
            logger.warning(f"Icon konnte nicht geladen werden: {e}")
        
        logger.info("App ist bereit!")
        logger.info("=" * 60)
        
        # Fenster anzeigen
        root.mainloop()
        
        logger.info("ProgGUI wurde beendet")
        
    except Exception as e:
        logger.critical(f"Kritischer Fehler: {e}")
        raise


if __name__ == "__main__":
    main()