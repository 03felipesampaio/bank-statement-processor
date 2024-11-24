import pytest

from src.readers.inter_bill_reader import InterBillReader
from src.models import Transaction
from decimal import Decimal

# Aux libs
from datetime import date

@pytest.mark.parametrize("date_string, expected", [("VENCIMENTO\n01/12/2023", date(2023, 12, 1)), ("Data de Vencimento\n01/11/2024", date(2024, 11, 1))])
def test_read_bill_date(date_string, expected):
    reader = InterBillReader()
    file_date = reader.read_bill_date(date_string)
    assert file_date == expected


@pytest.mark.parametrize("total_string, expected", [
    ("TOTAL DESSA FATURA\nR$ 1.665,24", Decimal("1665.24")),
    ("Total da sua fatura\nR$ 12.799,41", Decimal("12799.41")),
])
def test_read_bill_value(total_string, expected):
    reader = InterBillReader()
    value = reader.read_bill_value(total_string)
    assert value == expected


@pytest.mark.parametrize(
    "transactions_string, expected",
    [
        (
            """
            30 out 2023 Taco Bell R$ 58,89
            01 nov 2023 Pagto Debito Automatico + R$ 1.140,07
            22 nov 2023 Amazon Marketplace R$ 111,70
            """,
            [
                Transaction(
                    date(2023, 10, 30),
                    None,
                    description="Taco Bell",
                    value=Decimal("58.89"),
                ),
                Transaction(
                    date(2023, 11, 1),
                    None,
                    description="Pagto Debito Automatico",
                    value=Decimal("-1140.07"),
                ),
                Transaction(
                    date(2023, 11, 22),
                    None,
                    description="Amazon Marketplace",
                    value=Decimal("111.70"),
                ),
            ],
        ),
        (
            """07 de out. 2024
            P
            AO DE QUEIJO MINEIRO
            -
            R$ 14,00
            11 de out. 2024
            Uber *UBER *TRIP
            -
            R$ 13,90
            12 de out. 2024
            SER*SOME SERVICE
            -
            R$ 59,
            90
            15 de out. 2024
            Uber *UBER *TRIP
            -
            R$ 14,55
            16 de out. 2024
            ESTORNO
            -
            + R$ 14,50
            01 de out. 2024 
            P
            AGTO DEBITO AUTOMATICO 
            - 
            + R$ 1.576,20
            """,
            [
                Transaction(
                    date(2024, 10, 7),
                    None,
                    description="PAO DE QUEIJO MINEIRO",
                    value=Decimal("14.00"),
                ),
                Transaction(
                    date(2024, 10, 11),
                    None,
                    description="Uber *UBER *TRIP",
                    value=Decimal("13.90"),
                ),
                Transaction(
                    date(2024, 10, 12),
                    None,
                    description="SER*SOME SERVICE",
                    value=Decimal("59.90"),
                ),
                Transaction(
                    date(2024, 10, 15),
                    None,
                    description="Uber *UBER *TRIP",
                    value=Decimal("14.55"),
                ),
                Transaction(
                    date(2024, 10, 16),
                    None,
                    description="ESTORNO",
                    value=Decimal("-14.50"),
                ),
                Transaction(
                    date(2024, 10, 1),
                    None,
                    description="PAGTO DEBITO AUTOMATICO",
                    value=Decimal("-1576.20"),
                ),
            ],
        ),
    ],
)
def test_read_transactions(transactions_string, expected):
    reader = InterBillReader()
    transactions = reader.read_transactions(transactions_string)

    assert len(transactions) == len(expected)
    assert all([a == b for a, b in zip(transactions, expected)])


def test_get_bill_period():
    reader = InterBillReader()
    # TODO Add a test for the case where the bill starts in the last month of the year and ends in the first month of the next year
    bill_date = date(2024, 9, 1)
    period = reader.get_bill_period(bill_date)
    assert period == (date(2024, 7, 25), date(2024, 8, 24))
