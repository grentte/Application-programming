import json
from typing import Optional
from Address import Address


class AddressExistsError(Exception):
    pass


class AddressNotFoundError(Exception):
    pass


class AddressJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, address: Address):
        address_data = {
            "address_id": address.address_id,
            "user_id": address.user_id,
            "city": address.city,
            "street": address.street,
            "house": address.house,
            "apartment": address.apartment,
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"addresses": []}

        for existing_address in data.get("addresses", []):
            if existing_address["address_id"] == address.address_id:
                raise AddressExistsError(f"Address with ID {address.address_id} already exists.")

        data["addresses"].append(address_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, address_id: int) -> Optional[Address]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for address_data in data.get("addresses", []):
                if address_data["address_id"] == address_id:
                    return Address(
                        address_id=address_data["address_id"],
                        user_id=address_data["user_id"],
                        city=address_data["city"],
                        street=address_data["street"],
                        house=address_data["house"],
                        apartment=address_data["apartment"],
                    )
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update(self, address_id: int, new_city: str, new_street: str, new_house: int, new_apartment: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for address_data in data.get("addresses", []):
                if address_data["address_id"] == address_id:
                    if new_city:
                        address_data["city"] = new_city
                    if new_street:
                        address_data["street"] = new_street
                    if new_house:
                        address_data["house"] = new_house
                    if new_apartment:
                        address_data["apartment"] = new_apartment
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
            raise AddressNotFoundError(f"Address with ID {address_id} not found for update.")
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except AddressNotFoundError as e:
            print(e)
            return False

    def delete(self, address_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("addresses", []))
            data["addresses"] = [address for address in data.get("addresses", []) if address["address_id"] != address_id]

            if len(data["addresses"]) == original_length:
                raise AddressNotFoundError(f"Address with ID {address_id} not found for deletion.")

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except AddressNotFoundError as e:
            print(e)
            return False

    def get_all(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            return [
                Address(
                    address_id=address_data["address_id"],
                    user_id=address_data["user_id"],
                    city=address_data["city"],
                    street=address_data["street"],
                    house=address_data["house"],
                    apartment=address_data["apartment"],
                )
                for address_data in data.get("addresses", [])
            ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
