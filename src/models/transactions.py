from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import DECIMAL, Date
from sqlalchemy.orm import relationship
from ..database import Base


class Transaction (Base):
    __tablename__ = "transactions"

    id = Column(String(64), primary_key=True)
    date = Column(Date, index=True, nullable=False)
    bank = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    value = Column(DECIMAL(15, 2), nullable=False)
