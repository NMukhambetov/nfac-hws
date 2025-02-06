import pytest
from unittest.mock import patch, mock_open
from ascii_art import load_banner_from_file, print_word_in_banner

# Test for load_banner_from_file
def test_load_banner_from_file_success():
    # Example ASCII art
    mock_data = (
        " 111   222   333\n"
        " 1 1   2 2   3 3\n"
        " 1 1   222   3333\n"
        " 111   2     3 3\n"
        "        2     3333\n"
        "        2     3 3\n"
        "        2 2   333\n"
        "        222   333\n"
    )
    with patch("builtins.open", mock_open(read_data=mock_data)):
        banner_dict = load_banner_from_file("banner.txt")

    assert len(banner_dict) == 3  # There are 3 characters loaded (ASCII for 1, 2, and 3)
    assert '1' in banner_dict  # Checking if '1' exists in the dictionary
    assert '2' in banner_dict  # Checking if '2' exists in the dictionary
    assert '3' in banner_dict  # Checking if '3' exists in the dictionary

def test_load_banner_from_file_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(SystemExit):  # Expect the program to exit on error
            load_banner_from_file("non_existent_file.txt")

# Test for print_word_in_banner
def test_print_word_in_banner():
    banner_dict = {
        '1': ["111", "1 1", "1 1", "111", "   ", "   ", "   ", "   "],
        '2': ["222", "2 2", "222", "2  ", "222", "   ", "   ", "   "],
        '3': ["333", "3 3", "333", "  3", "333", "   ", "   ", "   "],
    }

    with patch("builtins.print") as mock_print:
        print_word_in_banner("123", banner_dict)
        # Check if print was called with the correct output
        mock_print.assert_any_call("111222333")
        mock_print.assert_any_call("1 12 23 3")
        mock_print.assert_any_call("1 12222")
        mock_print.assert_any_call("1112  3")
        mock_print.assert_any_call("   222 ")
        mock_print.assert_any_call("       ")
        mock_print.assert_any_call("       ")

def test_print_word_in_banner_invalid_char():
    banner_dict = {
        '1': ["111", "1 1", "1 1", "111", "   ", "   ", "   ", "   "],
    }

    with patch("sys.exit") as mock_exit:
        print_word_in_banner("A", banner_dict)
        mock_exit.assert_called_once()  # Check if the program exits on invalid character

