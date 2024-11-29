from Cart import Cart
from Address import Address


class InvalidOrderStatusError(Exception):
    def __init__(self, order_id, current_status, attempted_status):
        super().__init__(f"Cannot change status of order {order_id} from '{current_status}' to '{attempted_status}'.")


class OrderNotFoundError(Exception):
    def __init__(self, order_id):
        super().__init__(f"Order with ID {order_id} not found.")


class Order:
    def __init__(self, order_id: int, user_id: int, cart: Cart, address: Address, payment_method: str):
        if not cart.products:
            raise ValueError("Cart is empty. Cannot create an order.")
        self.order_id = order_id
        self.user_id = user_id
        self.cart = cart
        self.total_amount = sum(p.price * q for p, q in cart.products.items())
        if self.total_amount <= 0:
            raise ValueError("Total amount must be greater than zero.")
        self.status = "Pending"
        self.address = address
        self.payment_method = payment_method

    def __repr__(self):
        return (f"Order(order_id={self.order_id}, user_id={self.user_id}, total_amount={self.total_amount}, "
                f"status='{self.status}')")

    def place_order(self):
        if self.status != "Pending":
            raise InvalidOrderStatusError(self.order_id, self.status, "Placed")
        self.status = "Placed"
        return f"Order {self.order_id} placed."

    def cancel_order(self):
        if self.status != "Placed":
            raise InvalidOrderStatusError(self.order_id, self.status, "Cancelled")
        self.status = "Cancelled"
        self.cart.clear_cart()
        return f"Order {self.order_id} cancelled."


class OrderManager:
    def __init__(self):
        self.orders = {}
        self.current_order_id = 1

    def create_order(self, user_id: int, cart: Cart, address: Address, payment_method: str):
        if not address:
            raise ValueError("Address cannot be empty.")
        if not payment_method:
            raise ValueError("Payment method is required.")
        order = Order(self.current_order_id, user_id, cart, address, payment_method)
        self.orders[self.current_order_id] = order
        self.current_order_id += 1
        return order

    def read_order_by_id(self, order_id: int):
        order = self.orders.get(order_id)
        if not order:
            raise OrderNotFoundError(order_id)
        return order

    def update_order(self, order_id: int, status: str = None, address: Address = None, payment_method: str = None):
        try:
            order = self.read_order_by_id(order_id)
        except OrderNotFoundError as e:
            return str(e)

        if status:
            if status not in ["Pending", "Placed", "Cancelled", "Completed"]:
                raise ValueError("Invalid status value.")
            order.status = status
        if address:
            order.address = address
        if payment_method:
            order.payment_method = payment_method
        return order

    def delete_order(self, order_id: int):
        try:
            order = self.read_order_by_id(order_id)
            del self.orders[order_id]
            return f"Order {order_id} deleted."
        except OrderNotFoundError as e:
            return str(e)

    def get_all_orders(self):
        return list(self.orders.values())

    def get_orders_by_user(self, user_id: int):
        orders = [order for order in self.orders.values() if order.user_id == user_id]
        if not orders:
            raise ValueError(f"No orders found for user ID {user_id}.")
        return orders
