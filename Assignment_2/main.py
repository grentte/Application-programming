from reExpression import is_valid_utc, find_utc_times_in_text


if __name__ == "__main__":
    # Пример строки UTC
    test_utc = "2024-12-31T22:34:59Z"
    print(f"'{test_utc}' is valid UTC:", is_valid_utc(test_utc))  # True

    # Текст с несколькими строками UTC
    test_text = "Here are some UTC times: 2024-12-31T22:34:59Z, 1900-01-01T00:00:00Z, and 1988-12-03T22:05:59Z."
    print("Found UTC times:", find_utc_times_in_text(test_text))
