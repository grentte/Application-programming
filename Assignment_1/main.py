from User import UserManager, User, UserNotFoundError
from UserJSONHandler import UserJSONHandler, UserExistsError
from Address import Address
import os


def main():
    # Файлы для хранения данных о пользователях
    json_file = "users.json"

    # Убедимся, что файл существует (или создадим пустой файл)
    if not os.path.exists(json_file):
        with open(json_file, "w") as file:
            file.write("{\"users\": []}")

    # Инициализация менеджеров
    user_manager = UserManager()
    json_handler = UserJSONHandler(json_file)

    # Создание адреса и пользователя
    print("\n--- Creating user in memory ---")
    address1 = Address(1, 1, "Moscow", "Arbat", 15, 200)
    user1 = user_manager.create("user1@example.com", "Alice", "+1234567890", address1)
    print(f"Created user: {user1}")

    # Сохранение пользователя в JSON
    print("\n--- UserJSONHandler: Saving user to JSON ---")
    try:
        json_handler.create(user1)
        print(f"User {user1.name} saved to JSON.")
    except UserExistsError as e:
        print(e)

if __name__ == "__main__":
    main()
