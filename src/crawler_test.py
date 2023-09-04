import pytest

def verify_type(value, type):
    return isinstance(value, type)

def verify_if_is_float():
    assert verify_type(1.23, int)

def verify_if_is_string():
    assert verify_type("String", str)

def verify_if_is_list():
    assert verify_type(["Test", 1.11, 3.11], list)

