class Cart:
    def __init__(self, user_id, cart_id):
        self.user_id = user_id
        self.cart_id = cart_id
        self.products = {}

    def add_to_cart(self, product, quantity):
        pass

    def remove_from_cart(self, product):
        pass

    def view_cart(self):
        pass

    def clear_cart(self):
        pass

    def __repr__(self):
        return f"Cart(cart_id={self.cart_id}, user_id={self.user_id}, products={self.view_cart()})"


class CartManager:
    pass

