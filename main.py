from fastapi import FastAPI, UploadFile
import fitz
import os

from src import dto

# from src.readers.inter_statement import InterStatementReader
from src.readers import Reader, CSVExtractor, NubankBillReader, OFXReader
from src.readers.inter import InterCreditCardReader
from src.repository import read_file

app = FastAPI()


@app.get("/")
def hello_world():
    return "Hello World"


@app.post("/nubank/bills", response_model=dto.CreditCardBill, tags=["Nubank"])
def read_nubank_credit_card_bill(bill: UploadFile):
    """Read Nubank credit card bill from PDF file.
    You can find your bill files in your email.
    """
    contents = bill.file.read()  # .decode('utf8')
    document = fitz.Document(stream=contents)

    return NubankBillReader().read(document)


@app.post("/nubank/statements/csv", tags=["Nubank"])
def read_nubank_statement_csv(statement: UploadFile):
    """Read Nubank statement from CSV file.
    You can export yout statement from Nubank app to your email
    and then load it here."""
    # Open file
    contents = statement.file.read().decode("utf8")
    transactions = read_file(contents, Reader(CSVExtractor()))

    return transactions


@app.post("/nubank/statements/ofx", response_model=dto.BankStatement, tags=["Nubank"])
def read_nubank_statement_ofx(statement: UploadFile):
    """Read Nubank statement from OFX file.
    You can export yout statement from Nubank app to your email
    and then load it here.

    This is the most recommended way to load your statement.
    """
    # Open file
    contents = statement.file
    bank_statement = OFXReader().read(contents)
    return bank_statement


@app.post("/inter/bills", response_model=dto.CreditCardBill, tags=["Inter"])
def read_inter_credit_card_bill(bill: UploadFile, file_password: str):
    """Read Inter credit card bill from PDF file.
    You can find your bill files in your email."""
    contents = bill.file.read()
    document = fitz.Document(stream=contents)
    document.authenticate(file_password)

    return InterCreditCardReader().read(document)


@app.post("/inter/statements", tags=["Inter"])
def read_inter_statement(statement: UploadFile):
    """Read Inter statement from CSV file."""
    # Open file
    contents = statement.file.read().decode("utf8")
    transactions = read_file(
        contents, Reader(CSVExtractor(sep=";", skiprows=5, decimal=",", thousands="."))
    )

    return transactions


@app.post("/inter/statements/ofx", response_model=dto.BankStatement, tags=["Inter"])
def read_inter_statement_ofx(statement: UploadFile):
    """Read Inter statement from OFX file.
    You can export your statement from the bank app
    or from the bank web page.

    This is the most recommend way of loading your statement.


    The statements extracted from the bank web page have more information.
    """
    # Open file
    contents = statement.file

    # Gambiarra total rsrsrs
    # CONSERTAR ISSO PELO AMOR DE DEUS
    # Create a temporary file to fix encoding problem
    with open("inter_temp.ofx", "wb") as fp:
        fp.write(contents.read())
    with open("inter_temp.ofx", "r", encoding="utf8") as fp:
        bank_statement = OFXReader().read(fp)
    os.unlink("inter_temp.ofx")

    return bank_statement
