import unittest

from src.domain.exceptions.asset_value_not_accept import AssetValueNotAccept
from src.domain.exceptions.type_mismatch import TypeMismatch
from src.domain.exceptions.invalid_email import InvalidEmail
from src.domain.exceptions.invalid_value import InvalidValue
from src.domain.exceptions.empty_value import EmptyValue

from src.domain.value_objects.asset_value_object import AssetValueObject
from src.domain.value_objects.email_value_object import EmailValueObject
from src.domain.value_objects.name_value_object import NameValueObject
from src.domain.value_objects.type_request_value_object import TypeRequestValueObject


class TestValueObjects(unittest.TestCase):
    def test_name_must_be_string(self):
        with self.assertRaises(TypeMismatch):
            NameValueObject(123)

    def test_name_cannot_be_empty(self):
        with self.assertRaises(EmptyValue):
            NameValueObject(" ")

    def test_name_must_have_at_least_three_characters(self):
        with self.assertRaises(InvalidValue):
            NameValueObject("Jo")

    def test_email_must_be_valid(self):
        with self.assertRaises(InvalidEmail):
            EmailValueObject("invalid-email")

    def test_asset_value_must_be_integer_or_decimal(self):
        with self.assertRaises(TypeMismatch):
            AssetValueObject("200000")

    def test_asset_value_must_not_be_boolean(self):
        with self.assertRaises(TypeMismatch):
            AssetValueObject(True)

    def test_asset_value_must_be_positive(self):
        with self.assertRaises(AssetValueNotAccept):
            AssetValueObject(0)

    def test_type_request_cannot_be_empty(self):
        with self.assertRaises(EmptyValue):
            TypeRequestValueObject(" ")


if __name__ == "__main__":
    unittest.main()
