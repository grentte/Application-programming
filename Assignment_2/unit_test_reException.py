import unittest
from unittest.mock import patch, mock_open
import requests
from reExpression import is_valid_utc, find_utc_times_in_text
from WebPageSearch import find_utc_times_on_webpage
from FileSearch import find_utc_times_in_file


class TestReUTC(unittest.TestCase):

    def test_is_valid_utc(self):
        # Проверка валидных UTC строк
        self.assertTrue(is_valid_utc("2024-11-29T12:34:56Z"))
        self.assertTrue(is_valid_utc("2000-01-01T00:00:00Z"))

        # Проверка невалидных UTC строк
        self.assertFalse(is_valid_utc("2024-13-29T12:34:56Z"))  # ошибка в месяце
        self.assertFalse(is_valid_utc("2024-11-32T12:34:56Z"))  # ошибка в дне
        self.assertFalse(is_valid_utc("2024-11-29T25:00:00Z"))  # ошибка в часе
        self.assertFalse(is_valid_utc("2024-11-29T12:60:00Z"))  # ошибка в минуте
        self.assertFalse(is_valid_utc("2024-11-29T12:34:60Z"))  # ошибка в секунде
        self.assertFalse(is_valid_utc("2024-11-29T12:34:56"))  # ошибка в отсутствии Z

    def test_find_utc_times_in_text(self):
        text = "Dates: 2024-11-29T12:34:56Z, 2023-08-15T09:45:00Z, invalid: 2024-13-01T12:00:00Z"
        result = find_utc_times_in_text(text)
        self.assertEqual(result, ["2024-11-29T12:34:56Z", "2023-08-15T09:45:00Z"])

    def test_find_utc_times_in_text_no_valid(self):
        text = "No valid dates here"
        result = find_utc_times_in_text(text)
        self.assertEqual(result, [])


class TestFileUTCSearch(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open,
           read_data="UTC: 2024-11-29T12:34:56Z\nInvalid: 2024-13-29T12:34:56Z")
    def test_find_utc_times_in_file(self, mock_file):
        result = find_utc_times_in_file("utc_times.txt")
        self.assertEqual(result, ["2024-11-29T12:34:56Z"])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_find_utc_times_in_file_not_found(self, mock_file):
        with patch("builtins.print") as mock_print:
            find_utc_times_in_file("non_utc_times.txt")
            mock_print.assert_called_with(
                "Error: The file was not found. Make sure that the path is specified correctly.")


class TestWebpageUTCSearch(unittest.TestCase):

    @patch("requests.get")
    def test_find_utc_times_on_webpage(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "UTC times: 2024-11-29T12:34:56Z, 2023-08-15T09:45:00Z"

        with patch("builtins.print") as mock_print:
            find_utc_times_on_webpage("https://www.example.com")
            mock_print.assert_called_with("Found UTC times on the page:",
                                          ["2024-11-29T12:34:56Z", "2023-08-15T09:45:00Z"])

    @patch("requests.get")
    def test_find_utc_times_on_webpage_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")

        with patch("builtins.print") as mock_print:
            find_utc_times_on_webpage("https://www.example.com")
            mock_print.assert_called_with("An unexpected error occurred: Network error")


if __name__ == "__main__":
    unittest.main()
