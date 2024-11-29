import xml.etree.ElementTree as ET
from Product import Product
from Rating import Rating, InvalidRatingError
from Review import Review, ReviewNotFoundError


class ReviewXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _load_reviews(self):
        try:
            tree = ET.parse(self.filepath)
            return tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("reviews")
            tree = ET.ElementTree(root)
            tree.write(self.filepath)
            return root

    def _save_reviews(self, root):
        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def create_review(self, user_id: int, product: Product, rating_value: int, comment: str):
        if rating_value < 1 or rating_value > 5:
            raise InvalidRatingError(rating_value)

        rating = Rating(product)
        rating.update_rating(rating_value)

        root = self._load_reviews()
        review_id = len(root.findall("review")) + 1
        review = Review(review_id, user_id, product, rating, comment)

        review_element = ET.SubElement(root, "review")
        ET.SubElement(review_element, "review_id").text = str(review.review_id)
        ET.SubElement(review_element, "user_id").text = str(review.user_id)
        ET.SubElement(review_element, "product_id").text = str(product.product_id)
        ET.SubElement(review_element, "rating").text = str(rating_value)
        ET.SubElement(review_element, "comment").text = comment

        self._save_reviews(root)
        return review

    def get_review(self, review_id: int):
        root = self._load_reviews()

        for review_element in root.findall("review"):
            if int(review_element.find("review_id").text) == review_id:
                product_id = int(review_element.find("product_id").text)
                product = Product(product_id, "Placeholder Product", "Category", 0.0, 0)
                user_id = int(review_element.find("user_id").text)
                rating_value = int(review_element.find("rating").text)
                comment = review_element.find("comment").text
                rating = Rating(product)
                rating.update_rating(rating_value)

                return Review(review_id, user_id, product, rating, comment)

        raise ReviewNotFoundError(review_id)

    def get_reviews_for_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Invalid product. Must be an instance of Product.")
        root = self._load_reviews()

        reviews = []
        for review_element in root.findall("review"):
            if int(review_element.find("product_id").text) == product.product_id:
                review_id = int(review_element.find("review_id").text)
                user_id = int(review_element.find("user_id").text)
                rating_value = int(review_element.find("rating").text)
                comment = review_element.find("comment").text
                rating = Rating(product)
                rating.update_rating(rating_value)

                reviews.append(Review(review_id, user_id, product, rating, comment))

        return reviews

    def get_reviews_by_user(self, user_id: int):
        root = self._load_reviews()

        reviews = []
        for review_element in root.findall("review"):
            if int(review_element.find("user_id").text) == user_id:
                review_id = int(review_element.find("review_id").text)
                product_id = int(review_element.find("product_id").text)
                product = Product(product_id, "Placeholder Product", "Category", 0.0, 0)
                rating_value = int(review_element.find("rating").text)
                comment = review_element.find("comment").text
                rating = Rating(product)
                rating.update_rating(rating_value)

                reviews.append(Review(review_id, user_id, product, rating, comment))

        return reviews

    def update_review(self, review_id: int, new_comment: str = None, new_rating_value: int = None):
        root = self._load_reviews()

        for review_element in root.findall("review"):
            if int(review_element.find("review_id").text) == review_id:
                if new_comment:
                    review_element.find("comment").text = new_comment
                if new_rating_value is not None:
                    review_element.find("rating").text = str(new_rating_value)

                self._save_reviews(root)
                return f"Review {review_id} updated."

        raise ReviewNotFoundError(review_id)

    def delete_review(self, review_id: int):
        root = self._load_reviews()

        for review_element in root.findall("review"):
            if int(review_element.find("review_id").text) == review_id:
                root.remove(review_element)
                self._save_reviews(root)
                return f"Review {review_id} deleted."

        raise ReviewNotFoundError(review_id)

    def list_all_reviews(self):
        root = self._load_reviews()
        reviews = []
        for review_element in root.findall("review"):
            review_id = int(review_element.find("review_id").text)
            user_id = int(review_element.find("user_id").text)
            product_id = int(review_element.find("product_id").text)
            product = Product(product_id, "Placeholder Product", "Category", 0.0, 0)
            rating_value = int(review_element.find("rating").text)
            comment = review_element.find("comment").text
            rating = Rating(product)
            rating.update_rating(rating_value)

            reviews.append(Review(review_id, user_id, product, rating, comment))

        return reviews
