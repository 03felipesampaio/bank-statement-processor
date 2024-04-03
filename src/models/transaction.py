from datetime import date

class Transaction:
    def __init__(self, transaction_date: date, description: str, value: float, category: str|None = None) -> None:
        self.date = transaction_date
        self.description = description
        self.value = value
        self.category = category