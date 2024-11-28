from Inventory import Inventory
from Product import Product


class Seller:
    def __init__(self, seller_id: int, name: str, inventory: Inventory = None):
        self.seller_id = seller_id
        self.name = name
        self.inventory = inventory or {}

    def __repr__(self):
        return f"Seller(seller_id={self.seller_id}, name='{self.name}', inventory={list(self.inventory.keys())})"

    def add_product(self, product: Product):
        self.inventory[product.product_id] = product
        return f"Product {product.name} added to inventory."

    def remove_product(self, product_id: int):
        removed_product = self.inventory.pop(product_id)
        return f"Product {removed_product.name} removed from inventory."

    def update_stock(self, product_id: int, new_stock: int):
        product = self.inventory[product_id]
        product.stock = new_stock
        return f"Stock for {product.name} updated to {new_stock}."

    def list_inventory(self):
        """List all products in the seller's inventory."""
        return {product_id: product.name for product_id, product in self.inventory.items()}

class SellerManager:
    def __init__(self):
        self.sellers = {}  # Словарь для хранения продавцов: ключ - seller_id, значение - объект Seller
        self.current_seller_id = 1

    def add_seller(self, name: str, inventory: Inventory = None):
        """Добавить нового продавца."""
        seller = Seller(seller_id=self.current_seller_id, name=name, inventory=inventory or {})
        self.sellers[self.current_seller_id] = seller
        self.current_seller_id += 1
        return seller

    def get_seller(self, seller_id: int):
        """Получить продавца по его ID."""
        return self.sellers.get(seller_id, "Seller not found.")

    def update_seller(self, seller_id: int, name: str = None):
        """Обновить информацию о продавце."""
        seller = self.sellers.get(seller_id)
        if not seller:
            return "Seller not found."
        if name:
            seller.name = name
        return seller

    def delete_seller(self, seller_id: int):
        """Удалить продавца."""
        seller = self.sellers.pop(seller_id, None)
        if seller:
            return f"Seller {seller.name} deleted."
        return "Seller not found."

    def add_product_to_seller(self, seller_id: int, product: Product):
        """Добавить продукт в инвентарь продавца."""
        seller = self.sellers.get(seller_id)
        if not seller:
            return "Seller not found."
        return seller.add_product(product)

    def remove_product_from_seller(self, seller_id: int, product_id: int):
        """Удалить продукт из инвентаря продавца."""
        seller = self.sellers.get(seller_id)
        if not seller:
            return "Seller not found."
        if product_id not in seller.inventory:
            return "Product not found in inventory."
        return seller.remove_product(product_id)

    def update_seller_product_stock(self, seller_id: int, product_id: int, new_stock: int):
        """Обновить количество продукта в инвентаре продавца."""
        seller = self.sellers.get(seller_id)
        if not seller:
            return "Seller not found."
        if product_id not in seller.inventory:
            return "Product not found in inventory."
        return seller.update_stock(product_id, new_stock)

    def list_all_sellers(self):
        """Получить список всех продавцов."""
        return list(self.sellers.values())

    def list_seller_inventory(self, seller_id: int):
        """Получить инвентарь конкретного продавца."""
        seller = self.sellers.get(seller_id)
        if not seller:
            return "Seller not found."
        return seller.list_inventory()