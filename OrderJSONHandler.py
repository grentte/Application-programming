import json
from typing import Optional
from Cart import Cart
from Address import Address
from Order import Order, InvalidOrderStatusError, OrderNotFoundError

class OrderJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create_order(self, user_id: int, cart: Cart, address: Address, payment_method: str) -> Order:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"orders": []}

        order = Order(len(data["orders"]) + 1, user_id, cart, address, payment_method)
        data["orders"].append({
            "order_id": order.order_id,
            "user_id": order.user_id,
            "total_amount": order.total_amount,
            "status": order.status,
            "address": {
                "city": address.city if address else None,
                "street": address.street if address else None,
                "house": address.house if address else None,
                "apartment": address.apartment if address else None,
            },
            "payment_method": order.payment_method
        })

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

        return order

    def read_order_by_id(self, order_id: int) -> Optional[Order]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for order_data in data["orders"]:
                if order_data["order_id"] == order_id:
                    address = Address(
                        order_data["address"]["street"],
                        order_data["address"]["city"],
                        order_data["address"]["house"],
                        order_data["address"]["apartment"]
                    )
                    cart = Cart()
                    cart.load_from_json(order_data.get("cart", []))
                    order = Order(order_data["order_id"], order_data["user_id"], cart, address, order_data["payment_method"])
                    order.status = order_data["status"]
                    return order
            return None
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update_order(self, order_id: int, status: str = None, address: Address = None, payment_method: str = None) -> Optional[Order]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            order_data = next((order for order in data["orders"] if order["order_id"] == order_id), None)
            if not order_data:
                raise OrderNotFoundError(order_id)

            if status:
                if status not in ["Pending", "Placed", "Cancelled", "Completed"]:
                    raise ValueError("Invalid status value.")
                order_data["status"] = status
            if address:
                order_data["address"] = {
                    "city": address.city if address else None,
                    "street": address.street if address else None,
                    "house": address.house if address else None,
                    "apartment": address.apartment if address else None,
                }
            if payment_method:
                order_data["payment_method"] = payment_method

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)

            address_obj = Address(
                order_data["address"]["street"],
                order_data["address"]["city"],
                order_data["address"]["house"],
                order_data["address"]["apartment"]
            )
            cart = Cart()
            cart.load_from_json(order_data.get("cart", []))
            order = Order(order_data["order_id"], order_data["user_id"], cart, address_obj, order_data["payment_method"])
            order.status = order_data["status"]
            return order

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error updating order: {e}")
            return None
        except OrderNotFoundError as e:
            print(e)
            return None

    def delete_order(self, order_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            original_length = len(data["orders"])
            data["orders"] = [order for order in data["orders"] if order["order_id"] != order_id]

            if len(data["orders"]) == original_length:
                raise OrderNotFoundError(order_id)

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)

            return f"Order {order_id} deleted."

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error deleting order: {e}")
            return None
        except OrderNotFoundError as e:
            print(e)
            return None

    def get_all_orders(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            orders = []
            for order_data in data["orders"]:
                address = Address(
                    order_data["address"]["street"],
                    order_data["address"]["city"],
                    order_data["address"]["house"],
                    order_data["address"]["apartment"]
                )
                cart = Cart()
                cart.load_from_json(order_data.get("cart", []))
                order = Order(order_data["order_id"], order_data["user_id"], cart, address, order_data["payment_method"])
                order.status = order_data["status"]
                orders.append(order)
            return orders
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_orders_by_user(self, user_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            user_orders = [order for order in data["orders"] if order["user_id"] == user_id]
            if not user_orders:
                raise ValueError(f"No orders found for user ID {user_id}.")
            orders = []
            for order_data in user_orders:
                address = Address(
                    order_data["address"]["street"],
                    order_data["address"]["city"],
                    order_data["address"]["house"],
                    order_data["address"]["apartment"]
                )
                cart = Cart()
                cart.load_from_json(order_data.get("cart", []))
                order = Order(order_data["order_id"], order_data["user_id"], cart, address, order_data["payment_method"])
                order.status = order_data["status"]
                orders.append(order)
            return orders
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        except ValueError as e:
            print(e)
            return []
