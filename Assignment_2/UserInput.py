from reExpression import is_valid_utc

def check_user_input():
    try:
        utc_time = input("Enter UTC time for verification (e.g., 2024-11-29T12:34:56Z): ").strip()

        if not isinstance(utc_time, str):
            raise TypeError("The entered value must be a string.")

        if is_valid_utc(utc_time):
            print("The UTC time is correct!")
        else:
            print("Incorrect UTC time. Please ensure the format is YYYY-MM-DDTHH:MM:SSZ.")
    except TypeError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")

if __name__ == "__main__":
    check_user_input()