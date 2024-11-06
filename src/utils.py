import re
from decimal import Decimal

def convert_brazilian_real_notation_to_decimal(brazilian_real_value: str) -> Decimal:
    """
    Convert brazilian money notation to decimal value
    
    Ex.: 
        '-1,25' -> Decimal(-1.25)
        '25.000,00' -> Decimal(25000.00)
    """
    value_without_point = re.sub(r'[^\d-]', '', brazilian_real_value)
    return Decimal(value_without_point[:-2]+'.'+value_without_point[-2:])