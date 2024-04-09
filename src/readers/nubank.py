from fitz import Document
import re
from datetime import datetime, date
import arrow

from . import Reader, FileExtractor, CreditCardPDFReader
from .. import models, utils


class NubankCreditCardReader (CreditCardPDFReader):
    def __init__(self) -> None:
        pass
    
    def get_transactions(self, doc: Document):
        transactions = []
        for page in doc:
            tables = page.find_tables()
            for table in tables:
                transactions.extend(table.extract())
    
        return transactions
    
    def read_document_date(self, doc: Document):
        page_content = doc[1].get_text()
        date = arrow.get(page_content, 'DD MMM YYYY', locale='pt-BR').date()
        
        return date
    
    def get_bill_value(self, doc: Document):
        page_content = doc[0].get_text()
        value = re.search(r"no\s+valor\s+de\s+R\$\s+([\d\.]+,\d{2})", page_content).groups()[0]
        
        return utils.convert_brazilian_real_notation_to_decimal(value)
        
    def add_year_to_transaction_date(self, transaction_date, bill_date: date) -> date:
        if transaction_date == '':
            return None
        
        bill_year = bill_date.year
        
        # If bill is from January but transaction was in December we need to use last year
        if bill_date.month == 1 and 'DEZ' in transaction_date:
            bill_year = bill_year - 1
            
        transaction_datetime = arrow.get(transaction_date + ' ' + str(bill_date.year), 'DD MMM YYYY', locale='pt-BR').date()     
        
        return transaction_datetime
    
    def transform_to_transaction(self, raw_transaction: tuple[str, str, str, str], bill_date) -> models.Transaction:
        transaction_date = self.add_year_to_transaction_date(raw_transaction[0], bill_date)
        value = utils.convert_brazilian_real_notation_to_decimal(raw_transaction[3])
        return models.Transaction(transaction_date, 'Compra no crédito', raw_transaction[2], value)
    
    def read(self, document: Document) -> models.CreditCardBill:
        bill_date = self.read_document_date(document)
        bill_value = self.get_bill_value(document)
        
        credit_bill = models.CreditCardBill(bill_date, bill_value, (1,1))
        credit_bill.transactions = [self.transform_to_transaction(x, bill_date) for x in self.get_transactions(document)]
        
        return credit_bill