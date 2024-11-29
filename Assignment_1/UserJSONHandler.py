import json
from typing import Optional
from User import User
from Address import Address


class UserExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, user: User):
        user_data = {
            "user_id": user.user_id,
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "address": {
                "city": user.address.city if user.address else None,
                "street": user.address.street if user.address else None,
                "house": user.address.house if user.address else None,
                "apartment": user.address.apartment if user.address else None,
            },
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"users": []}

        for existing_user in data.get("users", []):
            if existing_user["email"] == user.email:
                raise UserExistsError(f"User with email '{user.email}' already exists.")

        data["users"].append(user_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, user_id: int) -> Optional[User]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for user_data in data.get("users", []):
                if user_data["user_id"] == user_id:
                    address = None
                    if user_data["address"]:
                        address = Address(
                            user_data["address"]["city"],
                            user_data["address"]["street"],
                            user_data["address"]["house"],
                            user_data["address"]["apartment"],
                        )
                    return User(
                        user_id=user_data["user_id"],
                        email=user_data["email"],
                        name=user_data["name"],
                        phone=user_data["phone"],
                        address=address,
                    )
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update(self, user_id: int, email: str = None, name: str = None, phone: str = None, address: Address = None):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for user_data in data.get("users", []):
                if user_data["user_id"] == user_id:
                    if email:
                        user_data["email"] = email
                    if name:
                        user_data["name"] = name
                    if phone:
                        user_data["phone"] = phone
                    if address:
                        user_data["address"] = {
                            "city": address.city,
                            "street": address.street,
                            "house": address.house,
                            "apartment": address.apartment,
                        }
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
            raise UserNotFoundError(f"User with ID {user_id} not found for update.")
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except UserNotFoundError as e:
            print(e)
            return False

    def delete(self, user_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("users", []))
            data["users"] = [user for user in data.get("users", []) if user["user_id"] != user_id]

            if len(data["users"]) == original_length:
                raise UserNotFoundError(f"User with ID {user_id} not found for deletion.")

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except UserNotFoundError as e:
            print(e)
            return False
