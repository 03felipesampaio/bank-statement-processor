from fastapi import FastAPI, UploadFile
import fitz
import os

from src import dto

# from src.readers.inter_statement import InterStatementReader
from src.readers import NubankBillReader, OFXReader
from src.readers.inter_bill_reader import InterBillReader

app = FastAPI()


@app.get("/")
async def hello_world():
    return (
        "Welcome to Bank Statement Processor. "
        "For more info go to /docs or directly to repository "
        "https://github.com/03felipesampaio/bank-statement-processor"
    )


@app.post("/nubank/bills", response_model=dto.CreditCardBill, tags=["Nubank"])
async def read_nubank_credit_card_bill(bill: UploadFile):
    """Read Nubank credit card bill from PDF file.
    You can find your bill files in your email.
    """
    contents = bill.file.read()  # .decode('utf8')
    document = fitz.Document(stream=contents)

    return NubankBillReader().read(document)


@app.post("/nubank/statements", response_model=dto.BankStatement, tags=["Nubank"])
async def read_nubank_statement_ofx(statement: UploadFile):
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
async def read_inter_credit_card_bill(bill: UploadFile, file_password: str):
    """Read Inter credit card bill from PDF file.
    You can find your bill files in your email."""
    contents = bill.file.read()
    document = fitz.Document(stream=contents)
    document.authenticate(file_password)

    return InterBillReader().read(document)


@app.post("/inter/statements", response_model=dto.BankStatement, tags=["Inter"])
async def read_inter_statement_ofx(statement: UploadFile):
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
