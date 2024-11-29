from Inventory import Inventory
from Product import Product, ProductNotFoundError


class SellerNotFoundError(Exception):
    def __init__(self, seller_id):
        super().__init__(f"Seller with ID {seller_id} not found.")


class Seller:
    def __init__(self, seller_id: int, name: str, inventory: Inventory = None):
        if not isinstance(seller_id, int) or seller_id <= 0:
            raise ValueError("Seller ID must be a positive integer.")
        if not name:
            raise ValueError("Seller name cannot be empty.")
        self.seller_id = seller_id
        self.name = name
        self.inventory = inventory or {}

    def __repr__(self):
        return f"Seller(seller_id={self.seller_id}, name='{self.name}', inventory={list(self.inventory.keys())})"

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Invalid product. Must be an instance of Product.")
        self.inventory[product.product_id] = product
        return f"Product {product.name} added to inventory."

    def remove_product(self, product_id: int):
        if product_id not in self.inventory:
            raise ProductNotFoundError(product_id)
        removed_product = self.inventory.pop(product_id)
        return f"Product {removed_product.name} removed from inventory."

    def update_stock(self, product_id: int, new_stock: int):
        if product_id not in self.inventory:
            raise ProductNotFoundError(product_id)
        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        product = self.inventory[product_id]
        product.stock = new_stock
        return f"Stock for {product.name} updated to {new_stock}."

    def list_inventory(self):
        return {product_id: product.name for product_id, product in self.inventory.items()}


class SellerManager:
    def __init__(self):
        self.sellers = {}
        self.current_seller_id = 1

    def add_seller(self, name: str, inventory: Inventory = None):
        if not name:
            raise ValueError("Seller name cannot be empty.")
        seller = Seller(seller_id=self.current_seller_id, name=name, inventory=inventory or {})
        self.sellers[self.current_seller_id] = seller
        self.current_seller_id += 1
        return seller

    def get_seller(self, seller_id: int):
        seller = self.sellers.get(seller_id)
        if not seller:
            raise SellerNotFoundError(seller_id)
        return seller

    def update_seller(self, seller_id: int, name: str = None):
        seller = self.get_seller(seller_id)
        if name:
            seller.name = name
        return seller

    def delete_seller(self, seller_id: int):
        seller = self.sellers.pop(seller_id, None)
        if not seller:
            raise SellerNotFoundError(seller_id)
        return f"Seller {seller.name} deleted."

    def add_product_to_seller(self, seller_id: int, product: Product):
        seller = self.get_seller(seller_id)
        return seller.add_product(product)

    def remove_product_from_seller(self, seller_id: int, product_id: int):
        seller = self.get_seller(seller_id)
        return seller.remove_product(product_id)

    def update_seller_product_stock(self, seller_id: int, product_id: int, new_stock: int):
        seller = self.get_seller(seller_id)
        return seller.update_stock(product_id, new_stock)

    def list_all_sellers(self):
        return list(self.sellers.values())

    def list_seller_inventory(self, seller_id: int):
        seller = self.get_seller(seller_id)
        return seller.list_inventory()
