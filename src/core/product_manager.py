import json
import os
from .product import Product

PRODUCTS_FILE = "data/products.json"

class ProductManager:
    def read_all(self):
        if not os.path.exists(PRODUCTS_FILE):
            return []
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Product(**item) for item in raw]

    def save_all(self, products):
        data = [p.__dict__ for p in products]
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

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