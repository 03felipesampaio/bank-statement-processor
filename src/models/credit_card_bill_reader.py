from datetime import date
from decimal import Decimal
from src.models.report_reader import ReportReader
from src.models.transaction import Transaction
from src.models.credit_card_bill import CreditCardBill

class CreditCardBillReader (ReportReader):
    def read(self, file: bytes) -> CreditCardBill:
        pass

    def is_valid_file(self, file: bytes, mime_type:str) -> bool:
        raise NotImplementedError
    
    def get_reference_month(self) -> str:
        raise NotImplementedError

    def get_transactions(self) -> list[Transaction]:
        raise NotImplementedError
    
    def get_bill_ammount(self) -> Decimal:
        raise NotImplementedError
    
    def get_period(self) -> tuple[date, date]:
        raise NotImplementedError
    