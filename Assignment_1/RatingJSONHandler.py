import json
from Product import Product, ProductNotFoundError, ProductManager
from Rating import Rating, InvalidRatingError


class RatingNotFoundError(Exception):
    pass


class RatingJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, product: Product):
        rating_data = {
            "product_id": product.product_id,
            "total_reviews": 0,
            "average_rating": 0.0
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"ratings": []}

        for existing_rating in data.get("ratings", []):
            if existing_rating["product_id"] == product.product_id:
                raise RatingNotFoundError(f"Rating for product with ID '{product.product_id}' already exists.")

        data["ratings"].append(rating_data)

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, product_id: int) -> Rating:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for rating_data in data.get("ratings", []):
                if rating_data["product_id"] == product_id:
                    product = self.get_product_by_id(product_id)
                    rating = Rating(product)
                    rating.total_reviews = rating_data["total_reviews"]
                    rating.average_rating = rating_data["average_rating"]
                    return rating
        except (FileNotFoundError, json.JSONDecodeError):
            return None

        raise RatingNotFoundError(f"Rating for product with ID {product_id} not found.")

    def update(self, product_id: int, new_rating: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for rating_data in data.get("ratings", []):
                if rating_data["product_id"] == product_id:
                    product = self.get_product_by_id(product_id)
                    rating = Rating(product)
                    return rating.update_rating(new_rating)

            raise RatingNotFoundError(f"Rating for product with ID {product_id} not found.")
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except InvalidRatingError as e:
            return str(e)

    def reset(self, product_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for rating_data in data.get("ratings", []):
                if rating_data["product_id"] == product_id:
                    product = self.get_product_by_id(product_id)
                    rating = Rating(product)
                    return rating.reset_rating()

            raise RatingNotFoundError(f"Rating for product with ID {product_id} not found.")
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def get_product_by_id(self, product_id: int):
        product_manager = ProductManager()
        return product_manager.read_product_by_id(product_id)

    def get_all_ratings(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            return [
                {
                    "product_id": rating_data["product_id"],
                    "total_reviews": rating_data["total_reviews"],
                    "average_rating": rating_data["average_rating"]
                }
                for rating_data in data.get("ratings", [])
            ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

