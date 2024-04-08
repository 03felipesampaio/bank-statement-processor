from ofxparse import OfxParser
import arrow
from ..models import BankStatement, Transaction

class OFXReader:
    def read_transaction_from_ofx(self, ofx_transaction) -> Transaction:
        transaction = Transaction(
            ofx_transaction.date,
            ofx_transaction.memo,
            ofx_transaction.amount,
            ofx_transaction.type
        )

        print(ofx_transaction.date,)

        return transaction

    def read(self, file_content) -> BankStatement:
        ofx = OfxParser.parse(file_content)
        # print(f'{dir(ofx)=}')
        # print(f'{dir(ofx.accounts)=}')
        # print(f'{dir(ofx.account)=}')

        account = ofx.account
        statement = account.statement

        bank_statement = BankStatement(
            account.institution,
            statement.start_date,
            statement.end_date,
            account.account_id,
            [self.read_transaction_from_ofx(tr) for tr in statement.transactions]
        )

        return bank_statement