from . import Transaction
from datetime import date

class CreditCardBill:
    def __init__(self, bank_name, bill_date: date, value: float, start_date: date, end_date: date, transactions: list[Transaction] = None) -> None:
        self.bank_name = bank_name
        self.bill_date = bill_date
        self.reference_month = bill_date.strftime('%Y-%m')
        self.value = value
        self.start_date = start_date
        self.end_date = end_date
        
        if not transactions:
            self.transactions: list[Transaction] = []
        else:
            self.transactions = transactions.copy()