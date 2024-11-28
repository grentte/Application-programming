from Product import Product

class Cart:
    def __init__(self, user_id: int, cart_id: int):
        self.user_id = user_id
        self.cart_id = cart_id
        self.products = {}

    def add_to_cart(self, product: Product, quantity: int):
        if product.stock >= quantity:
            self.products[product] = self.products.get(product, 0) + quantity
            product.stock -= quantity
            return f"{quantity} units of {product.name} added to cart."
        return f"Not enough stock for {product.name}."

    def remove_from_cart(self, product: Product):
        if product in self.products:
            removed_quantity = self.products[product]
            product.stock += removed_quantity
            del self.products[product]
            return f"{product.name} removed from cart."
        return f"{product.name} is not in the cart."

    def view_cart(self):
        return {product.name: qty for product, qty in self.products.items()}

    def clear_cart(self):
        for product, qty in self.products.items():
            product.stock += qty
        self.products.clear()
        return "Cart cleared successfully!"

    def __repr__(self):
        return f"Cart(cart_id={self.cart_id}, user_id={self.user_id}, products={self.view_cart()})"


class CartManager:
    def __init__(self):
        self.carts = {}

    def create_cart(self, user_id: int):
        cart_id = len(self.carts) + 1
        cart = Cart(user_id, cart_id)
        self.carts[cart_id] = cart
        return cart

    def get_cart_by_user(self, user_id: int):
        for cart in self.carts.values():
            if cart.user_id == user_id:
                return cart
        return None

    def update_cart(self, cart_id: int, product: Product, quantity: int, action: str):
        cart = self.carts.get(cart_id)
        if cart:
            if action == "add":
                return cart.add_to_cart(product, quantity)
            elif action == "remove":
                return cart.remove_from_cart(product)
        return "Cart not found."

    def clear_cart(self, cart_id: int):
        cart = self.carts.get(cart_id)
        if cart:
            return cart.clear_cart()
        return "Cart not found."

    def delete_cart(self, cart_id: int):
        if cart_id in self.carts:
            del self.carts[cart_id]
            return f"Cart {cart_id} deleted successfully."
        return "Cart not found."