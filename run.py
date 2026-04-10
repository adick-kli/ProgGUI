# -*- coding: utf-8 -*-
# run.py
"""
ProgGUI - Starter Script
Einstiegspunkt für die Anwendung.

Verwendung:
    python run.py
"""

import sys
import os

# Füge src zum Path hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app.main import main


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting ProgGUI - AT32UC3 Programmer")
    print("=" * 60)
    print()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Application closed by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Application crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)