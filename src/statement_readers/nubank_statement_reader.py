import csv
from pathlib import Path
from datetime import datetime
import decimal

# Set to money precision
decimal.getcontext().prec = 2


class NubankBankStatementFileReader:
    def __init__(self, file_name, raw_file_content) -> None:
        raw_rows = self._read_file(raw_file_content)

    def _read_file(self, raw_file_content):
        return list(csv.reader((row for row in raw_file_content if row), delimiter=';'))