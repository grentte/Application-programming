from Product import Product


class Rating:
    def __init__(self, product: Product):
        self.product = product
        self.total_reviews = 0
        self.average_rating = 0.0

    def __repr__(self):
        return f"Rating(product='{self.product.name}', total_reviews={self.total_reviews}, average_rating={self.average_rating:.1f})"

    def update_rating(self, new_rating):
        self.total_reviews += 1
        self.average_rating = ((self.average_rating * (self.total_reviews - 1)) + new_rating) / self.total_reviews
        return f"New average rating for {self.product.name}: {self.average_rating:.1f}"

    def reset_rating(self):
        self.total_reviews = 0
        self.average_rating = 0.0
        return f"Rating for {self.product.name} has been reset."
