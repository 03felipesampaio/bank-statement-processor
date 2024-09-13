from datetime import date
from src.readers.nubank import NubankCreditCardReader

def test_read_document_date():
    reader = NubankCreditCardReader()
    content = "VENCIMENTO: 01 OUT 2023"
    assert reader.read_document_date(content) == date(2023, 10, 1)

def test_get_bill_value():
    reader = NubankCreditCardReader()
    content = "no valor de R$ 1.234,56"
    assert reader.get_bill_value(content) == 1234.56

# def test_bill_period():
#     reader = NubankCreditCardReader()
#     bill_date = date(2023, 10, 1)
#     bill_period = reader.get_bill_period(bill_date)

#     assert bill_period[0] == date(2023, 9, 24)
#     assert bill_period[1] == date(2023, 10, 1)\

def test_add_year_to_transaction_date():
    reader = NubankCreditCardReader()
    bill_date = date(2024, 2, 1)
    assert reader.add_year_to_transaction_date('29 DEZ', bill_date) == date(2023, 12, 29)
    assert reader.add_year_to_transaction_date('01 JAN', bill_date) == date(2024, 1, 1)

# def test_read_transactions():
#     reader = NubankCreditCardReader()
#     content = "29 DEZ\nCOMPRA NO ESTABELECIMENTO\nR$ 1.234,56"
#     transactions = reader.read_transactions(content)

#     assert transactions[0].date == date(2023, 12, 29)
#     assert transactions[0].description == "COMPRA NO ESTABELECIMENTO"
#     assert transactions[0].value == 1234.56