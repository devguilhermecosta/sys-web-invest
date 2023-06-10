import string
from functools import reduce


class ValidateCPForCNPJ:
    def __init__(self, cpf_or_cnpj: str) -> None:
        self.__cpf_or_cnpj: str = cpf_or_cnpj

    @staticmethod
    def __remove_special_characters(string_chain: str) -> str:
        symbols = [
            ' ', '"', ',', '.', ';', ':', '?',
            '°', '~', '^', ']', '}', 'º',
            '´', '`', '[', 'ª', '{', '+',
            '-', '*', '/', '|', '_', '=',
            '!', '@', '#', '$', '%',
            '&', '¨', '(', ')'
            ]

        for s in string.ascii_letters:
            symbols.append(s)

        s = string_chain.translate({
            ord(s): '' for s in symbols
        })
        return s

    def __check_if_cpf_or_cnpj(self, cpf_or_cnpj: str) -> str | None:
        treated_data: str = self.__remove_special_characters(cpf_or_cnpj)

        if len(treated_data) == 11:
            return 'cpf'

        elif len(treated_data) == 14:
            return 'cnpj'

        return None

    def __calc_digit(self,
                     cpf_or_cnpj_slice: str,
                     count: int = 10,
                     reverse_for_cpnj: bool = False,
                     ) -> int:
        partial: str = cpf_or_cnpj_slice
        cpf_or_cnpj_list: list = []

        if reverse_for_cpnj:
            reversed_cnpj: str = partial[::-1]
            control: int = 2
            for n in reversed_cnpj:
                cpf_or_cnpj_list.append(
                    (control, n)
                )
                control += 1
                if control > 9:
                    control = 2

        else:
            for n in partial:
                cpf_or_cnpj_list.append(
                    (count, n)
                )
                count -= 1

        total: int = reduce(
            lambda x, y: x+y, [(i[0] * int(i[1])) for i in cpf_or_cnpj_list]
        )

        module: int = total % 11
        digit: int = 0 if (11 - module >= 10) else 11 - module

        return digit

    def __validate_cpf(self, cpf: str) -> bool:
        digit_one = self.__calc_digit(cpf[:9], 10)
        digit_two = self.__calc_digit(cpf[:10], 11)

        last_digits: str = f'{digit_one}{digit_two}'

        return cpf[-2:] == last_digits

    def __validate_cnpj(self, cnpj: str) -> bool:
        digit_one = self.__calc_digit(cnpj[:12], reverse_for_cpnj=True)
        digit_two = self.__calc_digit(cnpj[:13], reverse_for_cpnj=True)

        last_digits: str = f'{digit_one}{digit_two}'

        return cnpj[-2:] == last_digits

    def __fully_formed_by_one_or_zero(self, cpf_or_cnpj) -> bool:
        match cpf_or_cnpj:
            case '00000000000':
                return False
            case '11111111111':
                return False
            case '00000000000000':
                return False
            case '11111111111111':
                return False
            case _:
                return True

    def is_valid(self) -> bool:
        if not isinstance(self.__cpf_or_cnpj, str):
            try:
                self.__cpf_or_cnpj = str(self.__cpf_or_cnpj)
            except ValueError:
                return False

        check_data_type = self.__check_if_cpf_or_cnpj(self.__cpf_or_cnpj)
        treated_data: str = self.__remove_special_characters(
            self.__cpf_or_cnpj
            )

        if check_data_type == 'cpf':
            if not self.__fully_formed_by_one_or_zero(treated_data):
                return False
            return self.__validate_cpf(treated_data)

        if check_data_type == 'cnpj':
            if not self.__fully_formed_by_one_or_zero(treated_data):
                return False
            return self.__validate_cnpj(treated_data)

        return False

    def formatted(self) -> str:
        """
            if cpf_or_cnpj is valid, return cpf_of_cnpj
            without symbols and letters
        """
        if self.is_valid():
            return self.__remove_special_characters(self.__cpf_or_cnpj)
        return None

    @property
    def get_cpf_or_cnpj(self) -> str:
        return self.__cpf_or_cnpj
