from ofxparse import OfxParser
import arrow
from ..models import BankStatement, Transaction

class OFXReader:
    def read_transaction_from_ofx(self, ofx_transaction) -> Transaction:
        transaction = Transaction(
            ofx_transaction.date.date(),
            ofx_transaction.type,
            ofx_transaction.memo,
            ofx_transaction.amount,
        )

        return transaction

    def read(self, file_content) -> BankStatement:
        ofx = OfxParser.parse(file_content)

        account = ofx.account
        statement = account.statement

        bank_statement = BankStatement(
            account.institution.organization,
            statement.start_date.date(),
            statement.end_date.date(),
            account.account_id,
            [self.read_transaction_from_ofx(tr) for tr in statement.transactions]
        )

        return bank_statement