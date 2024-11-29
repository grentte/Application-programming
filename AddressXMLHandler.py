import xml.etree.ElementTree as ET
from typing import Optional
from Address import Address

class AddressExistsError(Exception):
    pass

class AddressNotFoundError(Exception):
    pass

class AddressXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, address: Address):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("addresses")

        # Check if the address already exists based on the address_id
        for address_element in root.findall("address"):
            if address_element.find("address_id").text == str(address.address_id):
                raise AddressExistsError(f"Address with ID '{address.address_id}' already exists.")

        address_element = ET.SubElement(root, "address")
        ET.SubElement(address_element, "address_id").text = str(address.address_id)
        ET.SubElement(address_element, "user_id").text = str(address.user_id)
        ET.SubElement(address_element, "city").text = address.city
        ET.SubElement(address_element, "street").text = address.street
        ET.SubElement(address_element, "house").text = str(address.house)
        ET.SubElement(address_element, "apartment").text = str(address.apartment)

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, address_id: int) -> Optional[Address]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for address_element in root.findall("address"):
                if int(address_element.find("address_id").text) == address_id:
                    user_id = int(address_element.find("user_id").text)
                    city = address_element.find("city").text
                    street = address_element.find("street").text
                    house = int(address_element.find("house").text)
                    apartment = int(address_element.find("apartment").text)
                    return Address(address_id, user_id, city, street, house, apartment)
        except (FileNotFoundError, ET.ParseError):
            return None
        return None

    def update(self, address_id: int, new_city: str, new_street: str, new_house: int, new_apartment: int) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for address_element in root.findall("address"):
                if int(address_element.find("address_id").text) == address_id:
                    address_element.find("city").text = new_city
                    address_element.find("street").text = new_street
                    address_element.find("house").text = str(new_house)
                    address_element.find("apartment").text = str(new_apartment)
                    tree.write(self.filepath)
                    return True

            raise AddressNotFoundError(f"Address with ID '{address_id}' not found for update.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except AddressNotFoundError as e:
            print(e)
            return False

    def delete(self, address_id: int) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for address_element in root.findall("address"):
                if int(address_element.find("address_id").text) == address_id:
                    root.remove(address_element)
                    tree.write(self.filepath)
                    return True

            raise AddressNotFoundError(f"Address with ID '{address_id}' not found for deletion.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except AddressNotFoundError as e:
            print(e)
            return False

    def get_all_addresses(self):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            addresses = []
            for address_element in root.findall("address"):
                address_id = int(address_element.find("address_id").text)
                user_id = int(address_element.find("user_id").text)
                city = address_element.find("city").text
                street = address_element.find("street").text
                house = int(address_element.find("house").text)
                apartment = int(address_element.find("apartment").text)
                addresses.append(Address(address_id, user_id, city, street, house, apartment))

            return addresses
        except (FileNotFoundError, ET.ParseError):
            return []
