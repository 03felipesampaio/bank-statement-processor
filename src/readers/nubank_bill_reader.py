import json
import fitz
import re
from datetime import datetime, date
import arrow

from . import CreditCardPDFReader
from .. import models, utils


class NubankBillReader(CreditCardPDFReader):
    """Reads a Nubank credit card bill from a PDF file.
    
    Pass a fitz.Document object to the read method to get a CreditCardBill object with all billing information.
    """
    
    def __init__(self) -> None:
        pass
    
    
    def is_valid(self, document: fitz.Document) -> bool:
        """Checks if the document is a valid Nubank bill.
        
        Args:
            document (fitz.Document): The document object.
            
        Returns:
            bool: True if the document is a valid Nubank bill, False otherwise.
        """
        # TODO Only the more recent bills have the "Esta é a sua fatura" string in the first page
        # return "Esta é a sua fatura" in document[0].get_text().lower()
        return True

    # def get_transactions(self, doc: fitz.Document):
    #     transactions = []
    #     for page in doc:
    #         tables = page.find_tables()
    #         for table in tables:
    #             transactions.extend(table.extract())

    #     # Removes all blank rows
    #     transactions = [row for row in transactions if not all((field == '' for field in row))]

    #     return transactions

    def read_bill_date(self, content: str) -> date:
        """Reads the bill date from the first page of the document.

        Args:
            content (str): The content of the first page of the document.

        Returns:
            date: The bill date.
        """
        match = re.search(
            r"VENCIMENTO:?\s+(?P<date>\d{2}\s+\w{3}\s+\d{4})",
            content,
            flags=re.IGNORECASE,
        )
        if not match:
            raise ValueError("Bill date not found in page")

        date_string = match.groupdict()["date"]
        bill_date = arrow.get(date_string, "DD MMM YYYY", locale="pt-BR").date()

        return bill_date

    def read_bill_value(self, content: str) -> float:
        """Reads the bill value from the first page of the document.
        
        Args:
            content (str): The content string of the first page of the document.
            
        Returns:
            float: The bill value.
        """
        match = re.search(r"no\s+valor\s+de\s+R\$\s+([\d\.]+,\d{2})", content)

        if not match:
            raise ValueError("Bill value not found in page")

        value = utils.convert_brazilian_real_notation_to_decimal(match.groups()[0])

        return value

    def get_bill_period(self, bill_date: date):
        """Gets the start and end date of the bill period.
        
        Nubank bills are closed 7 days before the bill date. Source:
        https://blog.nubank.com.br/data-de-vencimento-data-fechamento-cartao-de-credito/
        
        Args:
            bill_date (date): The bill date.
            
        Returns:
            tuple[date, date]: A tuple with the start and end date of the bill period
        """
        # https://blog.nubank.com.br/data-de-vencimento-data-fechamento-cartao-de-credito/
        start_date = arrow.get(bill_date).shift(months=-1, days=-7)
        end_date = arrow.get(bill_date).shift(days=-8)

        return start_date.date(), end_date.date()

    def add_year_to_transaction_date(self, transaction_date, bill_date: date) -> date:
        if transaction_date == "":
            return None

        bill_year = bill_date.year

        # If bill is from January but transaction was in December we need to use last year
        if bill_date.month == 1 and "DEZ" in transaction_date:
            bill_year = bill_year - 1

        transaction_datetime = arrow.get(
            transaction_date + " " + str(bill_date.year), "DD MMM YYYY", locale="pt-BR"
        ).date()

        return transaction_datetime

    def transform_to_transaction(
        self, raw_transaction: tuple[str, str, str, str], bill_date
    ) -> models.Transaction:
        """Transforms a raw transaction tuple into a Transaction object.

        Args:
            raw_transaction (tuple[str, str, str, str]): A tuple with the raw transaction data. The fields are:
                - date: The transaction date.
                - category: The transaction category.
                - description: The transaction description.
                - value: The transaction value.
            bill_date (date): The bill date.
        
        Returns:
            models.Transaction: A Transaction object.
        """

        # The date is in the format "DD MMM", so we need to add the year
        transaction_date = self.add_year_to_transaction_date(
            raw_transaction[0], bill_date
        )

        value = utils.convert_brazilian_real_notation_to_decimal(raw_transaction[3])
        
        # Sometimes a row comes with empty date field and a reference date in description, so we use it as the date
        if transaction_date is None and re.match(r"\d{2} \w{3}\b", raw_transaction[2]):
            match = re.match(r"\d{2} \w{3}\b", raw_transaction[2]).group(0)
            transaction_date = self.add_year_to_transaction_date(match, bill_date)

        return models.Transaction(transaction_date, None, raw_transaction[2], value)

    def read_transactions(self, document: fitz.Document) -> list[models.Transaction]:
        """Reads the transactions from the document.
        
        Iterates through the pages of the document and extracts the transactions.
        
        Args:
            document (fitz.Document): The document object.
            
        Returns:
            list[models.Transaction]: A list of transactions.
        """
        # Green color: (108, 192, 13)
        # Color used to highlight positive transactions
        # Transactions with this color have inverted signal
        POSITIVE_TRANSACTION_GREEN = (108, 192, 13)
        POSITIVE_TRANSACTION_GREEN_SINCE_2024_06 = (12, 121, 57)
        transactions = []

        # https://pymupdf.readthedocs.io/en/latest/recipes-text.html#how-to-extract-text-with-color
        # Iter through pages and search for specic color font
        for page in document:
            text_blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]
            for block in text_blocks:
                if len(block["lines"]) != 3:
                    continue

                date_span, descr_span, value_span = map(
                    lambda x: x["spans"][0], block["lines"]
                )
                
                value_match = re.match(r"(?P<signal>-)?(?P<coin>R\$)\s+(?P<value>\d+,\d{2})", value_span["text"])

                if not re.match(r"\d{2} \w{3}", date_span["text"]) or not value_match:
                    continue
                
                value_dict = value_match.groupdict()
                
                # Positive transactions are highlighted in green, so we need to invert the signal case the signal is not explicit
                if fitz.sRGB_to_rgb(value_span["color"]) == POSITIVE_TRANSACTION_GREEN or fitz.sRGB_to_rgb(value_span["color"]) == POSITIVE_TRANSACTION_GREEN_SINCE_2024_06:
                    value = "-" + value_span["text"] if value_dict["signal"] is None else value_span["text"]
                else:
                    value = value_span["text"]

                # TODO Still cant get category, so for now category will be set to None
                transaction = (date_span["text"], None, descr_span["text"], value)
                transactions.append(transaction)

        return transactions

    def read(self, document: fitz.Document) -> models.CreditCardBill:
        bill_date = self.read_bill_date(document[0].get_text())
        bill_value = self.read_bill_value(document[0].get_text())
        start_date, end_date = self.get_bill_period(bill_date)

        credit_bill = models.CreditCardBill(
            "Nubank", bill_date, bill_value, start_date, end_date
        )
        credit_bill.transactions = [self.transform_to_transaction(t, bill_date) for t in self.read_transactions(document)]

        return credit_bill
