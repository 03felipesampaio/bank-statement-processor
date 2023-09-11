import csv
from pathlib import Path
from datetime import datetime


class InterBankStatementFileReader:
    """
    Reads a csv file from Inter Banking
    containing transactions over a period
    of time.

    Arguments:
        file_path (Path or str): CSV file path
    """

    def __init__(self, file_path: Path | str) -> None:
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        raw_rows = self._read_file(file_path)

        try:
            self.statement_type = raw_rows[0][0].strip()
            self.account_number = raw_rows[1][1].strip()
            self.start, self.end = self._read_period(raw_rows[2][1])
            self.transactions = self._load_transactions(raw_rows[4:])
        except Exception as e:
            raise Exception(f"Error while trying to read file {file_path.name}, "
                            "are you sure that this file came from Inter Bank") from e

    def _read_file(self, file_path):
        with open(file_path, newline='') as csv_file:
            return list(csv.reader(csv_file, delimiter=';'))

    def _read_period(self, raw_period_text: str):
        raw_start, raw_end = raw_period_text.split(' a ')
        start = datetime.strptime(raw_start, '%d/%m/%Y')
        end = datetime.strptime(raw_end, '%d/%m/%Y')
        
        return start, end
    
    def _load_transactions(self, raw_rows) -> list[dict]:
        header = raw_rows[0]
        rows = raw_rows[1:]
        
        return [dict(zip(header, row)) for row in rows]
