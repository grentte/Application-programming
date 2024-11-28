class Product:
    def __init__(self, product_id, name, category, price, stock):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f"Product(product_id={self.product_id}, name='{self.name}', category='{self.category}', price={self.price}, stock={self.stock})"

    def update_price(self, new_price):
        self.price = new_price
        return f"Price for {self.name} updated to {self.price}"

    def check_availability(self):
        return self.stock > 0

    def update_stock(self, quantity):
        self.stock += quantity
        return f"Stock updated for {self.name}. New stock: {self.stock}"


class ProductManager:
    pass

