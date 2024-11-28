from Product import Product


class Inventory:
    def __init__(self):
        self.products = {}

    def __str__(self):
        return [f"{product.name} (ID: {product_id}, Price: {product.price}, Stock: {product.stock})"
                for product_id, product in self.products.items()]

    def add_product(self, product: Product):
        self.products[product.product_id] = product
        return f"Product {product.name} added to inventory."

    def remove_product(self, product_id: int):
        removed_product = self.products.pop(product_id)
        return f"Product {removed_product.name} removed from inventory."

    def update_stock(self, product_id: int, new_stock: int):
        self.products[product_id].stock = new_stock
        return f"Stock for product {self.products[product_id].name} updated to {new_stock}."

    def update_price(self, product_id: int, new_price: float):
        self.products[product_id].price = new_price
        return f"Price for product {self.products[product_id].name} updated to {new_price:.2f}."

    def get_product(self, product_id: int):
        product = self.products[product_id]
        return f"{product.name} (ID: {product.product_id}, Price: {product.price}, Stock: {product.stock})"

class InventoryManager:
    def __init__(self):
        self.inventories = {}

    def create_inventory(self, seller_id: int):
        if seller_id not in self.inventories:
            self.inventories[seller_id] = Inventory()
            return f"Inventory created for seller ID {seller_id}."
        return f"Inventory for seller ID {seller_id} already exists."

    def get_inventory(self, seller_id: int):
        if seller_id in self.inventories:
            return self.inventories[seller_id]
        return f"No inventory found for seller ID {seller_id}."

    def delete_inventory(self, seller_id: int):
        if seller_id in self.inventories:
            del self.inventories[seller_id]
            return f"Inventory for seller ID {seller_id} deleted."
        return f"No inventory found for seller ID {seller_id}."