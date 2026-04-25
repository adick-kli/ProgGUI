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

def product_to_dict(product):
    d = product.__dict__.copy()
    d["steps"] = [programming_step_to_dict(s) for s in product.steps]
    # Zeitfelder als ISO-String kodieren!
    for time_key in ["created_at", "updated_at", "last_programmed"]:
        if d.get(time_key):
            d[time_key] = d[time_key].isoformat() if d[time_key] else None
    return d

def dict_to_product(d):
    d = d.copy()
    d["steps"] = [ProgrammingStep(**s) for s in d.get("steps", [])]
    # Zeitfelder als datetime zurückwandeln
    for time_key in ["created_at", "updated_at", "last_programmed"]:
        if d.get(time_key):
            d[time_key] = datetime.fromisoformat(d[time_key]) if d[time_key] else None
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