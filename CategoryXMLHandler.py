import xml.etree.ElementTree as ET
from typing import Optional
from Product import Product, ProductNotFoundError
from Category import Category, CategoryNotFoundError

class CategoryExistsError(Exception):
    pass

class CategoryXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, category: Category):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("categories")

        # Check if the category already exists by category_id
        for category_element in root.findall("category"):
            if category_element.find("category_id").text == str(category.category_id):
                raise CategoryExistsError(f"Category with ID '{category.category_id}' already exists.")

        category_element = ET.SubElement(root, "category")
        ET.SubElement(category_element, "category_id").text = str(category.category_id)
        ET.SubElement(category_element, "name").text = category.name
        ET.SubElement(category_element, "description").text = category.description

        products_element = ET.SubElement(category_element, "products")
        for product in category.products:
            product_element = ET.SubElement(products_element, "product")
            ET.SubElement(product_element, "product_id").text = str(product.product_id)

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, category_id: int) -> Optional[Category]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for category_element in root.findall("category"):
                if int(category_element.find("category_id").text) == category_id:
                    name = category_element.find("name").text
                    description = category_element.find("description").text
                    category = Category(category_id, name, description)

                    # Load products from XML
                    for product_element in category_element.find("products").findall("product"):
                        product_id = int(product_element.find("product_id").text)
                        product = Product.get_product_by_id(product_id)  # Assuming a method in Product class
                        if product:
                            category.products.append(product)

                    return category
        except (FileNotFoundError, ET.ParseError):
            return None
        return None

    def update(self, category_id: int, name: str = None, description: str = None) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for category_element in root.findall("category"):
                if int(category_element.find("category_id").text) == category_id:
                    if name:
                        category_element.find("name").text = name
                    if description:
                        category_element.find("description").text = description
                    tree.write(self.filepath)
                    return True
            raise CategoryNotFoundError(category_id)
        except (FileNotFoundError, ET.ParseError, CategoryNotFoundError) as e:
            print(e)
            return False

    def delete(self, category_id: int) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for category_element in root.findall("category"):
                if int(category_element.find("category_id").text) == category_id:
                    root.remove(category_element)
                    tree.write(self.filepath)
                    return True

            raise CategoryNotFoundError(category_id)
        except (FileNotFoundError, ET.ParseError, CategoryNotFoundError) as e:
            print(e)
            return False

    def get_all_categories(self):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            categories = []
            for category_element in root.findall("category"):
                category_id = int(category_element.find("category_id").text)
                name = category_element.find("name").text
                description = category_element.find("description").text
                category = Category(category_id, name, description)

                # Load products from XML
                for product_element in category_element.find("products").findall("product"):
                    product_id = int(product_element.find("product_id").text)
                    product = Product.get_product_by_id(product_id)  # Assuming a method in Product class
                    if product:
                        category.products.append(product)

                categories.append(category)

            return categories
        except (FileNotFoundError, ET.ParseError):
            return []

    def add_product_to_category(self, category_id: int, product: Product) -> str:
        try:
            category = self.read(category_id)
            if not category:
                raise CategoryNotFoundError(category_id)
            if product in category.products:
                return f"Product {product.name} is already in category {category.name}."
            category.add_product_to_category(product)

            # Update XML
            self.update(category_id, category.name, category.description)
            return f"Product {product.name} added to category {category.name}."
        except (CategoryNotFoundError, ValueError) as e:
            return str(e)

    def remove_product_from_category(self, category_id: int, product: Product) -> str:
        try:
            category = self.read(category_id)
            if not category:
                raise CategoryNotFoundError(category_id)
            category.remove_product_from_category(product)

            # Update XML
            self.update(category_id, category.name, category.description)
            return f"Product {product.name} removed from category {category.name}."
        except (CategoryNotFoundError, ProductNotFoundError) as e:
            return str(e)
