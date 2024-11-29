import json
from typing import Optional
from Product import Product, ProductNotFoundError
from Category import Category, CategoryNotFoundError


class CategoryJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create_category(self, name: str, description: str) -> Category:
        category_data = {
            "name": name,
            "description": description,
            "products": []  # Empty list to store products initially
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"categories": []}

        category_id = len(data["categories"]) + 1  # Generate unique ID for new category
        category_data["category_id"] = category_id
        data["categories"].append(category_data)

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

        return Category(category_id, name, description)

    def read_category_by_id(self, category_id: int) -> Optional[Category]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for category_data in data.get("categories", []):
                if category_data["category_id"] == category_id:
                    category = Category(
                        category_data["category_id"],
                        category_data["name"],
                        category_data["description"]
                    )
                    # Rebuild the product objects from the stored data
                    category.products = [
                        Product(prod["product_id"], prod["name"], prod["price"], prod["stock"])
                        for prod in category_data.get("products", [])
                    ]
                    return category
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update_category(self, category_id: int, name: str = None, description: str = None) -> str:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for category_data in data["categories"]:
                if category_data["category_id"] == category_id:
                    if name:
                        category_data["name"] = name
                    if description:
                        category_data["description"] = description

                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return f"Category {category_id} updated successfully."
            raise CategoryNotFoundError(category_id)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return str(e)

    def delete_category(self, category_id: int) -> str:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            original_length = len(data["categories"])
            data["categories"] = [cat for cat in data["categories"] if cat["category_id"] != category_id]

            if len(data["categories"]) == original_length:
                raise CategoryNotFoundError(category_id)

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)

            return f"Category {category_id} deleted successfully."
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return str(e)
        except CategoryNotFoundError as e:
            return str(e)

    def add_product_to_category(self, category_id: int, product: Product) -> str:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for category_data in data["categories"]:
                if category_data["category_id"] == category_id:
                    product_data = {
                        "product_id": product.product_id,
                        "name": product.name,
                        "price": product.price,
                        "stock": product.stock
                    }
                    if product_data not in category_data["products"]:
                        category_data["products"].append(product_data)
                    else:
                        return f"Product {product.name} already in category {category_data['name']}."

                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return f"Product {product.name} added to category {category_data['name']}."
            raise CategoryNotFoundError(category_id)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return str(e)

    def remove_product_from_category(self, category_id: int, product: Product) -> str:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for category_data in data["categories"]:
                if category_data["category_id"] == category_id:
                    product_data = {
                        "product_id": product.product_id,
                        "name": product.name,
                        "price": product.price,
                        "stock": product.stock
                    }
                    if product_data in category_data["products"]:
                        category_data["products"].remove(product_data)

                        with open(self.filepath, "w") as file:
                            json.dump(data, file, indent=4)
                        return f"Product {product.name} removed from category {category_data['name']}."
                    else:
                        return f"Product {product.name} not found in category {category_data['name']}."
            raise CategoryNotFoundError(category_id)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return str(e)

    def get_all_categories(self) -> list:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            return [
                Category(
                    category_data["category_id"],
                    category_data["name"],
                    category_data["description"]
                ) for category_data in data.get("categories", [])
            ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
