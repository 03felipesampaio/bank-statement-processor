import fitz

from .. import models

class CreditCardPDFReader:
    def read(self, document: fitz.Document) -> models.CreditCardBill:
        raise NotImplementedError