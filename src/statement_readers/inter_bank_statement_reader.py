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
        file_name (str): File name
        raw_file_content (File object): CSV file content
    """

    def __init__(self, file_name, raw_file_content) -> None:
        raw_rows = self._read_file(raw_file_content)

        try:
            self.statement_type = raw_rows[0][0].strip()
            self.account_number = raw_rows[1][1].strip()
            self.start_date, self.end_date = self._read_period(raw_rows[2][1])
            self.transactions = self._load_transactions(raw_rows[5:])
        except Exception as e:
            raise Exception(f"Error while trying to read file {file_name}, "
                            "are you sure that this file came from Inter Bank?") from e

    def _read_file(self, raw_file_content):
        return list(csv.reader((row for row in raw_file_content if row), delimiter=';'))

    def _read_period(self, raw_period_text: str):
        raw_start, raw_end = raw_period_text.split(' a ')
        start = datetime.strptime(raw_start, '%d/%m/%Y')
        end = datetime.strptime(raw_end, '%d/%m/%Y')

        return start, end

    def __clean_rows(self, row):
        row['date'] = datetime.strptime(row['date'], '%d/%m/%Y')
        row['type'] = row['type'].strip()
        row['description'] = row['description'].strip()
        row['value'] = convert_brazilian_real_notation_to_decimal(row['value'])
        
        return row

    def _load_transactions(self, raw_rows) -> list[dict]:
        header = ('date', 'type',
                  'description', 'value')

        rows = []

        for i, row in enumerate(raw_rows):
            try:
                rows.append(self.__clean_rows(dict(zip(header, row))))
            except Exception as e:
                raise Exception(f'Error while processing {i+1} transaction (Line {i+6} in csv file).') from e

        return rows
    
    def to_json(self):
        return {
            'statement_type': self.statement_type,
            'account_number': self.account_number,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'transactions': self.transactions
        }

