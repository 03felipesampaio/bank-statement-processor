from datetime import datetime, date
from fitz import Document, Page
import re

from ..models import Transaction


class InterCreditCardBill:
    def __init__(self, bill_date: datetime, value: float, period_of_bill: tuple[datetime, datetime], transactions: list[Transaction] = None) -> None:
        self.bill_date = bill_date
        self.value = value
        self.period_of_bill = period_of_bill
        
        if not transactions:
            self.transactions: list[Transaction] = []
        else:
            self.transactions = transactions.copy()

    # def add_credit_card(self, first_digi)


class InterCreditCardReader:
    CREDIT_CARD_HEADER_PATTERN = r'\nCARTÃO (?P<first_digits>\d{4})\s+(?P<last_digits>\d{4})'
    TRANSACTION_HEADER_PATTERN = r'DATA\s*MOVIMENTAÇÃO\s*VALOR'
    TRANSACTION_PATTERN = re.compile(
        r'(?P<date>\d{2} \w{3} \d{4})[\s\n]+(?P<description>[^\n]+)[\s\n]+(?P<value>R\$[\s\n]+\d+[\s\n]*,[\s\n]*\d{2})')
    TOTAL_VALUE_FOOTER_PATTERN = re.compile(
        r'VALOR TOTAL CARTÃO (?P<last_digits>\d{4})'
    )

    def read_document_date(self, document):
        return date.today()
    
    def check_if_page_has_credit_card_header(self, page_content: str) -> bool:
        return [match.groupdict() for match in re.finditer(r'\nCARTÃO (?P<first_digits>\d{4})\s+(?P<last_digits>\d{4})', page_content)]
    
    def read_transactions_header(self, page_content: str):
        return None
    
    def read(self, document: Document) -> InterCreditCardBill:
        bill_date = self.read_document_date(document)
        value = 100.0
        
        for i, page in enumerate(document):
            # with open(f'inter_pdf_pages\\page_{i}.json', 'w') as fp:
            #     json = page.get_text('json')
            #     fp.write(json)
            
            # with open(f'inter_html_pages\\page_{i}.html', 'w') as fp:
            #     html = page.get_text('html')
            #     fp.write(html)

            with open(f'inter_text_pages\\page_{i}.txt', 'w', encoding='utf8') as fp:
                text = page.get_text()
                fp.write(text)

                # print(self.check_if_page_has_credit_card_header(text))
                print([x for x in re.findall(self.TRANSACTION_PATTERN, text)])
                # print([x for x in re.findall(self.TOTAL_VALUE_FOOTER_PATTERN, text)])
        
        bill = InterCreditCardBill(bill_date, value, (1,1))
        
        return bill