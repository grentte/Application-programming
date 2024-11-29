import json
from typing import Optional
from Product import Product, ProductNotFoundError

class InventoryNotFoundError(Exception):
    pass

class InventoryJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create_inventory(self, seller_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"inventories": []}

        if any(inventory["seller_id"] == seller_id for inventory in data["inventories"]):
            raise ValueError(f"Inventory for seller ID {seller_id} already exists.")

        data["inventories"].append({"seller_id": seller_id, "products": []})

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

        return f"Inventory created for seller ID {seller_id}."

    def get_inventory(self, seller_id: int) -> Optional[dict]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for inventory in data.get("inventories", []):
                if inventory["seller_id"] == seller_id:
                    return inventory
            return None
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def delete_inventory(self, seller_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("inventories", []))
            data["inventories"] = [inventory for inventory in data.get("inventories", []) if inventory["seller_id"] != seller_id]

            if len(data["inventories"]) == original_length:
                raise InventoryNotFoundError(f"No inventory found for seller ID {seller_id}.")

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)

            return f"Inventory for seller ID {seller_id} deleted."

        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except InventoryNotFoundError as e:
            print(e)
            return False

    def add_product(self, seller_id: int, product: Product):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for inventory in data.get("inventories", []):
                if inventory["seller_id"] == seller_id:
                    for existing_product in inventory["products"]:
                        if existing_product["product_id"] == product.product_id:
                            raise ValueError(f"Product with ID {product.product_id} already exists.")

                    inventory["products"].append({
                        "product_id": product.product_id,
                        "name": product.name,
                        "price": product.price,
                        "stock": product.stock
                    })

                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)

                    return f"Product {product.name} added to inventory."

            raise InventoryNotFoundError(f"No inventory found for seller ID {seller_id}.")

        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except InventoryNotFoundError as e:
            print(e)
            return False
        except ValueError as e:
            print(e)
            return False

    def remove_product(self, seller_id: int, product_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for inventory in data.get("inventories", []):
                if inventory["seller_id"] == seller_id:
                    product_found = False
                    for existing_product in inventory["products"]:
                        if existing_product["product_id"] == product_id:
                            inventory["products"].remove(existing_product)
                            product_found = True
                            break

                    if not product_found:
                        raise ProductNotFoundError(product_id)

                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)

                    return f"Product with ID {product_id} removed from inventory."

            raise InventoryNotFoundError(f"No inventory found for seller ID {seller_id}.")

        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except InventoryNotFoundError as e:
            print(e)
            return False
        except ProductNotFoundError as e:
            print(e)
            return False

    def update_stock(self, seller_id: int, product_id: int, new_stock: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for inventory in data.get("inventories", []):
                if inventory["seller_id"] == seller_id:
                    for product in inventory["products"]:
                        if product["product_id"] == product_id:
                            if new_stock < 0:
                                raise ValueError("Stock cannot be negative.")
                            product["stock"] = new_stock

                            with open(self.filepath, "w") as file:
                                json.dump(data, file, indent=4)

                            return f"Stock for product {product['name']} updated to {new_stock}."

                    raise ProductNotFoundError(product_id)

            raise InventoryNotFoundError(f"No inventory found for seller ID {seller_id}.")

        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except InventoryNotFoundError as e:
            print(e)
            return False
        except ProductNotFoundError as e:
            print(e)
            return False
        except ValueError as e:
            print(e)
            return False

    def update_price(self, seller_id: int, product_id: int, new_price: float):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for inventory in data.get("inventories", []):
                if inventory["seller_id"] == seller_id:
                    for product in inventory["products"]:
                        if product["product_id"] == product_id:
                            if new_price < 0:
                                raise ValueError("Price cannot be negative.")
                            product["price"] = new_price

                            with open(self.filepath, "w") as file:
                                json.dump(data, file, indent=4)

                            return f"Price for product {product['name']} updated to {new_price:.2f}."

                    raise ProductNotFoundError(product_id)

            raise InventoryNotFoundError(f"No inventory found for seller ID {seller_id}.")

        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except InventoryNotFoundError as e:
            print(e)
            return False
        except ProductNotFoundError as e:
            print(e)
            return False
        except ValueError as e:
            print(e)
            return False

    def list_products(self, seller_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for inventory in data.get("inventories", []):
                if inventory["seller_id"] == seller_id:
                    if not inventory["products"]:
                        return "No products in inventory."
                    return "\n".join(
                        [f"{product['name']} (ID: {product['product_id']}, Price: {product['price']:.2f}, Stock: {product['stock']})"
                         for product in inventory["products"]]
                    )

            raise InventoryNotFoundError(f"No inventory found for seller ID {seller_id}.")

        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except InventoryNotFoundError as e:
            print(e)
            return False
