from Product import Product
from Rating import Rating

class Review:
    def __init__(self, review_id: int, user_id: int, product: Product, rating: Rating, comment: str):
        self.review_id = review_id
        self.user_id = user_id
        self.product = product
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return f"Review(review_id={self.review_id}, user_id={self.user_id}, product='{self.product.name}', rating={self.rating}, comment='{self.comment}')"

    def add_review(self):
        return f"Review added for {self.product.name}: {self.comment}"

    def edit_review(self, new_comment: str, new_rating: Rating):
        self.comment = new_comment
        self.rating = new_rating
        return f"Review for {self.product.name} updated."

    def delete_review(self):
        return f"Review for {self.product.name} deleted."

class ReviewManager:
    def __init__(self):
        self.reviews = {}  # Словарь для хранения отзывов: ключ - review_id, значение - объект Review
        self.current_review_id = 1

    def add_review(self, user_id: int, product: Product, rating_value: int, comment: str):
        """Добавить новый отзыв."""
        rating = Rating(product)
        rating.update_rating(rating_value)
        review = Review(self.current_review_id, user_id, product, rating, comment)
        self.reviews[self.current_review_id] = review
        self.current_review_id += 1
        return review

    def get_review(self, review_id: int):
        """Получить отзыв по его ID."""
        return self.reviews.get(review_id, "Review not found.")

    def get_reviews_for_product(self, product: Product):
        """Получить все отзывы для определенного продукта."""
        return [review for review in self.reviews.values() if review.product == product]

    def get_reviews_by_user(self, user_id: int):
        """Получить все отзывы от определенного пользователя."""
        return [review for review in self.reviews.values() if review.user_id == user_id]

    def update_review(self, review_id: int, new_comment: str = None, new_rating_value: int = None):
        """Обновить отзыв."""
        review = self.reviews.get(review_id)
        if review:
            if new_comment:
                review.comment = new_comment
            if new_rating_value is not None:
                review.rating.update_rating(new_rating_value)
            return review
        return "Review not found."

    def delete_review(self, review_id: int):
        """Удалить отзыв."""
        review = self.reviews.pop(review_id, None)
        if review:
            return f"Review {review_id} for product {review.product.name} deleted."
        return "Review not found."

    def list_all_reviews(self):
        """Список всех отзывов."""
        return list(self.reviews.values())


