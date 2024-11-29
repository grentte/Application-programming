import json
from typing import Optional
from Product import Product
from Cart import Cart


class CartJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create_cart(self, user_id: int, cart_id: int) -> Cart:
        cart_data = {
            "cart_id": cart_id,
            "user_id": user_id,
            "products": {}
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"carts": []}

        data["carts"].append(cart_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

        return Cart(user_id, cart_id)

    def read_cart(self, cart_id: int) -> Optional[Cart]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for cart_data in data.get("carts", []):
                if cart_data["cart_id"] == cart_id:
                    cart = Cart(cart_data["user_id"], cart_data["cart_id"])
                    cart.products = {
                        Product(prod["product_id"], prod["name"], prod["price"], prod["stock"]): qty
                        for prod, qty in cart_data.get("products", {}).items()
                    }
                    return cart
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update_cart(self, cart_id: int, product: Product, quantity: int, action: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for cart_data in data.get("carts", []):
                if cart_data["cart_id"] == cart_id:
                    products = cart_data.get("products", {})
                    product_key = str(product.product_id)  # Use product ID as key for JSON serialization

                    if action == "add":
                        if product_key in products:
                            products[product_key]["quantity"] += quantity
                        else:
                            products[product_key] = {
                                "product_id": product.product_id,
                                "name": product.name,
                                "price": product.price,
                                "stock": product.stock,
                                "quantity": quantity,
                            }
                        product.stock -= quantity
                    elif action == "remove":
                        if product_key in products:
                            removed_qty = products[product_key]["quantity"]
                            product.stock += removed_qty
                            del products[product_key]
                        else:
                            return f"{product.name} not found in the cart."

                    cart_data["products"] = products
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return f"Cart {cart_id} updated successfully."
            return "Cart not found."
        except (FileNotFoundError, json.JSONDecodeError):
            return "Error while accessing the cart."

    def delete_cart(self, cart_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            original_length = len(data.get("carts", []))
            data["carts"] = [cart for cart in data.get("carts", []) if cart["cart_id"] != cart_id]

            if len(data["carts"]) == original_length:
                return f"Cart with ID {cart_id} not found."

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return f"Cart {cart_id} deleted successfully."
        except (FileNotFoundError, json.JSONDecodeError):
            return "Error while deleting the cart."

    def get_all_carts(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            return [
                Cart(
                    cart_data["user_id"],
                    cart_data["cart_id"],
                    products={
                        Product(prod["product_id"], prod["name"], prod["price"], prod["stock"]): qty
                        for prod, qty in cart_data.get("products", {}).items()
                    }
                )
                for cart_data in data.get("carts", [])
            ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

