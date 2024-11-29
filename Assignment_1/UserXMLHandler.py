import xml.etree.ElementTree as ET
from Address import Address
from User import User, UserNotFoundError


class UserXMLHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = None
        self.root = None
        self._load_xml()

    def _load_xml(self):
        """Загружает XML файл или создаёт новый, если его нет."""
        try:
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
        except FileNotFoundError:
            self.root = ET.Element("users")
            self.tree = ET.ElementTree(self.root)

    def _save_xml(self):
        """Сохраняет изменения в XML файл."""
        self.tree.write(self.file_path, encoding="utf-8", xml_declaration=True)

    def create(self, email: str, name: str, phone: str, address: Address):
        """Создаёт нового пользователя и сохраняет его в XML."""
        user_id = len(self.root.findall('user')) + 1
        user = User(user_id, email, name, phone, address)

        # Создаём элемент <user>
        user_element = ET.SubElement(self.root, "user")
        ET.SubElement(user_element, "user_id").text = str(user.user_id)
        ET.SubElement(user_element, "email").text = user.email
        ET.SubElement(user_element, "name").text = user.name
        ET.SubElement(user_element, "phone").text = user.phone

        # Создаём элемент <address> для пользователя
        address_element = ET.SubElement(user_element, "address")
        ET.SubElement(address_element, "address_id").text = str(address.address_id)
        ET.SubElement(address_element, "user_id").text = str(address.user_id)
        ET.SubElement(address_element, "city").text = address.city
        ET.SubElement(address_element, "street").text = address.street
        ET.SubElement(address_element, "house").text = str(address.house)
        ET.SubElement(address_element, "apartment").text = str(address.apartment)

        self._save_xml()  # Сохраняем изменения в файл
        return user

    def read_all(self):
        """Возвращает всех пользователей из XML."""
        users = []
        for user_element in self.root.findall('user'):
            user_id = int(user_element.find('user_id').text)
            email = user_element.find('email').text
            name = user_element.find('name').text
            phone = user_element.find('phone').text
            address_element = user_element.find('address')

            address_id = int(address_element.find('address_id').text)
            city = address_element.find('city').text
            street = address_element.find('street').text
            house = int(address_element.find('house').text)
            apartment = int(address_element.find('apartment').text)

            address = Address(address_id, user_id, city, street, house, apartment)
            user = User(user_id, email, name, phone, address)
            users.append(user)

        return users

    def read_by_id(self, user_id: int):
        """Чтение пользователя по ID из XML."""
        for user_element in self.root.findall('user'):
            if int(user_element.find('user_id').text) == user_id:
                email = user_element.find('email').text
                name = user_element.find('name').text
                phone = user_element.find('phone').text
                address_element = user_element.find('address')

                address_id = int(address_element.find('address_id').text)
                city = address_element.find('city').text
                street = address_element.find('street').text
                house = int(address_element.find('house').text)
                apartment = int(address_element.find('apartment').text)

                address = Address(address_id, user_id, city, street, house, apartment)
                user = User(user_id, email, name, phone, address)
                return user
        raise UserNotFoundError(user_id)

    def update(self, user_id: int, email: str = None, name: str = None, phone: str = None, address: Address = None):
        """Обновляет пользователя в XML."""
        user_element = None
        for elem in self.root.findall('user'):
            if int(elem.find('user_id').text) == user_id:
                user_element = elem
                break

        if user_element is None:
            raise UserNotFoundError(user_id)

        if email:
            user_element.find('email').text = email
        if name:
            user_element.find('name').text = name
        if phone:
            user_element.find('phone').text = phone

        if address:
            address_element = user_element.find('address')
            address_element.find('address_id').text = str(address.address_id)
            address_element.find('user_id').text = str(address.user_id)
            address_element.find('city').text = address.city
            address_element.find('street').text = address.street
            address_element.find('house').text = str(address.house)
            address_element.find('apartment').text = str(address.apartment)

        self._save_xml()

    def delete(self, user_id: int):
        """Удаляет пользователя из XML."""
        user_element = None
        for elem in self.root.findall('user'):
            if int(elem.find('user_id').text) == user_id:
                user_element = elem
                break

        if user_element is None:
            raise UserNotFoundError(user_id)

        self.root.remove(user_element)
        self._save_xml()

        return f"User {user_id} has been deleted."

