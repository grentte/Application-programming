from Product import Product


class Category:
    def __init__(self, category_id: int, name: str, description: str):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.products = []

    def __repr__(self):
        return f"Category(category_id={self.category_id}, name='{self.name}', description='{self.description}')"

    def add_product_to_category(self, product: Product):
        self.products.append(product)
        return f"Product {product.name} added to category {self.name}."

    def remove_product_from_category(self, product: Product):
        self.products.remove(product)
        return f"Product {product.name} removed from category {self.name}."

    def list_products(self):
        return [product.name for product in self.products]


class CategoryManager:
    def __init__(self):
        self.categories = {}  # Словарь для хранения категорий, ключ - category_id

    def create_category(self, name: str, description: str):
        category_id = len(self.categories) + 1  # Генерация уникального ID для категории
        category = Category(category_id, name, description)
        self.categories[category_id] = category
        return category

    def read_category_by_id(self, category_id: int):
        return self.categories.get(category_id, "Category not found.")

    def update_category(self, category_id: int, name: str = None, description: str = None):
        category = self.categories.get(category_id)
        if category:
            if name:
                category.name = name
            if description:
                category.description = description
            return category
        return "Category not found."

    def delete_category(self, category_id: int):
        category = self.categories.get(category_id)
        if category:
            del self.categories[category_id]
            return f"Category {category_id} deleted successfully."
        return "Category not found."

    def get_all_categories(self):
        return [category for category in self.categories.values()]

    def add_product_to_category(self, category_id: int, product: Product):
        category = self.categories.get(category_id)
        if category:
            return category.add_product_to_category(product)
        return "Category not found."

    def remove_product_from_category(self, category_id: int, product: Product):
        category = self.categories.get(category_id)
        if category:
            return category.remove_product_from_category(product)
        return "Category not found."