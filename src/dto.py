from pydantic import BaseModel
from datetime import date


class Transaction (BaseModel):
    date: date
    description: str
    category: str|None
    value: float
    

class CreditCardBill (BaseModel):
    bill_date: date
    value: float
    
    transactions: list[Transaction]