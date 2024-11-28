class Review:
    def __init__(self, review_id, user_id, product, rating, comment):
        self.review_id = review_id
        self.user_id = user_id
        self.product = product
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return f"Review(review_id={self.review_id}, user_id={self.user_id}, product='{self.product.name}', rating={self.rating}, comment='{self.comment}')"

    def add_review(self):
        return f"Review added for {self.product.name}: {self.comment}"

    def edit_review(self, new_comment, new_rating):
        self.comment = new_comment
        self.rating = new_rating
        return f"Review for {self.product.name} updated."

    def delete_review(self):
        return f"Review for {self.product.name} deleted."

class ReviewManager:
    pass

