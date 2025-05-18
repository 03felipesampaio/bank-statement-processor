from src.models import CreditCardBill

class InterPDFBillReader(CreditCardBill):
    bank = 'inter'
    report_type = 'bill'
    accepted_mime_types = ['application/pdf']

    def read(self, file_content: bytes):
        ...