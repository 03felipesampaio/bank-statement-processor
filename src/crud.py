from sqlalchemy.orm import Session
from . import models
from .statement_readers import InterBankStatementFileReader, NubankBankStatementFileReader


def add_bank(db: Session, bank_name: str):
    new_bank = models.Bank(name=bank_name)
    db.add(new_bank)
    db.commit()

    return new_bank


def get_bank(db: Session, bank_name: str):
    return db.get(models.Bank, bank_name)


# def add_transaction(db: Session, transaction)


def insert_inter_bank_transactions_from_file(db: Session, file_name: str, file):
    statement = InterBankStatementFileReader(file_name, file)
    transactions = []
    for transaction in statement.transactions:
        transaction_model = models.Transaction(
            **transaction,
            bank='Inter'
        )
        transactions.append(transaction_model)
    db.add_all(transactions)
    db.commit()
    return statement.to_json()


def insert_nubank_transactions_from_file(db: Session, file_name: str, file):
    statement = NubankBankStatementFileReader(file_name, file)
    transactions = []
    for transaction in statement.transactions:
        transaction_model = models.Transaction(
            **transaction,
            bank='Nubank'
        )
        transactions.append(transaction_model)
    db.add_all(transactions)
    db.commit()
    return statement.to_json()