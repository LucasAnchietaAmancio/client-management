import unittest

from domain.exceptions.asset_value_not_accept import AssetValueNotAccept
from domain.exceptions.type_mismatch import TypeMismatch
from domain.exceptions.invalid_email_error import InvalidEmailError
from domain.exceptions.invalid_value_error import InvalidValueError
from domain.exceptions.empty_value_error import EmptyValueError

from domain.value_objects.asset_value_object import AssetValueObject
from domain.value_objects.email_value_object import EmailValueObject
from domain.value_objects.name_value_object import NameValueObject


class TestValueObjects(unittest.TestCase):
    def test_name_must_be_string(self):
        with self.assertRaises(TypeMismatch):
            NameValueObject(123)

    def test_name_cannot_be_empty(self):
        with self.assertRaises(EmptyValueError):
            NameValueObject(" ")

    def test_name_must_have_at_least_three_characters(self):
        with self.assertRaises(InvalidValueError):
            NameValueObject("Jo")

    def test_email_must_be_valid(self):
        with self.assertRaises(InvalidEmailError):
            EmailValueObject("invalid-email")

    def test_asset_value_must_be_integer_or_decimal(self):
        with self.assertRaises(TypeMismatch):
            AssetValueObject("200000")

    def test_asset_value_must_be_positive(self):
        with self.assertRaises(AssetValueNotAccept):
            AssetValueObject(0)


if __name__ == "__main__":
    unittest.main()
