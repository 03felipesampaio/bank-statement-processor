import pytest
from pathlib import Path
from decimal import Decimal, getcontext
from src.statement_readers.inter_bank_statement_reader import InterBankStatementFileReader, convert_brazilian_real_notation_to_decimal

getcontext().prec = 2


class TestInterBankFileReader:
    dummy_file_path = Path("tests/mocks/inter_statement_file_mock.csv")

    @pytest.mark.parametrize('value,expected', [('-1,25', Decimal('-1.25')), ('-45.123.321,09', Decimal('-45123321.09')), ('2.345,45', Decimal('2345.45')), ('0,00', Decimal('0.00'))])
    def test_convert_brazilian_real_to_decimal_with_valid_values(self, value, expected):
        converted_value = convert_brazilian_real_notation_to_decimal(value)
        assert converted_value == expected

    def test_read_file_with_valid_transactions(self):
        with open(self.dummy_file_path) as csv_file:
            statement = InterBankStatementFileReader(self.dummy_file_path.name, csv_file)

        assert len(statement.transactions) == 6
        assert statement.account_number == '123456789'
