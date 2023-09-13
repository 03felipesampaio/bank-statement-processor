from .statement_readers import InterBankStatementFileReader


def insert_inter_bank_transactions_from_file(file_name: str, file):
    statement = InterBankStatementFileReader(file_name, file)
    return statement.to_json()