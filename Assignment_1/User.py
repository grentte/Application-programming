from Address import Address


class UserNotFoundError(Exception):
    def __init__(self, user_id):
        super().__init__(f"User with ID {user_id} not found.")


class User:
    def __init__(self, user_id: int, email: str, name: str = None, phone: str = None, address: Address = None):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.phone = phone
        self.address = address

    def register(self):
        return f"User {self.name} registered"

    def login(self):
        return f"User {self.email} logged in"

    def logout(self):
        return f"User {self.email} logged out"

    def __repr__(self):
        return f"User (id={self.user_id}, email={self.email}, name='{self.name}', phone={self.phone}, address={self.address})"


class UserManager:
    def __init__(self):
        self.users_list = []
        self.current_user_id = 1

    def create(self, email: str, name: str, phone: str, address: Address):
        if not email:
            raise ValueError("Email is required to create a user.")
        user = User(self.current_user_id, email, name, phone, address)
        self.users_list.append(user)
        self.current_user_id += 1
        return user

    def read_all(self):
        return self.users_list

    def read_by_id(self, user_id: int):
        for user in self.users_list:
            if user.user_id == user_id:
                return user
        raise UserNotFoundError(user_id)

    def update(self, user_id: int, email: str = None, name: str = None, phone: str = None, address: Address = None):
        try:
            user = self.read_by_id(user_id)
        except UserNotFoundError as e:
            return str(e)

        if email is not None:
            user.email = email
        if name is not None:
            user.name = name
        if phone is not None:
            user.phone = phone
        if address is not None:
            user.address = address
        return user

    def delete(self, user_id: int):
        try:
            user = self.read_by_id(user_id)
            self.users_list.remove(user)
            return f"User {user_id} has been deleted."
        except UserNotFoundError as e:
            return str(e)
