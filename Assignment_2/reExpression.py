import re

utc_regex = (r'(?:\d{4})' # Год
             r'-(?:0[1-9]|1[0-2])' # Месяц
             r'-(?:0[1-9]|[12]\d|3[01])T' # День
             r'(?:[01]\d|2[0-3])' # Час
             r':(?:[0-5]\d)' # Минута
             r':(?:[0-5]\d)Z') # Секунда

def is_valid_utc(utc_time):
    try:
        if not isinstance(utc_time, str):
            raise TypeError("The provided UTC time must be a string.")
        return re.fullmatch(utc_regex, utc_time) is not None
    except TypeError as e:
        print(f"Error: {e}")
        return False

def find_utc_times_in_text(text):
    try:
        if not isinstance(text, str):
            raise TypeError("The provided text must be a string.")
        return re.findall(utc_regex, text)
    except TypeError as e:
        print(f"Error: {e}")
        return []
