class Address:
    def __init__(self, address_id: int, user_id: int, city: str, street: str, house: int, apartment: int):
        self.address_id = address_id
        self.user_id = user_id
        self.city = city
        self.street = street
        self.house = house
        self.apartment = apartment

    def __repr__(self):
        return (f"Address(address_id={self.address_id}, user_id={self.user_id}, city={self.city}, street={self.street}, "
                f"house={self.house}, apartment={self.apartment})")

    def add_address(self):
        if not all([self.city, self.street, self.house, self.apartment]):
            raise ValueError("All address fields must be provided.")
        return f"Address {self.street}, {self.city} added."

    def update_address(self, new_city: str, new_street: str, new_house: int, new_apartment: int):
        if not all([new_city, new_street, new_house, new_apartment]):
            raise ValueError("All fields must be provided to update the address.")
        self.city = new_city
        self.street = new_street
        self.house = new_house
        self.apartment = new_apartment
        return f"Address updated to: {self.city}, {self.street}, {self.house}, {self.apartment}."

    def delete_address(self):
        return f"Address {self.city}, {self.street}, {self.house}, {self.apartment} deleted."


class AddressManager:
    def __init__(self):
        self.addresses = {}

    def create_address(self, user_id: int, city: str, street: str, house: int, apartment: int):
        if not all([city, street, house, apartment]):
            raise ValueError("All fields must be provided to create an address.")
        address_id = len(self.addresses) + 1  # Генерация уникального ID для нового адреса
        address = Address(address_id, user_id, city, street, house, apartment)
        self.addresses[address_id] = address
        return address

    def read_address_by_id(self, address_id: int):
        address = self.addresses.get(address_id)
        if not address:
            raise AddressNotFoundError(address_id)
        return address

    def update_address(self, address_id: int, new_city: str, new_street: str, new_house: int, new_apartment: int):
        address = self.addresses.get(address_id)
        if not address:
            raise AddressNotFoundError(address_id)
        return address.update_address(new_city, new_street, new_house, new_apartment)

    def delete_address(self, address_id: int):
        address = self.addresses.get(address_id)
        if not address:
            raise AddressNotFoundError(address_id)
        del self.addresses[address_id]
        return f"Address {address_id} deleted successfully."

    def get_all_addresses(self):
        if not self.addresses:
            raise AddressError("No addresses available.")
        return [address for address in self.addresses.values()]


class AddressError(Exception):
    """Общее исключение для ошибок, связанных с адресами."""
    pass


class AddressNotFoundError(AddressError):
    """Исключение для случаев, когда адрес не найден."""
    def __init__(self, address_id):
        super().__init__(f"Address with ID {address_id} not found.")
