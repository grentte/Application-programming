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
        return f"Address {self.street}, {self.city} added."

    def update_address(self, new_city: str, new_street: str, new_house: int, new_apartment: int):
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
        address_id = len(self.addresses) + 1  # Генерация уникального ID для нового адреса
        address = Address(address_id, user_id, city, street, house, apartment)
        self.addresses[address_id] = address
        return address

    def read_address_by_id(self, address_id: int):
        return self.addresses.get(address_id, "Address not found.")

    def update_address(self, address_id: int, new_city: str, new_street: str, new_house: int, new_apartment: int):
        address = self.addresses.get(address_id)
        if address:
            return address.update_address(new_city, new_street, new_house, new_apartment)
        return "Address not found."

    def delete_address(self, address_id: int):
        address = self.addresses.get(address_id)
        if address:
            del self.addresses[address_id]
            return f"Address {address_id} deleted successfully."
        return "Address not found."

    def get_all_addresses(self):
        return [address for address in self.addresses.values()]