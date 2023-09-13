from fastapi import FastAPI, HTTPException, UploadFile

from src.statement_readers import InterBankStatementFileReader
from src import crud, schemas

app = FastAPI()


@app.get("/")
def get_main_page() -> str:
    return "Hello World!"


@app.post("/banks/inter/statements", response_model=schemas.InterStatement, status_code=201)
def insert_inter_statement_transactions_from_file(statement_file: UploadFile):
    file_content = statement_file.file.read().decode().split('\n')
    statement = crud.insert_inter_bank_transactions_from_file(statement_file.filename, file_content)
    return statement