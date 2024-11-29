import xml.etree.ElementTree as ET
from typing import Optional
from Product import Product  # Assuming Product class is defined elsewhere
from Cart import Cart  # Assuming Cart class is defined elsewhere

class CartExistsError(Exception):
    pass

class CartNotFoundError(Exception):
    pass

class CartXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, cart: Cart):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("carts")

        # Check if the cart already exists by cart_id
        for cart_element in root.findall("cart"):
            if cart_element.find("cart_id").text == str(cart.cart_id):
                raise CartExistsError(f"Cart with ID '{cart.cart_id}' already exists.")

        cart_element = ET.SubElement(root, "cart")
        ET.SubElement(cart_element, "cart_id").text = str(cart.cart_id)
        ET.SubElement(cart_element, "user_id").text = str(cart.user_id)

        products_element = ET.SubElement(cart_element, "products")
        for product, quantity in cart.products.items():
            product_element = ET.SubElement(products_element, "product")
            ET.SubElement(product_element, "product_id").text = str(product.product_id)
            ET.SubElement(product_element, "quantity").text = str(quantity)

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, cart_id: int) -> Optional[Cart]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for cart_element in root.findall("cart"):
                if int(cart_element.find("cart_id").text) == cart_id:
                    user_id = int(cart_element.find("user_id").text)
                    cart = Cart(user_id, cart_id)

                    # Load products from XML
                    for product_element in cart_element.find("products").findall("product"):
                        product_id = int(product_element.find("product_id").text)
                        quantity = int(product_element.find("quantity").text)
                        product = Product.get_product_by_id(product_id)  # Assuming a method in Product class to get products
                        if product:
                            cart.products[product] = quantity

                    return cart
        except (FileNotFoundError, ET.ParseError):
            return None
        return None

    def update(self, cart_id: int, product: Product, quantity: int, action: str) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for cart_element in root.findall("cart"):
                if int(cart_element.find("cart_id").text) == cart_id:
                    products_element = cart_element.find("products")

                    # Perform action based on the request
                    if action == "add":
                        # Check if product exists, then update the quantity
                        for product_element in products_element.findall("product"):
                            if int(product_element.find("product_id").text) == product.product_id:
                                current_quantity = int(product_element.find("quantity").text)
                                product_element.find("quantity").text = str(current_quantity + quantity)
                                tree.write(self.filepath)
                                return True

                        # If product is not already in the cart, add it
                        product_element = ET.SubElement(products_element, "product")
                        ET.SubElement(product_element, "product_id").text = str(product.product_id)
                        ET.SubElement(product_element, "quantity").text = str(quantity)
                        tree.write(self.filepath)
                        return True

                    elif action == "remove":
                        # Remove product from the cart
                        for product_element in products_element.findall("product"):
                            if int(product_element.find("product_id").text) == product.product_id:
                                products_element.remove(product_element)
                                tree.write(self.filepath)
                                return True

            raise CartNotFoundError(f"Cart with ID '{cart_id}' not found.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except CartNotFoundError as e:
            print(e)
            return False

    def delete(self, cart_id: int) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for cart_element in root.findall("cart"):
                if int(cart_element.find("cart_id").text) == cart_id:
                    root.remove(cart_element)
                    tree.write(self.filepath)
                    return True

            raise CartNotFoundError(f"Cart with ID '{cart_id}' not found for deletion.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except CartNotFoundError as e:
            print(e)
            return False

    def get_all_carts(self):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            carts = []
            for cart_element in root.findall("cart"):
                cart_id = int(cart_element.find("cart_id").text)
                user_id = int(cart_element.find("user_id").text)
                cart = Cart(user_id, cart_id)

                # Load products from XML
                for product_element in cart_element.find("products").findall("product"):
                    product_id = int(product_element.find("product_id").text)
                    quantity = int(product_element.find("quantity").text)
                    product = Product.get_product_by_id(product_id)  # Assuming a method in Product class to get products
                    if product:
                        cart.products[product] = quantity

                carts.append(cart)

            return carts
        except (FileNotFoundError, ET.ParseError):
            return []
