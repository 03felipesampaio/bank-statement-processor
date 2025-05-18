from .base_exporter import BaseExporter, ExportedFile
from src.models import CreditCardBill
import io

import pandas as pd
from csv import QUOTE_NONNUMERIC

class CreditCardBillExporter(BaseExporter):
    supported_file_types = ['json', 'csv', 'excel', 'parquet']
    
    def export_bill_to_json(self, bill: CreditCardBill) -> ExportedFile:
        return bill

    def export_bill_to_dataframe(self, bill: CreditCardBill) -> pd.DataFrame:
        """Converts a Bill object to a pandas DataFrame."""
        df = pd.DataFrame(
            [
                {
                    "bank_name": bill.bank_name,
                    "bill_date": bill.bill_date,
                    "bill_reference_month": bill.reference_month,
                    "bill_value": bill.value,
                    "bill_start_date": bill.start_date,
                    "bill_end_date": bill.end_date,
                    "transaction_date": t.date,
                    "transaction_type": t.type,
                    "transaction_description": t.description,
                    "transaction_value": t.value,
                    "transaction_category": t.category,
                }
                for t in bill.transactions
            ]
        )

        return df

    def export_bill_to_csv(self, bill: CreditCardBill) -> ExportedFile:
        df = self.export_bill_to_dataframe(bill)

        mem_file = io.BytesIO()
        df.to_csv(mem_file, index=False, quoting=QUOTE_NONNUMERIC)

        return ExportedFile(
            file_name=f"{bill.reference_month}_{bill.bank_name}_bill.csv",
            file_content=mem_file.getvalue(),
            file_type="text/csv",
        )

    def export_bill_to_excel(self, bill: CreditCardBill) -> ExportedFile:
        df = self.export_bill_to_dataframe(bill)

        mem_file = io.BytesIO()
        df.to_excel(
            mem_file,
            sheet_name="Bill",
            index=False,
            float_format="%.2f",
            freeze_panes=(1, 0),
        )

        return ExportedFile(
            file_name=f"{bill.reference_month}_{bill.bank_name}_bill.xlsx",
            file_content=mem_file.getvalue(),
            file_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def export_bill_to_parquet(self, bill: CreditCardBill) -> ExportedFile:
        df = self.export_bill_to_dataframe(bill)

        mem_file = io.BytesIO()
        df.to_parquet(mem_file, index=False)

        return ExportedFile(
            file_name=f"{bill.reference_month}_{bill.bank_name}_bill.parquet",
            file_content=mem_file.getvalue(),
            file_type="application/octet-stream",
        )
