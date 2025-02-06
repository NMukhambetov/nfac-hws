import pytest
from poetry import greet

def test_greet():
    assert greet("Нуртас") == "Привет, Нуртас!"
    assert greet("Али") == "Привет, Али!"
