class Category:
    def __init__(self, category_id, name, description):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.products = []

    def __repr__(self):
        return f"Category(category_id={self.category_id}, name='{self.name}', description='{self.description}')"

    def add_product_to_category(self, product):
        self.products.append(product)
        return f"Product {product.name} added to category {self.name}."

    def remove_product_from_category(self, product):
        self.products.remove(product)
        return f"Product {product.name} removed from category {self.name}."

    def list_products(self):
        return [product.name for product in self.products]

class CategoryManager:
    pass

