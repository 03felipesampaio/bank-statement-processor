from fitz import Document
from datetime import date

from .. import models

class CreditCardPDFReader:
    def read(self, document: Document) -> models.CreditCardBill:
        pass
    
    def read_bill_date(self, content: str) -> date:
        pass
    
    def read_bill_value(self, content: str) -> float:
        pass
    
    def read_period(self, bill_date: date) -> tuple[date, date]:
        pass
    
    def read_transactions(self, content) -> list[models.Transaction]:
        pass