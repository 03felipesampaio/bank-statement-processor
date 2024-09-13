import pytest
from pathlib import Path
import fitz
import tempfile
from src.readers.inter import InterCreditCardReader
from datetime import date


def test_read_bill_date():
    reader = InterCreditCardReader()
    content = "VENCIMENTO\n10/10/2023"
    assert reader.read_bill_date(content) == date(2023, 10, 10)

def test_read_bill_value():
    reader = InterCreditCardReader()
    content = "TOTAL DESSA FATURA\nR$\n1.234,56"
    assert reader.read_bill_value(content) == 1234.56

def test_read_transactions():
    reader = InterCreditCardReader()
    content = "10 SET 2023\nCOMPRA NO ESTABELECIMENTO\nR$ 1.234,56"
    transactions = reader.read_transactions(content)

    assert transactions[0].date == date(2023, 9, 10)
    assert transactions[0].description == "COMPRA NO ESTABELECIMENTO"
    assert transactions[0].value == 1234.56

# def test_get_bill_period():
#     bill_date = date(2024, 9, 1)

#     reader = InterCreditCardReader()
#     bill_period = reader.get_bill_period(bill_date)

#     assert bill_period[0] == date(2023, 7, 26)
#     assert bill_period[1] == date(2024, 8, 25)