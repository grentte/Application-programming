import json
from Product import Product, ProductNotFoundError
from Seller import Seller, SellerNotFoundError


class SellerJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, name: str, inventory: dict = None):
        seller_data = {
            "name": name,
            "inventory": {product.product_id: product.__repr__() for product in inventory.values()} if inventory else {}
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"sellers": []}

        # Check for duplicate seller by name or seller_id
        if any(existing_seller["name"] == name for existing_seller in data["sellers"]):
            raise ValueError(f"Seller with name '{name}' already exists.")

        seller_data["seller_id"] = len(data["sellers"]) + 1
        data["sellers"].append(seller_data)

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

        return seller_data

    def read(self, seller_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for seller_data in data.get("sellers", []):
                if seller_data["seller_id"] == seller_id:
                    inventory = {int(product_id): Product(**product_data) for product_id, product_data in seller_data["inventory"].items()}
                    seller = Seller(seller_data["seller_id"], seller_data["name"], inventory)
                    return seller
        except (FileNotFoundError, json.JSONDecodeError):
            return None

        raise SellerNotFoundError(seller_id)

    def update(self, seller_id: int, name: str = None, inventory: dict = None):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for seller_data in data.get("sellers", []):
                if seller_data["seller_id"] == seller_id:
                    if name:
                        seller_data["name"] = name
                    if inventory:
                        seller_data["inventory"] = {product.product_id: product.__repr__() for product in inventory.values()}
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return seller_data
        except (FileNotFoundError, json.JSONDecodeError):
            return None

        raise SellerNotFoundError(seller_id)

    def delete(self, seller_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            updated_sellers = [seller_data for seller_data in data["sellers"] if seller_data["seller_id"] != seller_id]
            if len(updated_sellers) == len(data["sellers"]):
                raise SellerNotFoundError(seller_id)

            data["sellers"] = updated_sellers

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)

            return f"Seller with ID {seller_id} deleted."
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def add_product_to_seller(self, seller_id: int, product: Product):
        seller = self.read(seller_id)
        if not seller:
            raise SellerNotFoundError(seller_id)
        seller.add_product(product)
        return self.update(seller_id, inventory=seller.inventory)

    def remove_product_from_seller(self, seller_id: int, product_id: int):
        seller = self.read(seller_id)
        if not seller:
            raise SellerNotFoundError(seller_id)
        seller.remove_product(product_id)
        return self.update(seller_id, inventory=seller.inventory)

    def update_product_stock_in_seller(self, seller_id: int, product_id: int, new_stock: int):
        seller = self.read(seller_id)
        if not seller:
            raise SellerNotFoundError(seller_id)
        seller.update_stock(product_id, new_stock)
        return self.update(seller_id, inventory=seller.inventory)

    def list_all_sellers(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            return [Seller(seller_data["seller_id"], seller_data["name"]) for seller_data in data.get("sellers", [])]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def list_seller_inventory(self, seller_id: int):
        seller = self.read(seller_id)
        if not seller:
            raise SellerNotFoundError(seller_id)
        return seller.list_inventory()
