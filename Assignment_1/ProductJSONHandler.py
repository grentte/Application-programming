import json
from Product import Product, ProductNotFoundError, InsufficientStockError


class ProductExistsError(Exception):
    pass


class ProductJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, product: Product):
        product_data = {
            "product_id": product.product_id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "stock": product.stock
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"products": []}

        for existing_product in data.get("products", []):
            if existing_product["product_id"] == product.product_id:
                raise ProductExistsError(f"Product with ID '{product.product_id}' already exists.")

        data["products"].append(product_data)

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, product_id: int) -> Product:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for product_data in data.get("products", []):
                if product_data["product_id"] == product_id:
                    return Product(
                        product_data["product_id"],
                        product_data["name"],
                        product_data["category"],
                        product_data["price"],
                        product_data["stock"]
                    )
        except (FileNotFoundError, json.JSONDecodeError):
            return None

        raise ProductNotFoundError(product_id)

    def update(self, product_id: int, name: str = None, category: str = None, price: float = None, stock: int = None):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for product_data in data.get("products", []):
                if product_data["product_id"] == product_id:
                    if name:
                        product_data["name"] = name
                    if category:
                        product_data["category"] = category
                    if price is not None:
                        product_data["price"] = price
                    if stock is not None:
                        product_data["stock"] = stock

                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
            raise ProductNotFoundError(product_id)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def delete(self, product_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("products", []))
            data["products"] = [product for product in data.get("products", []) if product["product_id"] != product_id]

            if len(data["products"]) == original_length:
                raise ProductNotFoundError(product_id)

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except ProductNotFoundError as e:
            print(e)
            return False

    def get_all_products(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            return [
                Product(
                    product_data["product_id"],
                    product_data["name"],
                    product_data["category"],
                    product_data["price"],
                    product_data["stock"]
                )
                for product_data in data.get("products", [])
            ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def update_stock(self, product_id: int, quantity: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for product_data in data.get("products", []):
                if product_data["product_id"] == product_id:
                    if product_data["stock"] + quantity < 0:
                        raise InsufficientStockError(
                            product_data["name"], product_data["stock"], quantity
                        )
                    product_data["stock"] += quantity
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return f"Stock updated for product '{product_data['name']}'. New stock: {product_data['stock']}"
            raise ProductNotFoundError(product_id)
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except InsufficientStockError as e:
            return str(e)

    def update_price(self, product_id: int, new_price: float):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for product_data in data.get("products", []):
                if product_data["product_id"] == product_id:
                    if new_price < 0:
                        raise ValueError("Price cannot be negative.")
                    product_data["price"] = new_price
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return f"Price for product '{product_data['name']}' updated to {new_price}"
            raise ProductNotFoundError(product_id)
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except ValueError as e:
            return str(e)
