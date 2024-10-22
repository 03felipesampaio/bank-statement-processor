import pandas as pd
from src import file_types
import datetime
from src.models import BankStatement, Transaction
from src.models import BankStatement, CreditCardBill, Transaction
import io
import csv


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


def test_write_bill_as_csv():
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

    # Write the bill to a CSV file
    file_content = file_types.write_bill_as("csv", bill)

    # Check the file content
    assert isinstance(file_content, io.BytesIO)
    file_content.seek(0)
    csv_content = file_content.read().decode("utf-8")
    csv_reader = csv.DictReader(io.StringIO(csv_content))

    rows = list(csv_reader)
    assert len(rows) == 2  # 2 transactions

    assert rows[0]["bank_name"] == "Test Bank"
    assert rows[0]["bill_date"] == "2023-01-31"
    assert rows[0]["bill_reference_month"] == "2023-01"
    assert rows[0]["bill_value"] == "150.0"
    assert rows[0]["bill_start_date"] == "2023-01-01"
    assert rows[0]["bill_end_date"] == "2023-01-31"
    assert rows[0]["transaction_date"] == "2023-01-01"
    assert rows[0]["transaction_type"] == "purchase"
    assert rows[0]["transaction_description"] == "Electronics Store"
    assert rows[0]["transaction_value"] == "-200.0"
    assert rows[0]["transaction_category"] == "Electronics"

    assert rows[1]["bank_name"] == "Test Bank"
    assert rows[1]["transaction_date"] == "2023-01-02"
    assert rows[1]["transaction_type"] == "refund"
    assert rows[1]["transaction_description"] == "Returned Item"
    assert rows[1]["transaction_value"] == "50.0"
    assert rows[1]["transaction_category"] == "Refund"


def test_write_bill_as_xlsx():
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

    # Write the bill to an XLSX file
    file_content = file_types.write_bill_as("xlsx", bill)

    # Check the file content
    assert isinstance(file_content, io.BytesIO)
    file_content.seek(0)
    df = pd.read_excel(file_content, sheet_name="Bill")

    assert df.shape == (2, 11)  # 2 transactions, 11 columns

    assert df.iloc[0]["bank_name"] == "Test Bank"
    assert df.iloc[0]["bill_date"] == pd.Timestamp("2023-01-31")
    assert df.iloc[0]["bill_reference_month"] == "2023-01"
    assert df.iloc[0]["bill_value"] == 150.0
    assert df.iloc[0]["bill_start_date"] == pd.Timestamp("2023-01-01")
    assert df.iloc[0]["bill_end_date"] == pd.Timestamp("2023-01-31")
    assert df.iloc[0]["transaction_date"] == pd.Timestamp("2023-01-01")
    assert df.iloc[0]["transaction_type"] == "purchase"
    assert df.iloc[0]["transaction_description"] == "Electronics Store"
    assert df.iloc[0]["transaction_value"] == -200.0
    assert df.iloc[0]["transaction_category"] == "Electronics"

    assert df.iloc[1]["bank_name"] == "Test Bank"
    assert df.iloc[1]["transaction_date"] == pd.Timestamp("2023-01-02")
    assert df.iloc[1]["transaction_type"] == "refund"
    assert df.iloc[1]["transaction_description"] == "Returned Item"
    assert df.iloc[1]["transaction_value"] == 50.0
    assert df.iloc[1]["transaction_category"] == "Refund"


def test_write_statement_as_csv():
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

    # Write the statement to a CSV file
    file_content = file_types.write_statement_as("csv", statement)

    # Check the file content
    assert isinstance(file_content, io.BytesIO)
    file_content.seek(0)
    csv_content = file_content.read().decode("utf-8")
    csv_reader = csv.DictReader(io.StringIO(csv_content))

    rows = list(csv_reader)
    assert len(rows) == 2  # 2 transactions

    assert rows[0]["bank_name"] == "Test Bank"
    assert rows[0]["statement_start_date"] == "2023-01-01"
    assert rows[0]["statement_end_date"] == "2023-01-31"
    assert rows[0]["statement_account_id"] == "123456789"
    assert rows[0]["transaction_date"] == "2023-01-01"
    assert rows[0]["transaction_type"] == "debit"
    assert rows[0]["transaction_description"] == "Grocery Store"
    assert rows[0]["transaction_value"] == "-50.0"
    assert rows[0]["transaction_category"] == "Groceries"

    assert rows[1]["bank_name"] == "Test Bank"
    assert rows[1]["transaction_date"] == "2023-01-02"
    assert rows[1]["transaction_type"] == "credit"
    assert rows[1]["transaction_description"] == "Salary"
    assert rows[1]["transaction_value"] == "1500.0"
    assert rows[1]["transaction_category"] == "Income"


def test_write_statement_as_xlsx():
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

    # Write the statement to an XLSX file
    file_content = file_types.write_statement_as("xlsx", statement)

    # Check the file content
    assert isinstance(file_content, io.BytesIO)
    file_content.seek(0)
    df = pd.read_excel(file_content, sheet_name="Statement")

    assert df.shape == (2, 9)  # 2 transactions, 9 columns

    assert df.iloc[0]["bank_name"] == "Test Bank"
    assert df.iloc[0]["statement_start_date"] == pd.Timestamp("2023-01-01")
    assert df.iloc[0]["statement_end_date"] == pd.Timestamp("2023-01-31")
    assert str(df.iloc[0]["statement_account_id"]) == "123456789"
    assert df.iloc[0]["transaction_date"] == pd.Timestamp("2023-01-01")
    assert df.iloc[0]["transaction_type"] == "debit"
    assert df.iloc[0]["transaction_description"] == "Grocery Store"
    assert df.iloc[0]["transaction_value"] == -50.0
    assert df.iloc[0]["transaction_category"] == "Groceries"

    assert df.iloc[1]["bank_name"] == "Test Bank"
    assert df.iloc[1]["transaction_date"] == pd.Timestamp("2023-01-02")
    assert df.iloc[1]["transaction_type"] == "credit"
    assert df.iloc[1]["transaction_description"] == "Salary"
    assert df.iloc[1]["transaction_value"] == 1500.0
    assert df.iloc[1]["transaction_category"] == "Income"
