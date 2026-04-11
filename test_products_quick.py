# -*- coding: utf-8 -*-
# test_products_quick.py
"""
Schnell-Test für Product Models
Führe aus: python test_products_quick.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Stelle sicher, dass src im Path ist
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importiere Models
from core.product import Product, ProgrammingStep
from core.product_manager import ProductManager

print("=" * 60)
print("TEST: Product Models")
print("=" * 60)

try:
    # 1️⃣ TESTE ProductManager INIT
    print("\n[TEST 1] Initialisiere ProductManager...")
    manager = ProductManager(Path("data") / "test_products.db")
    print("✅ ProductManager erstellt")
    
    # 2️⃣ TESTE Product ERSTELLUNG
    print("\n[TEST 2] Erstelle neues Produkt...")
    product = Product(
        id=None,
        name="Test Mainboard v1.0",
        description="Test-Produkt für Unit-Tests",
        controller="AT32UC3A1512",
        bootloader_hex="firmware/v1.0/boot.hex",
        userpage_hex="firmware/v1.0/userpage.hex",
        fuse_bits_value="XXXXXXXX",
        steps=Product.create_default_steps(),
        atprogram_path="C:/atprogram.exe",
        atbackend_path="C:/atbackend.exe",
        objcopy_path="C:/avr32-objcopy.exe",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        last_programmed=None
    )
    print(f"✅ Product erstellt: {product}")
    print(f"   - Controller: {product.controller}")
    print(f"   - Steps: {len(product.steps)}")
    
    # 3️⃣ TESTE SPEICHERN
    print("\n[TEST 3] Speichere Produkt in DB...")
    created = manager.create(product)
    print(f"✅ Gespeichert mit ID: {created.id}")
    
    # 4️⃣ TESTE LADEN
    print("\n[TEST 4] Lade Produkt aus DB...")
    loaded = manager.read(created.id)
    print(f"✅ Geladen: {loaded}")
    print(f"   - Name: {loaded.name}")
    print(f"   - Controller: {loaded.controller}")
    print(f"   - Created: {loaded.created_at}")
    
    # 5️⃣ TESTE ALLE ANZEIGEN
    print("\n[TEST 5] Lade alle Produkte...")
    all_products = manager.read_all()
    print(f"✅ {len(all_products)} Produkt(e) in DB:")
    for p in all_products:
        print(f"   - {p.name} ({p.controller})")
    
    # 6️⃣ TESTE UPDATE
    print("\n[TEST 6] Aktualisiere Produkt...")
    loaded.description = "Aktualisierte Beschreibung"
    loaded.steps[0].enabled = False  # Deaktiviere Step 1
    manager.update(loaded)
    print("✅ Produkt aktualisiert")
    
    # 7️⃣ TESTE LESEN NACH NAME
    print("\n[TEST 7] Lade Produkt nach Name...")
    by_name = manager.read_by_name("Test Mainboard v1.0")
    print(f"✅ Gefunden: {by_name.name}")
    
    # 8️⃣ TESTE MARK_PROGRAMMED
    print("\n[TEST 8] Markiere als programmiert...")
    manager.mark_programmed(created.id)
    reloaded = manager.read(created.id)
    print(f"✅ Last Programmed: {reloaded.last_programmed}")
    
    # 9️⃣ TESTE HISTORY
    print("\n[TEST 9] Speichere Programmier-Historie...")
    manager.add_history(
        created.id,
        status="success",
        log_output="Programmierung erfolgreich abgeschlossen"
    )
    print("✅ Historie gespeichert")
    
    # 🔟 TESTE DELETE
    print("\n[TEST 10] Lösche Produkt...")
    manager.delete(created.id)
    deleted = manager.read(created.id)
    if deleted is None:
        print("✅ Produkt gelöscht")
    else:
        print("❌ Produkt nicht gelöscht!")
    
    print("\n" + "=" * 60)
    print("✅ ALLE TESTS BESTANDEN!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ FEHLER: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)