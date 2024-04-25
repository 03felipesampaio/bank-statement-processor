from . import Transaction
from datetime import date

class CreditCardBill:
    def __init__(self, bank_name, bill_date: date, value: float, period_of_bill: tuple[date, date], transactions: list[Transaction] = None) -> None:
        self.bank_name = bank_name
        self.bill_date = bill_date
        self.reference_month = bill_date.strftime('%Y-%m')
        self.value = value
        self.period_of_bill = period_of_bill
        
        if not transactions:
            self.transactions: list[Transaction] = []
        else:
            self.transactions = transactions.copy()