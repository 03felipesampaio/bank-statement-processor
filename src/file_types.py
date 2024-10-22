##############

# The purpose of this file is to define converters for bills and statements
# Statements and bills should be converted to Excel sheet, CSV and OFX file formats

##############
from . import models

import pandas as pd
from typing import Literal
import csv
import io
import datetime


FILE_FORMAT = Literal["csv", "xlsx", "ofx", "parquet"]


def bill_to_dataframe(bill: models.CreditCardBill) -> pd.DataFrame:
    """Converts a Bill object to a pandas DataFrame."""
    df = pd.DataFrame(
        [
            {
                "bank_name": bill.bank_name,
                "bill_date": bill.bill_date,
                "bill_reference_month": bill.reference_month,
                "bill_value": bill.value,
                "bill_start_date": bill.start_date,
                "bill_end_date": bill.end_date,
                "transaction_date": t.date,
                "transaction_type": t.type,
                "transaction_description": t.description,
                "transaction_value": t.value,
                "transaction_category": t.category,
            }
            for t in bill.transactions
        ]
    )

    return df


def statement_to_dataframe(statement: models.BankStatement) -> pd.DataFrame:
    """Converts a BankStatement object to a pandas DataFrame."""
    df = pd.DataFrame(
        [
            {
                "bank_name": statement.bank_name,
                "statement_start_date": statement.start_date,
                "statement_end_date": statement.end_date,
                "statement_account_id": statement.account_id,
                "transaction_date": t.date,
                "transaction_type": t.type,
                "transaction_description": t.description,
                "transaction_value": t.value,
                "transaction_category": t.category,
            }
            for t in statement.transactions
        ]
    )

    return df


def write_bill_as(file_format: FILE_FORMAT, bill: models.CreditCardBill) -> io.BytesIO:
    """Converts a Bill object to a file in the specified format.

    Args:
        file_format: The format of the file to be generated ("csv", "xlsx", "ofx", "parquet").
        bill: The Bill object to be converted.

    Returns:
        The file content as a BytesIO object.
    """

    file_content = io.BytesIO()

    if file_format == "csv":
        df = bill_to_dataframe(bill)
        df.to_csv(file_content, index=False, quoting=csv.QUOTE_NONNUMERIC)
    elif file_format == "xlsx":
        df = bill_to_dataframe(bill)
        df.to_excel(
            file_content,
            sheet_name="Bill",
            index=False,
            float_format="%.2f",
            freeze_panes=(1, 0),
        )
    elif file_format == "parquet":
        df = bill_to_dataframe(bill)
        df.to_parquet(file_content, index=False)
    elif file_format == "ofx":
        raise NotImplementedError("OFX file format is not yet supported")

    return file_content


def write_statement_as(
    file_format: FILE_FORMAT, statement: models.BankStatement
) -> io.BytesIO:
    """Converts a BankStatement object to a file in the specified format.

    Args:
        file_format: The format of the file to be generated ("csv", "xlsx", "ofx", "parquet").
        statement: The Bill object to be converted.

    Returns:
        The file content as a BytesIO object.
    """

    file_content = io.BytesIO()

    if file_format == "csv":
        df = statement_to_dataframe(statement)
        df.to_csv(file_content, index=False, quoting=csv.QUOTE_NONNUMERIC)
    elif file_format == "xlsx":
        df = statement_to_dataframe(statement)
        df.to_excel(
            file_content,
            sheet_name="Statement",
            index=False,
            float_format="%.2f",
            freeze_panes=(1, 0),
        )
    elif file_format == "parquet":
        df = statement_to_dataframe(statement)
        df.to_parquet(file_content, index=False)
    elif file_format == "ofx":
        raise NotImplementedError("OFX file format is not yet supported")

    return file_content


if __name__ == "__main__":
    transactions = [
        models.Transaction(
            transaction_date=datetime.date(2023, 1, 1),
            transaction_type="purchase",
            description="Electronics Store",
            value=-200.0,
            category="Electronics",
        ),
        models.Transaction(
            transaction_date=datetime.date(2023, 1, 2),
            transaction_type="refund",
            description="Returned Item",
            value=50.0,
            category="Refund",
        ),
    ]
    bill = models.CreditCardBill(
        bank_name="Test Bank",
        bill_date=datetime.date(2023, 1, 31),
        value=150.0,
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 1, 31),
        transactions=transactions,
    )

    file_content = write_bill_as("csv", bill)

    with open("files/test_bill.csv", "wb") as f:
        f.write(file_content.getvalue())

    file_content = write_bill_as("xlsx", bill)

    with open("files/test_bill.xlsx", "wb") as f:
        f.write(file_content.getvalue())

    with open('files/test_bill.parquet', 'wb') as f:
        file_content = write_bill_as("parquet", bill)
        f.write(file_content.getvalue())
