from fastapi import FastAPI, UploadFile
import fitz
import os

from src import dto
# from src.readers.inter_statement import InterStatementReader
from src.readers import Reader, CSVExtractor, NubankCreditCardReader, OFXReader
from src.readers.inter import InterCreditCardReader
from src.repository import read_file

app = FastAPI()

@app.get("/")
def hello_world():
    return 'Hello World'


@app.post("/nubank/fatura", response_model=dto.CreditCardBill)
def read_nubank_credit_card_bill(file: UploadFile):
    contents = file.file.read()#.decode('utf8')
    document = fitz.Document(stream=contents)
    
    return NubankCreditCardReader().read(document)


@app.post("/nubank/extrato/csv")
def read_nubank_statement_csv(file: UploadFile):
    # Open file
    contents = file.file.read().decode('utf8')
    transactions = read_file(contents, Reader(CSVExtractor()))
    
    return transactions


@app.post("/nubank/extrato/ofx", response_model=dto.BankStatement)
def read_nubank_statement_ofx(file: UploadFile):
    # Open file
    contents = file.file
    bank_statement = OFXReader().read(contents)
    return bank_statement


@app.post("/inter/fatura", response_model=dto.CreditCardBill)
def read_inter_credit_card_bill(file: UploadFile, file_password: str):
    contents = file.file.read()
    document = fitz.Document(stream=contents)
    document.authenticate(file_password)
    
    return InterCreditCardReader().read(document)


@app.post("/inter/extrato")
def read_inter_statement(file: UploadFile):
    # Open file
    contents = file.file.read().decode('utf8')
    transactions = read_file(contents, Reader(CSVExtractor(sep=';', skiprows=5, decimal=',', thousands='.')))
    
    return transactions


@app.post("/inter/extrato/ofx", response_model=dto.BankStatement)
def read_inter_statement_ofx(file: UploadFile):
    # Open file
    contents = file.file
    
    # Gambiarra total rsrsrs
    # CONSERTAR ISSO PELO AMOR DE DEUS
    # Create a temporary file to fix encoding problem
    with open('inter_temp.ofx', 'wb') as fp:
        fp.write(contents.read())
    with open('inter_temp.ofx', 'r', encoding='utf8') as fp:
        bank_statement = OFXReader().read(fp)
    os.unlink('inter_temp.ofx')
    
    return bank_statement