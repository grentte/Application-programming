import xml.etree.ElementTree as ET
from Cart import Cart
from Address import Address
from Order import Order, OrderNotFoundError
from Product import Product


class OrderXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _load_orders(self):
        try:
            tree = ET.parse(self.filepath)
            return tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("orders")
            tree = ET.ElementTree(root)
            tree.write(self.filepath)
            return root

    def _save_orders(self, root):
        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def create_order(self, user_id: int, cart: Cart, address: Address, payment_method: str):
        if not address:
            raise ValueError("Address cannot be empty.")
        if not payment_method:
            raise ValueError("Payment method is required.")

        root = self._load_orders()

        order_id = len(root.findall("order")) + 1
        order = Order(order_id, user_id, cart, address, payment_method)

        # Create new order XML element
        order_element = ET.SubElement(root, "order")
        ET.SubElement(order_element, "order_id").text = str(order.order_id)
        ET.SubElement(order_element, "user_id").text = str(order.user_id)
        ET.SubElement(order_element, "total_amount").text = str(order.total_amount)
        ET.SubElement(order_element, "status").text = order.status
        ET.SubElement(order_element, "payment_method").text = order.payment_method
        ET.SubElement(order_element, "address").text = str(order.address)

        # Adding cart items to the XML
        cart_element = ET.SubElement(order_element, "cart")
        for product, quantity in cart.products.items():
            product_element = ET.SubElement(cart_element, "product")
            ET.SubElement(product_element, "product_id").text = str(product.product_id)
            ET.SubElement(product_element, "name").text = product.name
            ET.SubElement(product_element, "price").text = str(product.price)
            ET.SubElement(product_element, "quantity").text = str(quantity)

        self._save_orders(root)
        return order

    def read_order_by_id(self, order_id: int):
        root = self._load_orders()

        for order_element in root.findall("order"):
            if int(order_element.find("order_id").text) == order_id:
                user_id = int(order_element.find("user_id").text)
                total_amount = float(order_element.find("total_amount").text)
                status = order_element.find("status").text
                payment_method = order_element.find("payment_method").text
                address = order_element.find("address").text  # Assuming Address class is properly handled

                # Retrieve cart items
                cart = Cart(user_id, order_id)
                cart_element = order_element.find("cart")
                for product_element in cart_element.findall("product"):
                    product_id = int(product_element.find("product_id").text)
                    name = product_element.find("name").text
                    price = float(product_element.find("price").text)
                    quantity = int(product_element.find("quantity").text)

                    product = Product(product_id, name, price, quantity)
                    cart.add_to_cart(product, quantity)

                return Order(order_id, user_id, cart, Address(address), payment_method)

        raise OrderNotFoundError(order_id)

    def update_order(self, order_id: int, status: str = None, address: Address = None, payment_method: str = None):
        root = self._load_orders()

        for order_element in root.findall("order"):
            if int(order_element.find("order_id").text) == order_id:
                if status:
                    if status not in ["Pending", "Placed", "Cancelled", "Completed"]:
                        raise ValueError("Invalid status value.")
                    order_element.find("status").text = status
                if address:
                    order_element.find("address").text = str(address)
                if payment_method:
                    order_element.find("payment_method").text = payment_method

                self._save_orders(root)
                return self.read_order_by_id(order_id)

        raise OrderNotFoundError(order_id)

    def delete_order(self, order_id: int):
        root = self._load_orders()

        for order_element in root.findall("order"):
            if int(order_element.find("order_id").text) == order_id:
                root.remove(order_element)
                self._save_orders(root)
                return f"Order {order_id} deleted."

        raise OrderNotFoundError(order_id)

    def get_all_orders(self):
        root = self._load_orders()
        orders = []
        for order_element in root.findall("order"):
            order_id = int(order_element.find("order_id").text)
            orders.append(self.read_order_by_id(order_id))
        return orders

    def get_orders_by_user(self, user_id: int):
        root = self._load_orders()
        orders = []
        for order_element in root.findall("order"):
            if int(order_element.find("user_id").text) == user_id:
                order_id = int(order_element.find("order_id").text)
                orders.append(self.read_order_by_id(order_id))
        if not orders:
            raise ValueError(f"No orders found for user ID {user_id}.")
        return orders