from .readers import Reader
from .models import Transaction

from typing import Type

def read_file(file_content: str, FileReader: Reader) -> list[Transaction]:
    raw_data = FileReader.read(file_content)
    
    return raw_data