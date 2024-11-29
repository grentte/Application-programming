from Product import Product, ProductNotFoundError


class Inventory:
    def __init__(self):
        self.products = {}

    def __str__(self):
        return "\n".join(
            [f"{product.name} (ID: {product_id}, Price: {product.price}, Stock: {product.stock})"
             for product_id, product in self.products.items()]
        )

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Invalid product. Must be an instance of Product.")
        self.products[product.product_id] = product
        return f"Product {product.name} added to inventory."

    def remove_product(self, product_id: int):
        if product_id not in self.products:
            raise ProductNotFoundError(product_id)
        removed_product = self.products.pop(product_id)
        return f"Product {removed_product.name} removed from inventory."

    def update_stock(self, product_id: int, new_stock: int):
        if product_id not in self.products:
            raise ProductNotFoundError(product_id)
        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.products[product_id].stock = new_stock
        return f"Stock for product {self.products[product_id].name} updated to {new_stock}."

    def update_price(self, product_id: int, new_price: float):
        if product_id not in self.products:
            raise ProductNotFoundError(product_id)
        if new_price < 0:
            raise ValueError("Price cannot be negative.")
        self.products[product_id].price = new_price
        return f"Price for product {self.products[product_id].name} updated to {new_price:.2f}."

    def get_product(self, product_id: int):
        if product_id not in self.products:
            raise ProductNotFoundError(product_id)
        product = self.products[product_id]
        return f"{product.name} (ID: {product.product_id}, Price: {product.price}, Stock: {product.stock})"

    def list_products(self):
        if not self.products:
            return "No products in inventory."
        return "\n".join(
            [f"{product.name} (ID: {product_id}, Price: {product.price:.2f}, Stock: {product.stock})"
             for product_id, product in self.products.items()]
        )


class InventoryManager:
    def __init__(self):
        self.inventories = {}

    def create_inventory(self, seller_id: int):
        if seller_id in self.inventories:
            raise ValueError(f"Inventory for seller ID {seller_id} already exists.")
        self.inventories[seller_id] = Inventory()
        return f"Inventory created for seller ID {seller_id}."

    def get_inventory(self, seller_id: int):
        if seller_id not in self.inventories:
            raise KeyError(f"No inventory found for seller ID {seller_id}.")
        return self.inventories[seller_id]

    def delete_inventory(self, seller_id: int):
        if seller_id not in self.inventories:
            raise KeyError(f"No inventory found for seller ID {seller_id}.")
        del self.inventories[seller_id]
        return f"Inventory for seller ID {seller_id} deleted."
