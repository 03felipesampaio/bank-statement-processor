from fastapi import FastAPI, UploadFile
from contextlib import asynccontextmanager
import fitz
import os
import logging
from pathlib import Path
import json
import atexit
import time

from src import dto

# from src.readers.inter_statement import InterStatementReader
from src.readers import NubankBillReader, OFXReader
from src.readers.inter_bill_reader import InterBillReader


logger = logging.getLogger("statement_processor")


def setup_logging():
    log_dir_path = Path(__file__).parent / "logs"
    log_dir_path.mkdir(exist_ok=True)

    config_file = Path(__file__).parent / "log_config.json"
    logging.config.dictConfig(json.loads(config_file.read_text()))


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(lifespan=lifespan)


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
    start_time = time.time()
    logger.info(f"Reading Nubank's bill file '{bill.filename}'")
    contents = bill.file.read()  # .decode('utf8')
    document = fitz.Document(stream=contents)
    bill = NubankBillReader().read(document)
    end_time = time.time()
    logger.info(f"Processed Nubank's bill file '{bill.filename}' in {end_time - start_time:.2f} seconds")
    return bill


@app.post("/nubank/statements", response_model=dto.BankStatement, tags=["Nubank"])
async def read_nubank_statement_ofx(statement: UploadFile):
    """Read Nubank statement from OFX file.
    You can export yout statement from Nubank app to your email
    and then load it here.

    This is the most recommended way to load your statement.
    """
    start_time = time.time()
    logger.info(f"Reading Nubank's statement file '{statement.filename}'")
    contents = statement.file
    bank_statement = OFXReader().read(contents)
    end_time = time.time()
    logger.info(f"Processed Nubank's statement file '{statement.filename}' in {end_time - start_time:.2f} seconds")
    return bank_statement


@app.post("/inter/bills", response_model=dto.CreditCardBill, tags=["Inter"])
async def read_inter_credit_card_bill(bill: UploadFile, file_password: str):
    """Read Inter credit card bill from PDF file.
    You can find your bill files in your email."""
    start_time = time.time()
    logger.info(f"Reading Inter's bill file '{bill.filename}'")
    contents = bill.file.read()
    document = fitz.Document(stream=contents)
    document.authenticate(file_password)
    bill = InterBillReader().read(document)
    end_time = time.time()
    logger.info(f"Processed Inter's bill file '{bill.filename}' in {end_time - start_time:.2f} seconds")
    return bill


@app.post("/inter/statements", response_model=dto.BankStatement, tags=["Inter"])
async def read_inter_statement_ofx(statement: UploadFile):
    """Read Inter statement from OFX file.
    You can export your statement from the bank app
    or from the bank web page.

    This is the most recommend way of loading your statement.


    The statements extracted from the bank web page have more information.
    """
    start_time = time.time()
    logger.info(f"Reading Inter's statement file '{statement.filename}'")
    contents = statement.file

    # Gambiarra total rsrsrs
    # CONSERTAR ISSO PELO AMOR DE DEUS
    # Create a temporary file to fix encoding problem
    with open("inter_temp.ofx", "wb") as fp:
        fp.write(contents.read())
    with open("inter_temp.ofx", "r", encoding="utf8") as fp:
        bank_statement = OFXReader().read(fp)
    os.unlink("inter_temp.ofx")
    end_time = time.time()
    logger.info(f"Processed Inter's statement file '{statement.filename}' in {end_time - start_time:.2f} seconds")
    return bank_statement
