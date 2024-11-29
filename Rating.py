from Product import Product


class InvalidRatingError(Exception):
    def __init__(self, rating_value):
        super().__init__(f"Invalid rating value: {rating_value}. Rating must be between 1 and 5.")


class Rating:
    def __init__(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Invalid product. Must be an instance of Product.")
        self.product = product
        self.total_reviews = 0
        self.average_rating = 0.0

    def __repr__(self):
        return (f"Rating(product='{self.product.name}', "
                f"total_reviews={self.total_reviews}, average_rating={self.average_rating:.1f})")

    def update_rating(self, new_rating: int):
        if not (1 <= new_rating <= 5):
            raise InvalidRatingError(new_rating)
        self.total_reviews += 1
        self.average_rating = ((self.average_rating * (self.total_reviews - 1)) + new_rating) / self.total_reviews
        return f"New average rating for {self.product.name}: {self.average_rating:.1f}"

    def reset_rating(self):
        self.total_reviews = 0
        self.average_rating = 0.0
        return f"Rating for {self.product.name} has been reset."
