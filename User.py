class User:
    def __init__(self, user_id, email, name = None, phone = None, address = None):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.phone = phone
        self.address = address

    def register(self):
        return f"User {self.name} registered successfully!"

    def login(self):
        return f"User {self.email} logged in successfully!"

    def logout(self):
        return f"User {self.email} logged out successfully!"

    def __repr__(self):
        return f"User (id={self.user_id}, email={self.email}, name='{self.name}', phone={self.phone}, address={self.address}"

class UserManager:
    def __init__(self):
        self.users_list = []
        self.current_user_id = 1

    def create(self, email, name, phone, address):
        user = User(self.current_user_id, email, name, phone, address)
        self.users_list.append(user)
        self.current_user_id += 1
        return user

    def read_all(self):
        return self.users_list

    def read_by_id(self, user_id):
        for user in self.users_list:
            if user_id == user_id:
                return user

        return None

    def update(self, user_id, email = None, name = None, phone = None, address = None):
        user = self.read_by_id(user_id)
        if user:
            if email is not None:
                user.email = email
            if name is not None:
                user.name = name
            if phone is not None:
                user.phone = phone
            if address is not None:
                user.address = address
            return user

    def delete(self, user_id):
        user = self.read_by_id(user_id)
        if user:
            self.users_list.remove(user)
            return f"User {user_id} has been deleted."
        return "Person not found"
