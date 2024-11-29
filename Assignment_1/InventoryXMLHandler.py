import xml.etree.ElementTree as ET
from typing import Optional
from Product import Product, ProductNotFoundError
from Inventory import Inventory

class InventoryNotFoundError(Exception):
    pass

class InventoryXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create_inventory(self, seller_id: int):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("inventories")

        # Check if inventory already exists
        for inventory_element in root.findall("inventory"):
            if inventory_element.find("seller_id").text == str(seller_id):
                raise ValueError(f"Inventory for seller ID {seller_id} already exists.")

        inventory_element = ET.SubElement(root, "inventory")
        ET.SubElement(inventory_element, "seller_id").text = str(seller_id)
        ET.SubElement(inventory_element, "products")

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

        return f"Inventory created for seller ID {seller_id}."

    def get_inventory(self, seller_id: int) -> Optional[Inventory]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for inventory_element in root.findall("inventory"):
                if int(inventory_element.find("seller_id").text) == seller_id:
                    inventory = Inventory()

                    # Load products from XML
                    products_element = inventory_element.find("products")
                    for product_element in products_element.findall("product"):
                        product_id = int(product_element.find("product_id").text)
                        name = product_element.find("name").text
                        price = float(product_element.find("price").text)
                        stock = int(product_element.find("stock").text)

                        product = Product(product_id, name, price, stock)
                        inventory.add_product(product)

                    return inventory

        except (FileNotFoundError, ET.ParseError):
            return None

        return None

    def update_inventory_stock(self, seller_id: int, product_id: int, new_stock: int):
        inventory = self.get_inventory(seller_id)
        if not inventory:
            raise InventoryNotFoundError(seller_id)

        product = inventory.products.get(product_id)
        if not product:
            raise ProductNotFoundError(product_id)

        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")

        product.stock = new_stock
        self._update_inventory_xml(seller_id, inventory)
        return f"Stock for product {product.name} updated to {new_stock}."

    def update_inventory_price(self, seller_id: int, product_id: int, new_price: float):
        inventory = self.get_inventory(seller_id)
        if not inventory:
            raise InventoryNotFoundError(seller_id)

        product = inventory.products.get(product_id)
        if not product:
            raise ProductNotFoundError(product_id)

        if new_price < 0:
            raise ValueError("Price cannot be negative.")

        product.price = new_price
        self._update_inventory_xml(seller_id, inventory)
        return f"Price for product {product.name} updated to {new_price:.2f}."

    def remove_product_from_inventory(self, seller_id: int, product_id: int):
        inventory = self.get_inventory(seller_id)
        if not inventory:
            raise InventoryNotFoundError(seller_id)

        if product_id not in inventory.products:
            raise ProductNotFoundError(product_id)

        removed_product = inventory.products.pop(product_id)
        self._update_inventory_xml(seller_id, inventory)
        return f"Product {removed_product.name} removed from inventory."

    def add_product_to_inventory(self, seller_id: int, product: Product):
        inventory = self.get_inventory(seller_id)
        if not inventory:
            raise InventoryNotFoundError(seller_id)

        if product.product_id in inventory.products:
            raise ValueError(f"Product {product.name} already exists in inventory.")

        inventory.add_product(product)
        self._update_inventory_xml(seller_id, inventory)
        return f"Product {product.name} added to inventory."

    def _update_inventory_xml(self, seller_id: int, inventory: Inventory):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            # Find the inventory by seller_id
            for inventory_element in root.findall("inventory"):
                if int(inventory_element.find("seller_id").text) == seller_id:
                    products_element = inventory_element.find("products")
                    # Clear existing products in XML
                    for product_element in products_element.findall("product"):
                        products_element.remove(product_element)

                    # Add updated products
                    for product in inventory.products.values():
                        product_element = ET.SubElement(products_element, "product")
                        ET.SubElement(product_element, "product_id").text = str(product.product_id)
                        ET.SubElement(product_element, "name").text = product.name
                        ET.SubElement(product_element, "price").text = str(product.price)
                        ET.SubElement(product_element, "stock").text = str(product.stock)

            tree.write(self.filepath)
        except (FileNotFoundError, ET.ParseError) as e:
            print(f"Error updating XML: {e}")
