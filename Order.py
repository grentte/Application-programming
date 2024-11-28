from Cart import Cart
from Address import Address


class Order:
    def __init__(self, order_id: int, user_id: int, cart: Cart, address: Address, payment_method: str):
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
        return f"Order {self.order_id} is not placed."


class OrderManager:
    def __init__(self):
        self.orders = {}  # Словарь для хранения заказов, где ключ - order_id, значение - объект Order
        self.current_order_id = 1

    def create_order(self, user_id: int, cart: Cart, address: Address, payment_method: str):
        order = Order(self.current_order_id, user_id, cart, address, payment_method)
        self.orders[self.current_order_id] = order
        self.current_order_id += 1
        return order

    def read_order_by_id(self, order_id: int):
        return self.orders.get(order_id, "Order not found.")

    def update_order(self, order_id: int, status: str = None, address: Address = None, payment_method: str = None):
        order = self.orders.get(order_id)
        if order:
            if status:
                order.status = status
            if address:
                order.address = address
            if payment_method:
                order.payment_method = payment_method
            return order
        return "Order not found."

    def delete_order(self, order_id: int):
        order = self.orders.get(order_id)
        if order:
            del self.orders[order_id]
            return f"Order {order_id} deleted."
        return "Order not found."

    def get_all_orders(self):
        return list(self.orders.values())

    def get_orders_by_user(self, user_id: int):
        return [order for order in self.orders.values() if order.user_id == user_id]
