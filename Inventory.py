class Inventory:
    def __init__(self):
        self.products = {}

    def __str__(self):
        return [f"{product.name} (ID: {product_id}, Price: {product.price}, Stock: {product.stock})"
                for product_id, product in self.products.items()]

    def add_product(self, product):
        self.products[product.product_id] = product
        return f"Product {product.name} added to inventory."

    def remove_product(self, product_id):
        removed_product = self.products.pop(product_id)
        return f"Product {removed_product.name} removed from inventory."

    def update_stock(self, product_id, new_stock):
        self.products[product_id].stock = new_stock
        return f"Stock for product {self.products[product_id].name} updated to {new_stock}."

    def update_price(self, product_id, new_price):
        self.products[product_id].price = new_price
        return f"Price for product {self.products[product_id].name} updated to {new_price:.2f}."

    def get_product(self, product_id):
        product = self.products[product_id]
        return f"{product.name} (ID: {product.product_id}, Price: {product.price}, Stock: {product.stock})"

class InventoryManager:
    pass

