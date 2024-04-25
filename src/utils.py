import re

def convert_brazilian_real_notation_to_decimal(brazilian_real_value: str) -> float:
    """
    Convert brazilian money notation to decimal value
    
    Ex.: 
        '-1,25' -> Decimal(-1.25)
        '25.000,00' -> Decimal(25000.00)
    """
    return float(re.sub(r'[^\d-]', '', brazilian_real_value)) / 100