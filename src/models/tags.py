from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class TransactionTag (Base):
    __tablename__ = "transactions_tags"

    transaction = Column(String(64), ForeignKey("transactions.id"), primary_key=True)
    tag = Column(String(32), primary_key=True)
