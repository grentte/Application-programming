from reExpression import find_utc_times_in_text


def find_utc_times_in_file(filepath):
    try:
        if not isinstance(filepath, str):
            raise TypeError("The file path must be a string.")

        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

            utc_times = find_utc_times_in_text(content)

            if utc_times:
                print("Found UTC times in the file: ", utc_times)
                return utc_times
            else:
                print("No UTC times were found in the file.")

    except FileNotFoundError:
        print("Error: The file was not found. Make sure that the path is specified correctly.")
    except PermissionError:
        print("Error: There are not enough permissions to access the file.")
    except UnicodeDecodeError:
        print("Error: The file cannot be read. Make sure that the file is in UTF-8 encoding.")
    except TypeError as e:
        print(f"Type error: {e}")
    except IOError as e:
        print(f"I/O error: {e}")
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")


if __name__ == "__main__":
    filepath = input("Enter the path to the file: ")
    find_utc_times_in_file(filepath)
