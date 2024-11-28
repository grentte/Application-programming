class Seller:
    def __init__(self, seller_id, name, email, inventory=None):
        self.seller_id = seller_id
        self.name = name
        self.email = email
        self.inventory = inventory or {}

    def __repr__(self):
        return f"Seller(seller_id={self.seller_id}, name='{self.name}', email='{self.email}', inventory={list(self.inventory.keys())})"

    def add_product(self, product):
        self.inventory[product.product_id] = product
        return f"Product {product.name} added to inventory."

    def remove_product(self, product_id):
        removed_product = self.inventory.pop(product_id)
        return f"Product {removed_product.name} removed from inventory."

    def update_stock(self, product_id, new_stock):
        product = self.inventory[product_id]
        product.stock = new_stock
        return f"Stock for {product.name} updated to {new_stock}."

    def list_inventory(self):
        """List all products in the seller's inventory."""
        return {product_id: product.name for product_id, product in self.inventory.items()}

class SellerManager:
    pass

