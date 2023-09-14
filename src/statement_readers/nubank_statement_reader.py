import csv
from pathlib import Path
from datetime import datetime
import decimal

# Set to money precision
decimal.getcontext().prec = 2


class NubankBankStatementFileReader:
    def __init__(self, file_name, raw_file_content) -> None:
        raw_rows = self._read_file(raw_file_content)

        try:
            self.transactions = self._load_transactions(raw_rows[1:])
            self.start_date = min(self.transactions, key=lambda x: x['date'])['date']
            self.end_date = max(self.transactions, key=lambda x: x['date'])['date']
        except Exception as e:
            raise Exception(f"Error while trying to read file {file_name}, "
                            "are you sure that this file came from NuBank?") from e
        
    def _read_file(self, raw_file_content):
        return list(csv.reader((row for row in raw_file_content if row), delimiter=','))

    
    def __clean_row(self, row):
        row['date'] = datetime.strptime(row['date'], '%d/%m/%Y')
        row['value'] = decimal.Decimal(row['value'])

        return row
    
    def _load_transactions(self, raw_rows):
        header = ('date', 'value',
                  'id', 'description')
        
        rows = []

        for i, row in enumerate(raw_rows):
            try:
                rows.append(self.__clean_row(dict(zip(header, row))))
            except Exception as e:
                raise Exception(f'Error while processing {i+1} transaction (Line {i+1} in csv file).') from e

        return rows
