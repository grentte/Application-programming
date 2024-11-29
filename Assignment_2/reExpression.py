import re

utc_regex = r'(?:\d{1,3}[0-9]{3}|20[0-9]{2})-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])T(?:[01]\d|2[0-3]):(?:[0-5]\d):(?:[0-5]\d)Z'

def is_valid_utc(utc_time):
    """
    Проверяет, соответствует ли строка формату UTC (например, 2024-11-29T12:34:56Z).
    """
    try:
        if not isinstance(utc_time, str):
            raise TypeError("The provided UTC time must be a string.")
        return re.fullmatch(utc_regex, utc_time) is not None
    except TypeError as e:
        print(f"Error: {e}")
        return False

def find_utc_times_in_text(text):
    """
    Ищет все строки формата UTC в тексте.
    """
    try:
        if not isinstance(text, str):
            raise TypeError("The provided text must be a string.")
        return re.findall(utc_regex, text)
    except TypeError as e:
        print(f"Error: {e}")
        return []
