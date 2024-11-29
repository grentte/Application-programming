import json
from typing import Optional
from Review import Review
from Product import Product
from Rating import Rating


class ReviewExistsError(Exception):
    pass


class ReviewNotFoundError(Exception):
    pass


class ReviewJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, review: Review):
        review_data = {
            "review_id": review.review_id,
            "user_id": review.user_id,
            "product": {
                "product_id": review.product.product_id,
                "name": review.product.name,
                "price": review.product.price,
                "stock": review.product.stock,
            },
            "rating": review.rating.average_rating,
            "comment": review.comment,
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"reviews": []}

        for existing_review in data.get("reviews", []):
            if existing_review["review_id"] == review.review_id:
                raise ReviewExistsError(f"Review with ID {review.review_id} already exists.")

        data["reviews"].append(review_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, review_id: int) -> Optional[Review]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for review_data in data.get("reviews", []):
                if review_data["review_id"] == review_id:
                    product_data = review_data["product"]
                    product = Product(
                        product_id=product_data["product_id"],
                        name=product_data["name"],
                        price=product_data["price"],
                        stock=product_data["stock"],
                    )
                    rating = Rating(product)
                    rating.average_rating = review_data["rating"]
                    return Review(
                        review_id=review_data["review_id"],
                        user_id=review_data["user_id"],
                        product=product,
                        rating=rating,
                        comment=review_data["comment"],
                    )
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update(self, review_id: int, new_comment: str = None, new_rating: float = None):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for review_data in data.get("reviews", []):
                if review_data["review_id"] == review_id:
                    if new_comment:
                        review_data["comment"] = new_comment
                    if new_rating is not None:
                        review_data["rating"] = new_rating
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
            raise ReviewNotFoundError(f"Review with ID {review_id} not found for update.")
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except ReviewNotFoundError as e:
            print(e)
            return False

    def delete(self, review_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("reviews", []))
            data["reviews"] = [review for review in data.get("reviews", []) if review["review_id"] != review_id]

            if len(data["reviews"]) == original_length:
                raise ReviewNotFoundError(f"Review with ID {review_id} not found for deletion.")

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except ReviewNotFoundError as e:
            print(e)
            return False
