from .statement_readers import InterBankStatementFileReader, NubankBankStatementFileReader


def insert_inter_bank_transactions_from_file(file_name: str, file):
    statement = InterBankStatementFileReader(file_name, file)
    return statement.to_json()


def insert_nubank_transactions_from_file(file_name: str, file):
    statement = NubankBankStatementFileReader(file_name, file)
    return statement.to_json()