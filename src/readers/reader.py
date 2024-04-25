from typing import Callable, Type, Any, Iterable
import pandas as pd
from io import StringIO
import fitz

from ..models import Transaction


class FileExtractor:
    def __init__(self) -> None:
        pass
    
    def extract(self, content: Any) -> list:
        raise NotImplemented 


class CSVExtractor (FileExtractor):
    def __init__(self, sep=',', skiprows: int|None = None, thousands: str = ',', decimal:str = '.') -> None:
        self.sep = sep
        self.skiprows = skiprows
        self.thousands = thousands
        self.decimal = decimal
        
    def extract(self, content: Any) -> Iterable:
        rows = pd.read_csv(StringIO(content), sep=self.sep, skiprows=self.skiprows, thousands=self.thousands, decimal = self.decimal).to_dict(orient='records')
        return rows
    
    
class PDFExtractor (FileExtractor):
    def extract(self, content: bytes) -> list:
        return fitz.Document(stream=content)


class Reader:
    def __init__(self, extractor: FileExtractor, convert_to_transactions: Callable[[Any], Transaction] = lambda x:x) -> None:
        self.transactions = None
        self.extractor = extractor
        self.convert_to_transactions = convert_to_transactions
        
    def read(self, content) -> list[Transaction]:
        raw_transactions = self.extractor.extract(content)
        
        transactions = [self.convert_to_transactions(transaction) for transaction in raw_transactions]
        
        return transactions
        



# class ReaderFactory:
#     def __init__(self) -> None:
#         self.Inter