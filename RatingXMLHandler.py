import xml.etree.ElementTree as ET
from Product import Product
from Rating import Rating, InvalidRatingError


class RatingXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _load_ratings(self):
        try:
            tree = ET.parse(self.filepath)
            return tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("ratings")
            tree = ET.ElementTree(root)
            tree.write(self.filepath)
            return root

    def _save_ratings(self, root):
        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def create_rating(self, product: Product):
        root = self._load_ratings()

        # Check if the product already has a rating in XML
        for rating_element in root.findall("rating"):
            if int(rating_element.find("product_id").text) == product.product_id:
                raise ValueError(f"Product '{product.name}' already has a rating.")

        # Create a new rating object and corresponding XML element
        rating = Rating(product)
        rating_element = ET.SubElement(root, "rating")
        ET.SubElement(rating_element, "product_id").text = str(product.product_id)
        ET.SubElement(rating_element, "total_reviews").text = str(rating.total_reviews)
        ET.SubElement(rating_element, "average_rating").text = str(rating.average_rating)

        self._save_ratings(root)
        return rating

    def read_rating_by_product_id(self, product_id: int):
        root = self._load_ratings()

        for rating_element in root.findall("rating"):
            if int(rating_element.find("product_id").text) == product_id:
                product_name = rating_element.find("product_name").text
                total_reviews = int(rating_element.find("total_reviews").text)
                average_rating = float(rating_element.find("average_rating").text)

                product = Product(product_id, product_name, "Category", 0.0, 0)
                rating = Rating(product)
                rating.total_reviews = total_reviews
                rating.average_rating = average_rating
                return rating

        raise ValueError(f"No rating found for product ID {product_id}.")

    def update_rating(self, product_id: int, new_rating: int):
        root = self._load_ratings()

        for rating_element in root.findall("rating"):
            if int(rating_element.find("product_id").text) == product_id:
                rating = Rating(Product(product_id, "Product Name", "Category", 0.0, 0))
                current_reviews = int(rating_element.find("total_reviews").text)
                current_average_rating = float(rating_element.find("average_rating").text)

                rating.total_reviews = current_reviews
                rating.average_rating = current_average_rating

                rating.update_rating(new_rating)

                rating_element.find("total_reviews").text = str(rating.total_reviews)
                rating_element.find("average_rating").text = str(rating.average_rating)

                self._save_ratings(root)
                return rating

        raise ValueError(f"No rating found for product ID {product_id}.")

    def reset_rating(self, product_id: int):
        root = self._load_ratings()

        for rating_element in root.findall("rating"):
            if int(rating_element.find("product_id").text) == product_id:
                rating = Rating(Product(product_id, "Product Name", "Category", 0.0, 0))

                rating.reset_rating()

                rating_element.find("total_reviews").text = str(rating.total_reviews)
                rating_element.find("average_rating").text = str(rating.average_rating)

                self._save_ratings(root)
                return rating

        raise ValueError(f"No rating found for product ID {product_id}.")

    def delete_rating(self, product_id: int):
        root = self._load_ratings()

        for rating_element in root.findall("rating"):
            if int(rating_element.find("product_id").text) == product_id:
                root.remove(rating_element)
                self._save_ratings(root)
                return f"Rating for product ID {product_id} deleted."

        raise ValueError(f"No rating found for product ID {product_id}.")
