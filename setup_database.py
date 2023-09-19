from src.database import Base
from src import models

from sqlalchemy.orm import Session


def setup_banks(db: Session):
    for bank in ['nubank', 'inter']:
        if db.get(models.Bank, bank):
            continue
        db.add(models.Bank(name=bank))
    db.commit()


def setup_transaction_types(db: Session):
    types = [
        'Pix recebido',
        'Pix enviado',
        'Investimento',
        'Pagamento de fatura',
        'Compra no credito',
        'Compra no debito'
    ]

    for _type in types:
        if db.get(models.TransactionTypes, _type):
            continue
        db.add(models.TransactionTypes(type=_type))

    db.commit()


def setup_database(db: Session):
    print(f"Starting database setup")
    Base.metadata.create_all(bind=db.connection())
    setup_banks(db)
    setup_transaction_types(db)
    print("Ended database setup")