from datetime import date
from . import Transaction

class BankStatement:
    def __init__(self, bank_name: str, start_date: date, end_date: date, account_id: str, transactions: list[Transaction] = None) -> None:
        self.bank_name = bank_name
        self.start_date = start_date
        self.end_date = end_date
        self.account_id = account_id

        if not transactions:
            self.transactions: list[Transaction] = []
        else:
            self.transactions = transactions