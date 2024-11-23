from datetime import date


class Transaction:
    def __init__(
        self,
        transaction_date: date,
        transaction_type: str | None,
        description: str,
        value: float,
        category: str | None = None,
    ) -> None:
        self.date = transaction_date
        self.type = transaction_type
        self.description = description
        self.value = value
        self.category = category

    def __eq__(self, value):
        return (
            self.date == value.date
            and self.type == value.type
            and self.description == value.description
            and self.value == value.value
            and self.category == value.category
        )
