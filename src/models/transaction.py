from datetime import date

class Transaction:
    def __init__(self, transaction_date: date, transaction_type: str|None, description: str, value: float, category: str|None = None) -> None:
        self.date = transaction_date
        self.type = transaction_type
        self.description = description
        self.value = value
        self.category = category