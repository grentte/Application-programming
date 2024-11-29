class InsufficientStockError(Exception):
    def __init__(self, product_name: str, current_stock: int, requested_change: int):
        message = (f"Insufficient stock for product '{product_name}'. "
                   f"Current stock: {current_stock}, requested change: {requested_change}.")
        super().__init__(message)


class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        super().__init__(f"Product with ID {product_id} not found.")


class Product:
    def __init__(self, product_id: int, name: str, category: str, price: float, stock: int):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def __repr__(self):
        return (f"Product(product_id={self.product_id}, name='{self.name}', category='{self.category}', "
                f"price={self.price}, stock={self.stock})")

    def update_price(self, new_price: float):
        if new_price < 0:
            raise ValueError("Price cannot be negative.")
        self.price = new_price
        return f"Price for {self.name} updated to {self.price}"

    def check_availability(self):
        return self.stock > 0

    def update_stock(self, quantity: int):
        if self.stock + quantity < 0:
            raise InsufficientStockError(self.name, self.stock, quantity)
        self.stock += quantity
        return f"Stock updated for {self.name}. New stock: {self.stock}"


class ProductManager:
    def __init__(self):
        self.products = {}

    def create_product(self, name: str, category: str, price: float, stock: int):
        if not name or not category:
            raise ValueError("Name and category cannot be empty.")
        product_id = len(self.products) + 1
        product = Product(product_id, name, category, price, stock)
        self.products[product_id] = product
        return product

    def read_product_by_id(self, product_id: int):
        product = self.products.get(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product

    def update_product(self, product_id: int, name: str = None, category: str = None, price: float = None, stock: int = None):
        try:
            product = self.read_product_by_id(product_id)
        except ProductNotFoundError as e:
            return str(e)

        if name:
            product.name = name
        if category:
            product.category = category
        if price is not None:
            product.update_price(price)
        if stock is not None:
            product.update_stock(stock)
        return product

    def delete_product(self, product_id: int):
        try:
            product = self.read_product_by_id(product_id)
            del self.products[product_id]
            return f"Product {product_id} deleted successfully."
        except ProductNotFoundError as e:
            return str(e)

    def get_all_products(self):
        return list(self.products.values())

    def update_stock(self, product_id: int, quantity: int):
        try:
            product = self.read_product_by_id(product_id)
            return product.update_stock(quantity)
        except (ProductNotFoundError, InsufficientStockError) as e:
            return str(e)

    def update_price(self, product_id: int, new_price: float):
        try:
            product = self.read_product_by_id(product_id)
            return product.update_price(new_price)
        except (ProductNotFoundError, ValueError) as e:
            return str(e)
