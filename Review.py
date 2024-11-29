from Product import Product
from Rating import Rating, InvalidRatingError


class ReviewNotFoundError(Exception):
    def __init__(self, review_id):
        super().__init__(f"Review with ID {review_id} not found.")


class Review:
    def __init__(self, review_id: int, user_id: int, product: Product, rating: Rating, comment: str):
        if not comment:
            raise ValueError("Comment cannot be empty.")
        if not isinstance(product, Product):
            raise TypeError("Invalid product. Must be an instance of Product.")
        if not isinstance(rating, Rating):
            raise TypeError("Invalid rating. Must be an instance of Rating.")
        self.review_id = review_id
        self.user_id = user_id
        self.product = product
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return (f"Review(review_id={self.review_id}, user_id={self.user_id}, "
                f"product='{self.product.name}', rating={self.rating}, comment='{self.comment}')")

    def edit_review(self, new_comment: str, new_rating: Rating):
        if not new_comment:
            raise ValueError("New comment cannot be empty.")
        if not isinstance(new_rating, Rating):
            raise TypeError("Invalid rating. Must be an instance of Rating.")
        self.comment = new_comment
        self.rating = new_rating
        return f"Review for {self.product.name} updated."

    def delete_review(self):
        return f"Review for {self.product.name} deleted."


class ReviewManager:
    def __init__(self):
        self.reviews = {}
        self.current_review_id = 1

    def add_review(self, user_id: int, product: Product, rating_value: int, comment: str):
        if rating_value < 1 or rating_value > 5:
            raise InvalidRatingError(rating_value)
        rating = Rating(product)
        rating.update_rating(rating_value)
        review = Review(self.current_review_id, user_id, product, rating, comment)
        self.reviews[self.current_review_id] = review
        self.current_review_id += 1
        return review

    def get_review(self, review_id: int):
        review = self.reviews.get(review_id)
        if not review:
            raise ReviewNotFoundError(review_id)
        return review

    def get_reviews_for_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Invalid product. Must be an instance of Product.")
        return [review for review in self.reviews.values() if review.product == product]

    def get_reviews_by_user(self, user_id: int):
        return [review for review in self.reviews.values() if review.user_id == user_id]

    def update_review(self, review_id: int, new_comment: str = None, new_rating_value: int = None):
        try:
            review = self.get_review(review_id)
        except ReviewNotFoundError as e:
            return str(e)

        if new_comment:
            if not new_comment.strip():
                raise ValueError("Comment cannot be empty.")
            review.comment = new_comment
        if new_rating_value is not None:
            if new_rating_value < 1 or new_rating_value > 5:
                raise InvalidRatingError(new_rating_value)
            review.rating.update_rating(new_rating_value)
        return review

    def delete_review(self, review_id: int):
        try:
            review = self.get_review(review_id)
            del self.reviews[review_id]
            return f"Review {review_id} for product {review.product.name} deleted."
        except ReviewNotFoundError as e:
            return str(e)

    def list_all_reviews(self):
        return list(self.reviews.values())
