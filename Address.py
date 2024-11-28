class Address:

    def __init__(self, address_id, user_id, city, street, house, apartment):
        self.address_id = address_id
        self.user_id = user_id
        self.city = city
        self.street = street
        self.house = house
        self.apartment = apartment

    def __repr__(self):
        return f"Address(address_id={self.address_id}, user_id={self.user_id}, street='{self.street}', city='{self.city}', zip_code='{self.zip_code}')"

    def add_address(self):
        return f"Address {self.street}, {self.city} added successfully!"

    def update_address(self, new_street, new_city, new_zip_code):
        self.street = new_street
        self.city = new_city
        self.zip_code = new_zip_code
        return f"Address updated to {self.street}, {self.city}."

    def delete_address(self):
        return f"Address {self.street}, {self.city} deleted successfully!"


class AddressManager:
    pass

