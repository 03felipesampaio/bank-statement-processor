from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class TransactionTypes (Base):
    __tablename__ = "transaction_types"

    type = Column(String(50), nullable=False, primary_key=True)