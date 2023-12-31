import csv
from pathlib import Path
from datetime import datetime
import decimal

# Set to money precision
decimal.getcontext().prec = 2


def convert_brazilian_real_notation_to_decimal(brazilian_real_value: str):
    """
    Convert brazilian money notation to decimal value
    
    Ex.: 
        '-1,25' -> Decimal(-1.25)
        '25.000,00' -> Decimal(25000.00)
    """
    reais, cents = brazilian_real_value.split(',')
    reais = reais.replace('.', '')
    return decimal.Decimal('.'.join((reais, cents)))

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

    def __clean_rows(self, row):
        row['transaction_date'] = datetime.strptime(row['transaction_date'], '%d/%m/%Y')
        row['transaction_type'] = row['transaction_type'].strip()
        row['transaction_description'] = row['transaction_description'].strip()
        row['transaction_value'] = convert_brazilian_real_notation_to_decimal(row['transaction_value'])
        
        return row

    def _load_transactions(self, raw_rows) -> list[dict]:
        header = ('transaction_date', 'transaction_type',
                  'transaction_description', 'transaction_value')
        rows = raw_rows[1:]

        return [self.__clean_rows(dict(zip(header, row))) for row in rows]

