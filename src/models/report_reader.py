class ReportReader:
    bank = None
    report_type = None
    accepted_mime_types = None

    def __init__(self) -> None:
        if not self.bank or not self.report_type or not self.accepted_mime_types:
            raise ValueError('When creating a ReportReader implementation, you must set the bank, report_type and accepted_mime_types before calling the constructor')
    
    def read(self, file_content: bytes):
        raise NotImplementedError