# -*- coding: utf-8 -*-
# run.py
"""
ProgGUI Starter
- Main Entry Point
- Fenster erstellen + zeigen
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
    
    # Logger initialisieren
    logger = get_logger()
    logger.info("=" * 60)
    logger.info("ProgGUI wird gestartet...")
    logger.info("=" * 60)
    
    try:
        # Root Fenster erstellen
        root = tk.Tk()
        
        # Fenster-Icon
        try:
            from src.utils import IconManager
            IconManager.apply_icon_to_window(root)
        except Exception as e:
            logger.warning(f"Icon konnte nicht geladen werden: {e}")
        
        # MainWindow initialisieren
        main_window = MainWindow(root)
        logger.info("MainWindow erstellt ✅")
        
        # Home-Seite laden
        main_window.show_home()
        logger.info("Home-Seite geladen ✅")
        
        # Fenster anzeigen
        root.mainloop()
        
        logger.info("ProgGUI wurde beendet")
        
    except Exception as e:
        logger.critical(f"Kritischer Fehler: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()