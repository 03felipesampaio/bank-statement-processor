from datetime import datetime, date
from fitz import Document

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


class InterCreditCardReader:
    def read_document_date(self, document):
        return date.today()
    
    def read(self, document: Document) -> InterCreditCardBill:
        bill_date = self.read_document_date(document)
        value = 100.0
        
        for i, page in enumerate(document):
            with open(f'inter_pdf_pages\\page_{i}.json', 'w') as fp:
                json = page.get_text('json')
                fp.write(json)
            
            with open(f'inter_html_pages\\page_{i}.html', 'w') as fp:
                json = page.get_text('html')
                fp.write(json)
        
        bill = InterCreditCardBill(bill_date, value, (1,1))
        
        return bill