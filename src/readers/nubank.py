from fitz import Document
import re
from datetime import datetime
import arrow

from . import Reader, FileExtractor
from ..models import Transaction


# class NubankCreditCardReaderExtractor (FileExtractor):
    # def open()

def convert_brazilian_real_notation_to_decimal(brazilian_real_value: str) -> float:
    """
    Convert brazilian money notation to decimal value
    
    Ex.: 
        '-1,25' -> Decimal(-1.25)
        '25.000,00' -> Decimal(25000.00)
    """
    return float(re.sub(r'[^\d-]', '', brazilian_real_value)) / 100



class NubankTransaction:
    def __init__(self, date, description, category, value) -> None:
        pass


class NubankCreditCardBill:
    def __init__(self, bill_date: datetime, value: float, period_of_bill: tuple[datetime, datetime], transactions: list[NubankTransaction] = None) -> None:
        self.bill_date = bill_date
        self.value = value
        self.period_of_bill = period_of_bill
        
        if not transactions:
            self.transactions: list[NubankTransaction] = []
        else:
            self.transactions = transactions.copy()


class NubankCreditCardReader:
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
        # try:
        #     date_string = re.search("EMISSÃO E ENVIO\s+(\d{2} \w{3} \d{4})", page_content).groups()[0]
        # except AttributeError:
        #     return datetime(2022, 1, 1)
        # date = datetime.strptime(date_string, '%d %b %Y')
        return date
    
    def get_bill_value(self, doc: Document):
        page_content = doc[0].get_text()
        value = re.search(r"no\s+valor\s+de\s+R\$\s+([\d\.]+,\d{2})", page_content).groups()[0]
        
        return convert_brazilian_real_notation_to_decimal(value)
        
    def add_year_to_transaction_date(self, transaction_date, bill_date) -> datetime:
        if transaction_date == '':
            return None
        
        if bill_date.month == 1 and 'DEZ' in transaction_date:
            transaction_datetime = arrow.get(transaction_date + ' ' + str(bill_date.year-1), 'DD MMM YYYY', locale='pt-BR')
        else:
            transaction_datetime = arrow.get(transaction_date + ' ' + str(bill_date.year), 'DD MMM YYYY', locale='pt-BR')        
        
        return transaction_datetime.date()
    
    def transform_to_transaction(self, raw_transaction: tuple[str, str, str, str], bill_date) -> Transaction:
        transaction_date = self.add_year_to_transaction_date(raw_transaction[0], bill_date)
        value = convert_brazilian_real_notation_to_decimal(raw_transaction[3])
        return Transaction(transaction_date, raw_transaction[2], value)
    
    def read(self, document: Document) -> NubankCreditCardBill:
        bill_date = self.read_document_date(document)
        bill_value = self.get_bill_value(document)
        
        credit_bill = NubankCreditCardBill(bill_date, bill_value, (1,1))
        credit_bill.transactions = [self.transform_to_transaction(x, bill_date) for x in self.get_transactions(document)]
        
        return credit_bill