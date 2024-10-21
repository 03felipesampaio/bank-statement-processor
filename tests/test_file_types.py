import pandas as pd
from src import file_types
import datetime
from src.models import BankStatement, Transaction
from src.models import BankStatement, CreditCardBill, Transaction


def test_bill_to_dataframe():
    # Placeholder test for bill_to_dataframe
    # Create a mock CreditCardBill object
    transactions = [
        Transaction(
            transaction_date=datetime.date(2023, 1, 1),
            transaction_type="purchase",
            description="Electronics Store",
            value=-200.0,
            category="Electronics",
        ),
        Transaction(
            transaction_date=datetime.date(2023, 1, 2),
            transaction_type="refund",
            description="Returned Item",
            value=50.0,
            category="Refund",
        ),
    ]
    bill = CreditCardBill(
        bank_name="Test Bank",
        bill_date=datetime.date(2023, 1, 31),
        value=150.0,
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 1, 31),
        transactions=transactions,
    )

    # Convert the bill to a DataFrame
    df = file_types.bill_to_dataframe(bill)

    # Check the DataFrame structure
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 11)  # 2 transactions, 11 columns

    # Check the DataFrame content
    assert df.iloc[0]["bank_name"] == "Test Bank"
    assert df.iloc[0]["bill_date"] == datetime.date(2023, 1, 31)
    assert df.iloc[0]["bill_reference_month"] == "2023-01"
    assert df.iloc[0]["bill_value"] == 150.0
    assert df.iloc[0]["bill_start_date"] == datetime.date(2023, 1, 1)
    assert df.iloc[0]["bill_end_date"] == datetime.date(2023, 1, 31)
    assert df.iloc[0]["transaction_date"] == datetime.date(2023, 1, 1)
    assert df.iloc[0]["transaction_type"] == "purchase"
    assert df.iloc[0]["transaction_description"] == "Electronics Store"
    assert df.iloc[0]["transaction_value"] == -200.0
    assert df.iloc[0]["transaction_category"] == "Electronics"

    assert df.iloc[1]["bank_name"] == "Test Bank"
    assert df.iloc[1]["transaction_date"] == datetime.date(2023, 1, 2)
    assert df.iloc[1]["transaction_type"] == "refund"
    assert df.iloc[1]["transaction_description"] == "Returned Item"
    assert df.iloc[1]["transaction_value"] == 50.0
    assert df.iloc[1]["transaction_category"] == "Refund"


def test_statement_to_dataframe():
    # Create a mock BankStatement object
    transactions = [
        Transaction(
            transaction_date=datetime.date(2023, 1, 1),
            transaction_type="debit",
            description="Grocery Store",
            value=-50.0,
            category="Groceries",
        ),
        Transaction(
            transaction_date=datetime.date(2023, 1, 2),
            transaction_type="credit",
            description="Salary",
            value=1500.0,
            category="Income",
        ),
    ]
    statement = BankStatement(
        bank_name="Test Bank",
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 1, 31),
        account_id="123456789",
        transactions=transactions,
    )

    # Convert the statement to a DataFrame
    df = file_types.statement_to_dataframe(statement)

    # Check the DataFrame structure
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 9)  # 2 transactions, 9 columns

    # Check the DataFrame content
    assert df.iloc[0]["bank_name"] == "Test Bank"
    assert df.iloc[0]["transaction_date"] == datetime.date(2023, 1, 1)
    assert df.iloc[0]["transaction_type"] == "debit"
    assert df.iloc[0]["transaction_description"] == "Grocery Store"
    assert df.iloc[0]["transaction_value"] == -50.0
    assert df.iloc[0]["transaction_category"] == "Groceries"

    assert df.iloc[1]["bank_name"] == "Test Bank"
    assert df.iloc[1]["transaction_date"] == datetime.date(2023, 1, 2)
    assert df.iloc[1]["transaction_type"] == "credit"
    assert df.iloc[1]["transaction_description"] == "Salary"
    assert df.iloc[1]["transaction_value"] == 1500.0
    assert df.iloc[1]["transaction_category"] == "Income"
