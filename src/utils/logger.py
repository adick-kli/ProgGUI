# -*- coding: utf-8 -*-
# src/utils/logger.py
"""
Logger Module
- Logging für ProgGUI
- Console + File Logging
"""

import logging
from pathlib import Path
from datetime import datetime


class ProgGUILogger:
    """Logger für ProgGUI."""
    
    def __init__(self, name: str = "ProgGUI"):
        """Initialisiert den Logger."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Erstelle logs/ Verzeichnis
        logs_dir = Path(__file__).parent.parent.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Log-Datei
        log_file = logs_dir / f"proggui_{datetime.now().strftime('%Y%m%d')}.log"
        
        # File Handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Füge Handler hinzu
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """Debug-Level Logging."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Info-Level Logging."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Warning-Level Logging."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Error-Level Logging."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Critical-Level Logging."""
        self.logger.critical(message)


# Global Logger Instance
_logger_instance = None


def get_logger(name: str = "ProgGUI") -> ProgGUILogger:
    """Holt die globale Logger-Instanz."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ProgGUILogger(name)
    return _logger_instance