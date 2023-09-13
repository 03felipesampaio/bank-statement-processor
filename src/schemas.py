from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class InterTransaction (BaseModel):
    date: datetime
    type: str
    description: str
    value: Decimal


class InterStatement (BaseModel):
    account_number: str
    start_date: datetime
    end_date: datetime
    
    transactions: list[InterTransaction]