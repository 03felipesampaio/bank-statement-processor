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


class BankStatement (BaseModel):
    bank_name: str
    start_date: date
    end_date: date
    account_id: str

    transactions: list[Transaction]