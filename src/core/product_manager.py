import json
import os
from .product import Product, ProgrammingStep
from datetime import datetime

PRODUCTS_FILE = "data/products.json"

# === Hilfsfunktionen für JSON-Konvertierung, AUßERHALB der Klasse! ===
def programming_step_to_dict(step):
    return {
        "number": step.number,
        "name": step.name,
        "description": step.description,
        "enabled": step.enabled
    }

def dict_to_product(d):
    d = d.copy()
    d["steps"] = [ProgrammingStep(**s) for s in d.get("steps", [])]
    # Zeitfelder als datetime zurückwandeln
    if d.get("created_at"):
        d["created_at"] = datetime.fromisoformat(d["created_at"])
    if d.get("updated_at"):
        d["updated_at"] = datetime.fromisoformat(d["updated_at"])
    if d.get("last_programmed"):
        d["last_programmed"] = datetime.fromisoformat(d["last_programmed"]) if d["last_programmed"] else None
    return Product(**d)

def dict_to_product(d):
    d = d.copy()
    d["steps"] = [ProgrammingStep(**s) for s in d.get("steps", [])]
    return Product(**d)

class ProductManager:
    def save_all(self, products):
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
            json.dump([product_to_dict(p) for p in products], f, ensure_ascii=False, indent=2)

    def read_all(self):
        if not os.path.exists(PRODUCTS_FILE):
            return []
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [dict_to_product(item) for item in raw]

    def create(self, product):
        products = self.read_all()
        products.append(product)
        self.save_all(products)

    def update(self, product):
        products = self.read_all()
        for idx, p in enumerate(products):
            if p.id == product.id:
                products[idx] = product
                break
        self.save_all(products)

    def delete(self, product_id):
        products = self.read_all()
        products = [p for p in products if p.id != product_id]
        self.save_all(products)