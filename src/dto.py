from pydantic import BaseModel


class Transaction (BaseModel):
    date: str
    description: str
    value: float