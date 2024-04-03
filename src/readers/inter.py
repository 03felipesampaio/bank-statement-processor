from datetime import datetime, date
from fitz import Document, Page
import arrow
import re
import itertools

from .. import models
from .. import utils

class InterCreditCardReader:
    BILL_DATE_PATTERN = r'VENCIMENTO[\s\n]+(?P<date>\d{2}/\d{2}/\d{4})'
    BILL_VALUE_PATTERN = r'TOTAL DESSA FATURA[\s\n]+R\$[\s\n]+(?P<value>[\d.]+,\d{2})'
    CREDIT_CARD_HEADER_PATTERN = r'\nCARTÃO (?P<first_digits>\d{4})\s+(?P<last_digits>\d{4})'
    TRANSACTION_HEADER_PATTERN = r'DATA\s*MOVIMENTAÇÃO\s*VALOR'
    TRANSACTION_PATTERN = re.compile(
        r'(?P<date>\d{2} \w{3} \d{4})[\s\n]+(?P<description>[^\n]+)[\s\n]+(?P<value>\+?[\s\n]*R\$[\s\n]+\d+[\s\n]*,[\s\n]*\d{2})')
    TOTAL_VALUE_FOOTER_PATTERN = re.compile(
        r'VALOR TOTAL CARTÃO (?P<last_digits>\d{4})'
    )
    
    def get_page(self, document: Document, page_number: int) -> Page:
        return next(itertools.islice(document.pages(), page_number, page_number+1))

    def read_bill_date(self, content) -> date:
        date_string = re.search(self.BILL_DATE_PATTERN, content).group(1)
        return arrow.get(date_string, 'DD/MM/YYYY').date()
    
    def read_bill_value(self, content) -> float:
        value_string = re.search(self.BILL_VALUE_PATTERN, content).group(1)
        return utils.convert_brazilian_real_notation_to_decimal(value_string)
    
    def check_if_page_has_credit_card_header(self, page_content: str) -> bool:
        return [match.groupdict() for match in re.finditer(r'\nCARTÃO (?P<first_digits>\d{4})\s+(?P<last_digits>\d{4})', page_content)]
    
    def read_transactions_header(self, page_content: str):
        return None
    
    def read_transactions(self, content: str) -> list[models.Transaction]:
        transactions = []
        raw_transactions = re.finditer(self.TRANSACTION_PATTERN, content)
        
        for match in raw_transactions:
            transactions.append(
                models.Transaction(
                    arrow.get(match.groupdict()['date'], 'DD MMM YYYY', locale='pt-BR').date(),
                    match.groupdict()['description'],
                    utils.convert_brazilian_real_notation_to_decimal(
                        match.groupdict()['value'].replace('+', '-'))  # Consider bill payment as a negative value
                )
            )
        
        return transactions
    
    def read(self, document: Document) -> models.CreditCardBill:
        first_page = self.get_page(document, 0)
        bill_date = self.read_bill_date(first_page.get_text())
        bill_value = self.read_bill_value(first_page.get_text())
        
        bill = models.CreditCardBill(bill_date, bill_value, (1,1))
        
        for i, page in enumerate(document):
            text = page.get_text()
            bill.transactions.extend(self.read_transactions(text))

        return bill