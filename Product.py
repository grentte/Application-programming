class Product:
    def __init__(self, product_id: int, name: str, category: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f"Product(product_id={self.product_id}, name='{self.name}', category='{self.category}', price={self.price}, stock={self.stock})"

    def update_price(self, new_price: float):
        self.price = new_price
        return f"Price for {self.name} updated to {self.price}"

    def check_availability(self):
        return self.stock > 0

    def update_stock(self, quantity: int):
        self.stock += quantity
        return f"Stock updated for {self.name}. New stock: {self.stock}"


class ProductManager:
    def __init__(self):
        self.products = {}  # Словарь, где ключ - product_id, значение - объект Product

    def create_product(self, name: str, category: str, price: float, stock: int):
        product_id = len(self.products) + 1  # Генерация уникального ID для продукта
        product = Product(product_id, name, category, price, stock)
        self.products[product_id] = product
        return product

    def read_product_by_id(self, product_id: int):
        return self.products.get(product_id, "Product not found.")

    def update_product(self, product_id: int, name: str = None, category: str =None, price: float =None, stock: int =None):
        product = self.products.get(product_id)
        if product:
            if name:
                product.name = name
            if category:
                product.category = category
            if price is not None:
                product.price = price
            if stock is not None:
                product.stock = stock
            return product
        return "Product not found."

    def delete_product(self, product_id: int):
        product = self.products.get(product_id)
        if product:
            del self.products[product_id]
            return f"Product {product_id} deleted successfully."
        return "Product not found."

    def get_all_products(self):
        return list(self.products.values())

    def update_stock(self, product_id: int, quantity: int):
        product = self.products.get(product_id)
        if product:
            return product.update_stock(quantity)
        return "Product not found."

    def update_price(self, product_id: int, new_price: float):
        product = self.products.get(product_id)
        if product:
            return product.update_price(new_price)
        return "Product not found."