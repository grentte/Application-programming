import requests
from reExpression import find_utc_times_in_text


def find_utc_times_on_webpage(url):
    try:
        if not isinstance(url, str):
            raise TypeError("The URL must be a string.")

        # Получаем содержимое веб-страницы
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Ищем все строки UTC в содержимом страницы
        utc_times = find_utc_times_in_text(response.text)

        # Если строки UTC найдены, выводим их
        if utc_times:
            print("Found UTC times on the page:", utc_times)
        else:
            print("No UTC times were found on the page.")

    except requests.Timeout:
        print("Error: The request timed out. Please check your connection or try a different URL.")
    except requests.ConnectionError:
        print("Error: Unable to connect to the server. Please check your internet connection.")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except TypeError as e:
        print(f"Type error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    url = input("Enter the URL of the web page: ")
    find_utc_times_on_webpage(url) # https://www.utctime.net -> для положительного результата
                                   # https://edu.stankin.ru/mod/assign/view.php?id=412360 -> для отрицательного
