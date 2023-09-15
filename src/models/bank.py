from sqlalchemy import Column, Integer, String
from ..database import Base


class Bank (Base):
    __tablename__ = "banks"

    name = Column(String(50), primary_key=True)