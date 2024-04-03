from fastapi import FastAPI, UploadFile
import fitz

from src.dto import Transaction
# from src.readers.inter_statement import InterStatementReader
from src.readers import Reader, CSVExtractor, NubankCreditCardReader
from src.readers.inter import InterCreditCardReader
from src.repository import read_file

app = FastAPI()

@app.get("/")
def hello_world():
    return 'Hello World'


@app.post("/nubank/fatura") # , response_model=list[Transaction]
def read_nubank_credit_card_bill(file: UploadFile):
    contents = file.file.read()#.decode('utf8')
    document = fitz.Document(stream=contents)
    
    return NubankCreditCardReader().read(document)


@app.post("/nubank/extrato/csv") # , response_model=list[Transaction]
def read_nubank_statement(file: UploadFile):
    # Open file
    contents = file.file.read().decode('utf8')
    transactions = read_file(contents, Reader(CSVExtractor()))
    
    return transactions


@app.post("/inter/fatura") # , response_model=list[Transaction]
def read_inter_credit_card_bill(file: UploadFile, file_password: str):
    contents = file.file.read()
    document = fitz.Document(stream=contents)
    document.authenticate(file_password)
    
    return InterCreditCardReader().read(document)


@app.post("/inter/extrato") # , response_model=list[Transaction]
def read_inter_statement(file: UploadFile):
    # Open file
    contents = file.file.read().decode('utf8')
    transactions = read_file(contents, Reader(CSVExtractor(sep=';', skiprows=5, decimal=',', thousands='.')))
    
    return transactions