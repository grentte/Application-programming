import xml.etree.ElementTree as ET
from Product import Product, InsufficientStockError, ProductNotFoundError


class ProductXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _load_products(self):
        try:
            tree = ET.parse(self.filepath)
            return tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("products")
            tree = ET.ElementTree(root)
            tree.write(self.filepath)
            return root

    def _save_products(self, root):
        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def create_product(self, name: str, category: str, price: float, stock: int):
        if not name or not category:
            raise ValueError("Name and category cannot be empty.")

        root = self._load_products()

        product_id = len(root.findall("product")) + 1
        product = Product(product_id, name, category, price, stock)

        # Create new product XML element
        product_element = ET.SubElement(root, "product")
        ET.SubElement(product_element, "product_id").text = str(product.product_id)
        ET.SubElement(product_element, "name").text = product.name
        ET.SubElement(product_element, "category").text = product.category
        ET.SubElement(product_element, "price").text = str(product.price)
        ET.SubElement(product_element, "stock").text = str(product.stock)

        self._save_products(root)
        return product

    def read_product_by_id(self, product_id: int):
        root = self._load_products()

        for product_element in root.findall("product"):
            if int(product_element.find("product_id").text) == product_id:
                name = product_element.find("name").text
                category = product_element.find("category").text
                price = float(product_element.find("price").text)
                stock = int(product_element.find("stock").text)

                product = Product(product_id, name, category, price, stock)
                return product

        raise ProductNotFoundError(product_id)

    def update_product(self, product_id: int, name: str = None, category: str = None, price: float = None,
                       stock: int = None):
        root = self._load_products()

        for product_element in root.findall("product"):
            if int(product_element.find("product_id").text) == product_id:
                product = Product(product_id,
                                  product_element.find("name").text,
                                  product_element.find("category").text,
                                  float(product_element.find("price").text),
                                  int(product_element.find("stock").text))

                if name:
                    product.name = name
                    product_element.find("name").text = name
                if category:
                    product.category = category
                    product_element.find("category").text = category
                if price is not None:
                    product.update_price(price)
                    product_element.find("price").text = str(price)
                if stock is not None:
                    product.update_stock(stock)
                    product_element.find("stock").text = str(stock)

                self._save_products(root)
                return product

        raise ProductNotFoundError(product_id)

    def delete_product(self, product_id: int):
        root = self._load_products()

        for product_element in root.findall("product"):
            if int(product_element.find("product_id").text) == product_id:
                root.remove(product_element)
                self._save_products(root)
                return f"Product {product_id} deleted successfully."

        raise ProductNotFoundError(product_id)

    def get_all_products(self):
        root = self._load_products()
        products = []
        for product_element in root.findall("product"):
            product_id = int(product_element.find("product_id").text)
            products.append(self.read_product_by_id(product_id))
        return products

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
