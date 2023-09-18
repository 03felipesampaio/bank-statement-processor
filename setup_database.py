from src.database import Base, SessionLocal, engine
from src import models

from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)


def setup_banks(db: Session):
    db.add(models.Bank(name='nubank'))
    db.add(models.Bank(name='inter'))
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
        db.add(models.TransactionTypes(type=_type))

    db.commit()


if __name__ == '__main__':
    with SessionLocal() as session:
        setup_banks(session)
        setup_transaction_types(session)