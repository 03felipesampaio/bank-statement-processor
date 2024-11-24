from datetime import date
from fitz import Document, Page
import arrow
import re

from .credit_card_pdf_reader import CreditCardPDFReader
from .. import models
from .. import utils


class InterBillReader(CreditCardPDFReader):
    BILL_DATE_PATTERN = r"VENCIMENTO[\s\n]+(?P<date>\d{2}/\d{2}/\d{4})"
    BILL_VALUE_PATTERN = r"TOTAL (DESSA|DA SUA) FATURA[\s\n]+R\$[\s\n]+(?P<value>[\d.]+,\d{2})"
    CREDIT_CARD_HEADER_PATTERN = (
        r"\nCARTÃO (?P<first_digits>\d{4})\s+(?P<last_digits>\d{4})"
    )
    TRANSACTION_HEADER_PATTERN = r"DATA\s*MOVIMENTAÇÃO\s*VALOR"
    TRANSACTION_PATTERN = re.compile(
        r"""
        (?P<date>\d{2}\s+(de\s+)?\w{3}\.?\s+\d{4})  # Date in the format 'dd de mmm. yyyy' or 'dd mmm yyyy'
        \s+
        (?P<description>.+?)                  # Description of the transaction
        \s*-?\s*                              # Optional '-' between description and value
        (?P<value>\+?\s*R\$\s+[\d.]+\s*,\s*\d{2})  # Value in the format 'R$ xx,yy'
        """,
        re.VERBOSE|re.DOTALL
    )
    TOTAL_VALUE_FOOTER_PATTERN = re.compile(
        r"VALOR TOTAL CARTÃO (?P<last_digits>\d{4})"
    )
    
    def is_valid(self, document: Document) -> bool:
        """Checks if the document is a valid Inter bill.
        
        Args:
            document (Document): The document object.
            
        Returns:
            bool: True if the document is a valid Inter bill, False otherwise.
        """
        return "Resumo da fatura" in document[0].get_text()

    def find_resume_page(self, document: Document) -> Page:
        """Finds the page with billing information. Includind the bill date and value.
        
        Args:
            document (Document): The document object.
        
        Returns:
            Page: The page with billing information.
        """
        for page in document:
            if re.search(r"Resumo[\s\n]+da[\s\n]+fatura", page.get_text()):
                return page
        
        raise ValueError("Resume page not found in document")

    def read_bill_date(self, content: str) -> date:
        """Reads the bill date from the resume page.
        
        Args:
            content (str): The text content of the resume page.
            
        Returns:
            date: The bill date.
        """
        match = re.search(self.BILL_DATE_PATTERN, content, re.I)

        if match:
            bill_date = arrow.get(match.group(1), "DD/MM/YYYY").date()
        else:
            bill_date = None

        return bill_date

    def read_bill_value(self, content: str) -> float:
        """Reads the bill value from the resume page.
        
        Args:
            content (str): The text content of the resume page.
        
        Returns:
            float: The bill value.
        """
        value_string = re.search(self.BILL_VALUE_PATTERN, content, flags=re.I).group(2)
        return utils.convert_brazilian_real_notation_to_decimal(value_string)

    def check_if_page_has_credit_card_header(self, page_content: str) -> bool:
        return [
            match.groupdict()
            for match in re.finditer(
                r"\nCARTÃO (?P<first_digits>\d{4})\s+(?P<last_digits>\d{4})",
                page_content,
            )
        ]

    def read_transactions(self, content: str) -> list[models.Transaction]:
        """Reads the transactions from the page.
        
        Args:
            content (str): The text content of the page.
            
        Returns:
            list[Transaction]: The list of transactions.
            
        """
        transactions = []
        raw_transactions = re.finditer(self.TRANSACTION_PATTERN, content)

        for match in raw_transactions:
            row = match.groupdict()

            transactions.append(
                models.Transaction(
                    arrow.get(
                        re.sub(r" +", " ", row["date"]).replace(' de ', ' ').replace('.', ''), "DD MMM YYYY", locale="pt-BR"
                    ).date(),
                    None,
                    re.sub(r"\n\s*", "", row["description"]),
                    utils.convert_brazilian_real_notation_to_decimal(
                        re.sub(r" +", " ", row["value"]).replace("+", "-")
                    ),  # Consider bill payment as a negative value
                )
            )

        return transactions

    def get_bill_period(self, bill_date: date):
        """Returns the start and end date of the bill period.
        
        Source: https://ajuda.inter.co/cartao/qual-sera-a-data-de-vencimento-da-minha-fatura/
        
        Args:
            bill_date (date): The bill date.
        
        Returns:
            tuple[date, date]: The start and end date of the bill period.    
        """
        # https://ajuda.inter.co/cartao/qual-sera-a-data-de-vencimento-da-minha-fatura/
        start_date = arrow.get(bill_date).shift(months=-1, days=-7)
        end_date = arrow.get(bill_date).shift(days=-8)

        return start_date.date(), end_date.date()

    def read(self, document: Document) -> models.CreditCardBill:
        resume_page = self.find_resume_page(document)
        resume_page_content = resume_page.get_text()
        bill_date = self.read_bill_date(resume_page_content)
        bill_value = self.read_bill_value(resume_page_content)
        start_date, end_date = self.get_bill_period(bill_date)

        bill = models.CreditCardBill(
            "Inter", bill_date, bill_value, start_date, end_date
        )

        for i, page in enumerate(document):
            text = page.get_text()
            bill.transactions.extend(self.read_transactions(text))

        return bill


# if __name__ == "__main__":

# #     reader = InterBillReader()
# #     reader.read_transactions("""07 de out. 2024
# # P
# # AO DE QUEIJO MINEIRO
# # -
# # R$ 14,00""")
#     # (?P<value>\+?[\s\n]*R\$[\s\n]+[\d.]+[\s\n]*,[\s\n]*\d{2})
    
#     string = """07 de out. 2024
# P
# AO DE QUEIJO MINEIRO
# -
# R$ 14,00
# 07 de out. 2024
# Uber *UBER *TRIP
# -
# R$ 6,95
# 11 de out. 2024
# Uber *UBER *TRIP
# -
# R$ 13,90
# 12 de out. 2024
# ASA*FUTURO GESTAO FINA
# -
# R$ 59,90
# 15 de out. 2024
# Uber *UBER *TRIP
# -
# R$ 14,55
# 16 de out. 2024
# MonicaRosaPimenta
# -
# R$ 14,50
# 17 de out. 2024
# Uber *UBER *TRIP
# -
# R$ 6,80
# 18 de out. 2024
# MP *NAPOLESPIZZAR
# -
# R$ 69,89
# 18 de out. 2024
# Uber *UBER *TRIP
# -
# R$ 6,
# 15
# 19 de out. 2024
# Uber *UBER *TRIP
# -
# R$ 15,38
# 19 de out. 2024
# Uber *UBER *TRIP
# -
# R$ 6,90
# 19 de out. 2024
# Uber *UBER *TRIP
# -
# R$ 9,95
# 20 de out. 2024
# JAU SERVE LJ 32
# -
# R$ 11,99
# 21 de out. 2024
# MP *NAPOLESPIZZAR
# -
# R$ 60,89
# 21 de out. 2024
# Uber *UBER *TRIP
# -
# + R$ 9,90"""
#     TRANSACTION_PATTERN = re.compile(
#         r"(?P<date>\d{2}[\s\n]+(de[\s\n]+)?\w{3}\.?[\s\n]+\d{4})[\s\n]+(?P<description>.+?)[\s\n]+-\s*\+?R\$\s*(?P<value>[\d.,]+)"
#     )
#     # TRANSACTION_PATTERN = re.compile(
#     #     r"(?P<date>\d{2}[\s\n]+(de[\s\n]+)?\w{3}\.?[\s\n]+\d{4})[\s\n]+(?P<description>.+)[\s\n]+"
#     # )
    
#     # print(TRANSACTION_PATTERN.match("07 de out. 2024\nP\nAO DE QUEIJO MINEIRO\n-\nR$ 14,00").groupdict())
#     print(re.findall(TRANSACTION_PATTERN, string))