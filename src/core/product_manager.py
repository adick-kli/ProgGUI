# -*- coding: utf-8 -*-
# src/core/product_manager.py
"""
ProductManager - Verwaltet alle Produkte
- CRUD-Operationen auf products.db
- Lädt/speichert Products
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from .product import Product, ProgrammingStep


class ProductManager:
    """Verwaltet alle Produkte in der Datenbank."""
    
    def __init__(self, db_path: Path = None):
        """
        Initialisiert ProductManager.
        
        Args:
            db_path: Pfad zur products.db
                    Default: data/products.db
        """
        if db_path is None:
            db_path = Path("data") / "products.db"
        
        self.db_path = db_path
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Initialisiere Datenbank
        self._init_db()
    
    def _init_db(self):
        """Erstellt die Datenbank-Tabellen falls nicht vorhanden."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    controller TEXT NOT NULL,
                    bootloader_hex TEXT NOT NULL,
                    userpage_hex TEXT NOT NULL,
                    fuse_bits_value TEXT NOT NULL,
                    steps TEXT NOT NULL,
                    atprogram_path TEXT,
                    atbackend_path TEXT,
                    objcopy_path TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    last_programmed TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS programming_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    programmed_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    log_output TEXT,
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """)
            
            conn.commit()
    
    def create(self, product: Product) -> Product:
        """
        Erstellt ein neues Produkt.
        
        Args:
            product: Product-Objekt ohne ID
        
        Returns:
            Product mit neu zugewiesener ID
        """
        steps_json = json.dumps([
            {
                "number": s.number,
                "name": s.name,
                "description": s.description,
                "enabled": s.enabled
            }
            for s in product.steps
        ])
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO products (
                    name, description, controller, bootloader_hex,
                    userpage_hex, fuse_bits_value, steps,
                    atprogram_path, atbackend_path, objcopy_path,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product.name,
                product.description,
                product.controller,
                product.bootloader_hex,
                product.userpage_hex,
                product.fuse_bits_value,
                steps_json,
                product.atprogram_path,
                product.atbackend_path,
                product.objcopy_path,
                datetime.now().isoformat(),
                datetime.now().isoformat(),
            ))
            
            conn.commit()
            product.id = cursor.lastrowid
        
        return product
    
    def read(self, product_id: int) -> Optional[Product]:
        """Liest ein Produkt aus der DB."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM products WHERE id = ?",
                (product_id,)
            ).fetchone()
        
        if not row:
            return None
        
        return self._row_to_product(row)
    
    def read_by_name(self, name: str) -> Optional[Product]:
        """Liest ein Produkt nach Name."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM products WHERE name = ?",
                (name,)
            ).fetchone()
        
        if not row:
            return None
        
        return self._row_to_product(row)
    
    def read_all(self) -> List[Product]:
        """Liest alle Produkte."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM products ORDER BY created_at DESC"
            ).fetchall()
        
        return [self._row_to_product(row) for row in rows]
    
    def update(self, product: Product) -> bool:
        """
        Aktualisiert ein bestehendes Produkt.
        
        Args:
            product: Product mit ID
        
        Returns:
            True bei Erfolg
        """
        if not product.id:
            raise ValueError("Product muss eine ID haben zum Update")
        
        steps_json = json.dumps([
            {
                "number": s.number,
                "name": s.name,
                "description": s.description,
                "enabled": s.enabled
            }
            for s in product.steps
        ])
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE products SET
                    name = ?, description = ?, controller = ?,
                    bootloader_hex = ?, userpage_hex = ?,
                    fuse_bits_value = ?, steps = ?,
                    atprogram_path = ?, atbackend_path = ?,
                    objcopy_path = ?, updated_at = ?
                WHERE id = ?
            """, (
                product.name,
                product.description,
                product.controller,
                product.bootloader_hex,
                product.userpage_hex,
                product.fuse_bits_value,
                steps_json,
                product.atprogram_path,
                product.atbackend_path,
                product.objcopy_path,
                datetime.now().isoformat(),
                product.id,
            ))
            
            conn.commit()
        
        return True
    
    def delete(self, product_id: int) -> bool:
        """Löscht ein Produkt."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
        
        return True
    
    def mark_programmed(self, product_id: int):
        """Aktualisiert last_programmed Zeitstempel."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE products SET last_programmed = ? WHERE id = ?",
                (datetime.now().isoformat(), product_id)
            )
            conn.commit()
    
    def add_history(self, product_id: int, status: str, log_output: str = ""):
        """Speichert Programmier-Historie."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO programming_history (
                    product_id, programmed_at, status, log_output
                ) VALUES (?, ?, ?, ?)
            """, (
                product_id,
                datetime.now().isoformat(),
                status,
                log_output
            ))
            conn.commit()
    
    def _row_to_product(self, row: sqlite3.Row) -> Product:
        """Konvertiert DB-Row zu Product-Objekt."""
        steps_data = json.loads(row["steps"])
        steps = [ProgrammingStep(**step) for step in steps_data]
        
        return Product(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            controller=row["controller"],
            bootloader_hex=row["bootloader_hex"],
            userpage_hex=row["userpage_hex"],
            fuse_bits_value=row["fuse_bits_value"],
            steps=steps,
            atprogram_path=row["atprogram_path"],
            atbackend_path=row["atbackend_path"],
            objcopy_path=row["objcopy_path"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            last_programmed=datetime.fromisoformat(row["last_programmed"]) 
                           if row["last_programmed"] else None,
        )