import xml.etree.ElementTree as ET
from Inventory import Inventory
from Product import Product, ProductNotFoundError
from Seller import Seller, SellerNotFoundError


class SellerXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _load_sellers(self):
        try:
            tree = ET.parse(self.filepath)
            return tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("sellers")
            tree = ET.ElementTree(root)
            tree.write(self.filepath)
            return root

    def _save_sellers(self, root):
        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def create_seller(self, name: str, inventory: Inventory = None):
        if not name:
            raise ValueError("Seller name cannot be empty.")

        # Create a new Seller object
        root = self._load_sellers()
        seller_id = len(root.findall("seller")) + 1  # Generate new seller ID
        seller = Seller(seller_id=seller_id, name=name, inventory=inventory)

        # Create XML structure for the seller
        seller_element = ET.SubElement(root, "seller")
        ET.SubElement(seller_element, "seller_id").text = str(seller.seller_id)
        ET.SubElement(seller_element, "name").text = seller.name

        inventory_element = ET.SubElement(seller_element, "inventory")
        for product in seller.inventory.values():
            product_element = ET.SubElement(inventory_element, "product")
            ET.SubElement(product_element, "product_id").text = str(product.product_id)
            ET.SubElement(product_element, "name").text = product.name
            ET.SubElement(product_element, "price").text = str(product.price)
            ET.SubElement(product_element, "stock").text = str(product.stock)

        self._save_sellers(root)
        return seller

    def get_seller(self, seller_id: int):
        root = self._load_sellers()

        for seller_element in root.findall("seller"):
            if int(seller_element.find("seller_id").text) == seller_id:
                name = seller_element.find("name").text
                seller = Seller(seller_id=seller_id, name=name)

                # Load products into the seller's inventory
                inventory_element = seller_element.find("inventory")
                for product_element in inventory_element.findall("product"):
                    product_id = int(product_element.find("product_id").text)
                    product_name = product_element.find("name").text
                    price = float(product_element.find("price").text)
                    stock = int(product_element.find("stock").text)

                    # Create product objects and add them to the seller's inventory
                    product = Product(product_id=product_id, name=product_name, category="Unknown", price=price, stock=stock)
                    seller.add_product(product)

                return seller

        raise SellerNotFoundError(seller_id)

    def update_seller(self, seller_id: int, name: str = None):
        seller = self.get_seller(seller_id)
        if name:
            seller.name = name

        # Save updated seller info to XML
        root = self._load_sellers()
        for seller_element in root.findall("seller"):
            if int(seller_element.find("seller_id").text) == seller_id:
                if name:
                    seller_element.find("name").text = name
                self._save_sellers(root)
                return seller

    def delete_seller(self, seller_id: int):
        root = self._load_sellers()

        for seller_element in root.findall("seller"):
            if int(seller_element.find("seller_id").text) == seller_id:
                root.remove(seller_element)
                self._save_sellers(root)
                return f"Seller {seller_id} deleted."

        raise SellerNotFoundError(seller_id)

    def add_product_to_seller(self, seller_id: int, product: Product):
        seller = self.get_seller(seller_id)
        seller.add_product(product)

        # Save updated seller info to XML
        root = self._load_sellers()
        for seller_element in root.findall("seller"):
            if int(seller_element.find("seller_id").text) == seller_id:
                inventory_element = seller_element.find("inventory")
                product_element = ET.SubElement(inventory_element, "product")
                ET.SubElement(product_element, "product_id").text = str(product.product_id)
                ET.SubElement(product_element, "name").text = product.name
                ET.SubElement(product_element, "price").text = str(product.price)
                ET.SubElement(product_element, "stock").text = str(product.stock)

        self._save_sellers(root)
        return f"Product {product.name} added to seller {seller.name}."

    def remove_product_from_seller(self, seller_id: int, product_id: int):
        seller = self.get_seller(seller_id)
        seller.remove_product(product_id)

        # Save updated seller info to XML
        root = self._load_sellers()
        for seller_element in root.findall("seller"):
            if int(seller_element.find("seller_id").text) == seller_id:
                inventory_element = seller_element.find("inventory")
                for product_element in inventory_element.findall("product"):
                    if int(product_element.find("product_id").text) == product_id:
                        inventory_element.remove(product_element)

        self._save_sellers(root)
        return f"Product {product_id} removed from seller {seller.name}."

    def list_all_sellers(self):
        root = self._load_sellers()
        sellers = []
        for seller_element in root.findall("seller"):
            seller_id = int(seller_element.find("seller_id").text)
            name = seller_element.find("name").text
            sellers.append(Seller(seller_id=seller_id, name=name))
        return sellers

    def list_seller_inventory(self, seller_id: int):
        seller = self.get_seller(seller_id)
        return seller.list_inventory()
