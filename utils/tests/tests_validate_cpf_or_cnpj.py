# flake8: noqa
from unittest import TestCase
from utils.validators import ValidateCPForCNPJ


class ValidateCpfOrCnpjTests(TestCase):
    def test_function_returns_false_if_param_cpf_or_cnpj_is_not_a_string_and_not_valid(self) -> None:
        cpf = ValidateCPForCNPJ(1111111111)

        self.assertFalse(cpf.is_valid())

    def test_function_returns_false_if_len_param_cpf_diferrent_of_11(self) -> None:
        cpf = ValidateCPForCNPJ('1111111111')
        self.assertFalse(cpf.is_valid())

    def test_function_returns_false_if_len_param_cnpj_diferrent_of_14(self) -> None:
        cnpj = ValidateCPForCNPJ('111111111111111')
        self.assertFalse(cnpj.is_valid())

    def test_function_remove_letters_and_special_chars_for_validate_cnpj_and_return_true_if_is_valid(self) -> None:
        cnpj = ValidateCPForCNPJ('12.684.abcd442/0001-83@bgtdsff//;[]')
        self.assertTrue(cnpj.is_valid())
        self.assertEqual(cnpj.formatted(), '12684442000183')

    def test_function_remove_letters_and_special_chars_for_validate_cpf_and_return_true_if_is_valid(self) -> None:
        cpf = ValidateCPForCNPJ('739.070.200-14@bgtdsff//;[]')
        self.assertTrue(cpf.is_valid())
        self.assertEqual(cpf.formatted(), '73907020014')

    def test_function_return_false_if_cnpj_is_invalid(self) -> None:
        cnpj = ValidateCPForCNPJ('09.770.970/0001-00ac@bgtdsff//;[]')
        self.assertFalse(cnpj.is_valid())

    def test_function_return_false_if_cpf_is_invalid_and_formatted_func_not_format(self) -> None:
        cpf = ValidateCPForCNPJ('137.461.044-00@bgtdsff//;[]')
        self.assertFalse(cpf.is_valid())
        self.assertEqual(cpf.formatted(), None)

    def test_function_return_false_if_cpf_is_fully_formed_by_number_one(self) -> None:
        cpf = ValidateCPForCNPJ('111.111.111-11')
        self.assertFalse(cpf.is_valid())

    def test_function_return_false_if_cpf_is_fully_formed_by_number_zero(self) -> None:
        cpf = ValidateCPForCNPJ('000.000.000-00')
        self.assertFalse(cpf.is_valid())

    def test_function_return_false_if_cnpj_is_fully_formed_by_number_one(self) -> None:
        cpf = ValidateCPForCNPJ('11.111.111/1111-11')
        self.assertFalse(cpf.is_valid())

    def test_function_return_false_if_cnpj_is_fully_formed_by_number_zero(self) -> None:
        cpf = ValidateCPForCNPJ('00.000.000/0000-00')
        self.assertFalse(cpf.is_valid())
