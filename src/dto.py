from pydantic import BaseModel, Field, AliasGenerator, ConfigDict
from pydantic.alias_generators import to_camel
import datetime


class Transaction(BaseModel):
    date: datetime.date = Field(..., description='The date of the transaction')
    type: str | None = Field(..., description='The type of the transaction, e.g., debit or credit')
    description: str = Field(..., description='A brief description of the transaction')
    category: str | None = Field(..., description='The category of the transaction, e.g., groceries, utilities')
    value: float = Field(..., description='The monetary value of the transaction')
    

class CreditCardBill(BaseModel):
    model_config = ConfigDict(
            alias_generator=AliasGenerator(
                serialization_alias=to_camel,
            )
        )
    
    bank_name: str = Field(..., description='The name of the bank issuing the credit card')
    reference_month: str = Field(..., description='The reference month for the credit card bill, formatted as "YYYY-MM"')
    bill_date: datetime.date = Field(..., description='The date the bill was due')
    start_date: datetime.date = Field(..., description='The start date of the billing period')
    end_date: datetime.date = Field(..., description='The end date of the billing period')
    value: float = Field(..., description='The total value of the credit card bill')
    transactions: list[Transaction] = Field(..., description='A list of transactions included in the bill')


class BankStatement(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_camel,
        )
    )
    
    bank_name: str = Field(..., description='The name of the bank issuing the statement')
    start_date: datetime.date = Field(..., description='The start date of the statement period')
    end_date: datetime.date = Field(..., description='The end date of the statement period')
    # account_id: str

    transactions: list[Transaction] = Field(..., description='A list of transactions included in the statement')