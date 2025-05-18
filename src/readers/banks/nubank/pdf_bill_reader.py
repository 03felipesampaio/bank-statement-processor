from src.models import CreditCardBillReader

class NubankPDFBillReader(CreditCardBillReader):
    bank = 'nubank'
    report_type = 'bill'
    accepted_mime_types = ['application/pdf']

    def read(self, file_content: bytes):
        ...