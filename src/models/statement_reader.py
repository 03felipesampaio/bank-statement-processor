from datetime import date
from decimal import Decimal
from src.models.report_reader import ReportReader
from src.models.transaction import Transaction
from src.models.bank_statement import BankStatement

class StatementReader (ReportReader):
    def read(self, file_content: bytes) -> BankStatement:
        pass

    def is_valid_file(self, file: bytes, mime_type:str) -> bool:
        raise NotImplementedError
    
    def get_transactions(self) -> list[Transaction]:
        raise NotImplementedError
    
    def get_ballance(self) -> Decimal:
        raise NotImplementedError
    
    def get_period(self) -> tuple[date, date]:
        raise NotImplementedError
    
    def get_account_id(self) -> str:
        raise NotImplementedError