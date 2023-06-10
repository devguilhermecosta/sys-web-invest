from django.test import TestCase
from django.core.exceptions import ValidationError
from utils.validators.fields import length_validate


class FieldLengthValidate(TestCase):
    def test_field_length_validate_returns_validationerror_if_length_igual_zero(self) -> None:  # noqa: E501
        with self.assertRaises(ValidationError):
            field = ''
            length_validate(field)

    def test_field_length_validate_returns_the_field_if_length_biger_then_zero(self) -> None:  # noqa: E501
        field = 'abc'
        validate = length_validate(field)
        self.assertEqual(validate, 'abc')
