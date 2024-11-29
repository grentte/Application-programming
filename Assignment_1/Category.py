from Product import Product, ProductNotFoundError


class Category:
    def __init__(self, category_id: int, name: str, description: str):
        if not name:
            raise ValueError("Category name cannot be empty.")
        self.category_id = category_id
        self.name = name
        self.description = description
        self.products = []

    def __repr__(self):
        return f"Category(category_id={self.category_id}, name='{self.name}', description='{self.description}')"

    def add_product_to_category(self, product: Product):
        if product in self.products:
            raise ValueError(f"Product {product.name} is already in category {self.name}.")
        self.products.append(product)
        return f"Product {product.name} added to category {self.name}."

    def remove_product_from_category(self, product: Product):
        if product not in self.products:
            raise ProductNotFoundError(product.product_id, self.name)
        self.products.remove(product)
        return f"Product {product.name} removed from category {self.name}."

    def list_products(self):
        if not self.products:
            return f"No products in category {self.name}."
        return [product.name for product in self.products]


class CategoryNotFoundError(Exception):
    def __init__(self, category_id: int):
        super().__init__(f"Category with ID {category_id} not found.")


class CategoryManager:
    def __init__(self):
        self.categories = {}  # Dictionary to store categories, key is category_id

    def create_category(self, name: str, description: str):
        if not name:
            raise ValueError("Category name cannot be empty.")
        category_id = len(self.categories) + 1  # Generate a unique ID for the category
        category = Category(category_id, name, description)
        self.categories[category_id] = category
        return category

    def read_category_by_id(self, category_id: int):
        category = self.categories.get(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)
        return category

    def update_category(self, category_id: int, name: str = None, description: str = None):
        try:
            category = self.read_category_by_id(category_id)
        except CategoryNotFoundError as e:
            return str(e)

        if name:
            category.name = name
        if description:
            category.description = description
        return category

    def delete_category(self, category_id: int):
        try:
            category = self.read_category_by_id(category_id)
            del self.categories[category_id]
            return f"Category {category_id} deleted successfully."
        except CategoryNotFoundError as e:
            return str(e)

    def get_all_categories(self):
        return [category for category in self.categories.values()]

    def add_product_to_category(self, category_id: int, product: Product):
        try:
            category = self.read_category_by_id(category_id)
            return category.add_product_to_category(product)
        except (CategoryNotFoundError, ValueError) as e:
            return str(e)

    def remove_product_from_category(self, category_id: int, product: Product):
        try:
            category = self.read_category_by_id(category_id)
            return category.remove_product_from_category(product)
        except (CategoryNotFoundError, ProductNotFoundError) as e:
            return str(e)
