from UserXMLHandler import UserXMLHandler
from Address import Address


def main():
    # Указываем путь к файлу XML, где будут храниться данные о пользователях
    file_path = 'users.xml'

    # Создаём объект UserXMLHandler
    user_handler = UserXMLHandler(file_path)

    # Создаём адреса
    address1 = Address(address_id=1, user_id=1, city="New York", street="123 Main St", house=10, apartment=101)
    user1 = user_handler.create(email="john.doe@example.com", name="John Doe", phone="123-456-7890", address=address1)
    print(f"Created User: {user1}")

    address2 = Address(address_id=2, user_id=2, city="Los Angeles", street="456 Elm St", house=20, apartment=202)
    user2 = user_handler.create(email="jane.smith@example.com", name="Jane Smith", phone="987-654-3210",
                                address=address2)
    print(f"Created User: {user2}")

    # Обновляем информацию о пользователе
    updated_user = user_handler.update(user1.user_id, name="Johnathan Doe", phone="111-222-3333")
    print(f"Updated User: {updated_user}")

    # Удаляем пользователя
    deleted_user_message = user_handler.delete(user2.user_id)
    print(deleted_user_message)

    # Считываем всех пользователей из файла
    users = user_handler.list_all()
    print("\nAll Users in the system:")
    for user in users:
        print(user)


if __name__ == '__main__':
    main()
