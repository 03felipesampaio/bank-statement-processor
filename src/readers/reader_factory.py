import src.models as models
from src.readers.banks.inter.pdf_billl_reader import InterPDFBillReader
from src.readers.banks.nubank.pdf_bill_reader import NubankPDFBillReader

class ReaderFactory:
    def __init__(self) -> None:
        self.readers: list[models.ReportReader] = [
            InterPDFBillReader,
            NubankPDFBillReader
        ]

    def get_reader(self, bank, file_type, file_format) -> models.ReportReader:
        for reader in self.reader:
            if bank == reader.bank and file_type == reader.report_type and file_format in reader.accepted_mime_types:
                return reader()