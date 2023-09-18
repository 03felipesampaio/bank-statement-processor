from fastapi import FastAPI, HTTPException, Depends, UploadFile
from sqlalchemy.orm import Session

from src import crud, schemas, models
from src.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_main_page() -> str:
    return "Hello World!"


@app.post("/banks/{bank_name}", response_model=schemas.Bank, status_code=201)
def add_bank(bank_name: str, db: Session = Depends(get_db)):
    bank = crud.add_bank(db, bank_name)

    return bank


@app.get("/banks/{bank_name}", response_model=schemas.Bank)
def get_bank(bank_name: str, db: Session = Depends(get_db)):
    return crud.get_bank(db, bank_name)


@app.post("/banks/inter/statements", response_model=schemas.InterStatement, status_code=201)
def insert_inter_statement_transactions_from_file(statement_file: UploadFile, db: Session = Depends(get_db)):
    file_content = statement_file.file.read().decode().split('\n')
    statement = crud.insert_inter_bank_transactions_from_file(db, statement_file.filename, file_content)
    return statement


@app.post("/banks/nubank/statements", response_model=schemas.NubankStatement, status_code=201)
def insert_nubank_statement_transactions_from_file(statement_file: UploadFile, db: Session = Depends(get_db)):
    file_content = statement_file.file.read().decode().split('\n')
    statement = crud.insert_nubank_transactions_from_file(db, statement_file.filename, file_content)
    return statement
