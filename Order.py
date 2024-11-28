class Order:
    def __init__(self, order_id, user_id, cart, address, payment_method):
        self.order_id = order_id
        self.user_id = user_id
        self.cart = cart
        self.total_amount = sum(p.price * q for p, q in cart.products.items())
        self.status = "Pending"
        self.address = address
        self.payment_method = payment_method

    def __repr__(self):
        return f"Order(order_id={self.order_id}, user_id={self.user_id}, total_amount={self.total_amount}, status='{self.status}')"

    def place_order(self):
        self.status = "Placed"
        return f"Order {self.order_id} placed"

    def cancel_order(self):
        if self.status == "Placed":
            self.status = "Cancelled"
            self.cart.clear_cart()
            return f"Order {self.order_id} cancelled."
        return f"Order{self.order_id} is not placed."

class OrderManager:
    pass
