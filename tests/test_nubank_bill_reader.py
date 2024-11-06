import pytest

from src.readers.nubank_bill_reader import NubankBillReader
# Aux libs
from datetime import date
from decimal import Decimal

def test_read_bill_date():
    content = "VENCIMENTO: 01 DEZ 2023"
    reader = NubankBillReader()
    file_date = reader.read_bill_date(content)
    assert file_date == date(2023, 12, 1)


def test_read_bill_value():
    content = "no valor de R$ 1.665,24"
    reader = NubankBillReader()
    value = reader.read_bill_value(content)
    assert value == Decimal('1665.24')


def test_transform_to_transaction():
    reader = NubankBillReader()
    bill_date = date(2023, 12, 1)
    raw_transaction = ('25 NOV', None, 'Hering*Hering6166190 - 3/4', '54,99')
    
    transaction = reader.transform_to_transaction(raw_transaction, bill_date)

    assert transaction.date == date(2023, 11, 25)
    assert transaction.description == "Hering*Hering6166190 - 3/4"
    assert transaction.value == Decimal('54.99')


# def test_read_transactions():
#     content = """
#         30 out 2023 Taco Bell R$ 58,89
#         01 nov 2023 Pagto Debito Automatico + R$ 1.140,07
#         22 nov 2023 Amazon Marketplace R$ 111,70
#     """

#     reader = NubankBillReader()
#     transactions = reader.read_transactions(content)

#     assert len(transactions) == 3
#     assert [t.date for t in transactions] == [date(2023, 10, 30), date(2023, 11, 1), date(2023, 11, 22)]
#     assert [t.description for t in transactions] == ["Taco Bell", "Pagto Debito Automatico", "Amazon Marketplace"]
#     assert [t.value for t in transactions] == [58.89, -1140.07, 111.70]


def test_get_bill_period():
    reader = NubankBillReader()
    # TODO Add a test for the case where the bill starts in the last month of the year and ends in the first month of the next year
    bill_date = date(2024, 9, 1)
    period = reader.get_bill_period(bill_date)
    assert period == (date(2024, 7, 25), date(2024, 8, 24))