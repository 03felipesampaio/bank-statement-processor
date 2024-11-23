from fastapi import FastAPI, HTTPException, UploadFile, Depends
from fastapi.responses import Response, HTMLResponse
from contextlib import asynccontextmanager
import fitz
import os
import logging
from pathlib import Path
import json
import time
from enum import Enum

from src import dto, file_types, file_to_response

# from src.readers.inter_statement import InterStatementReader
from src.readers import NubankBillReader, OFXReader
from src.readers.inter_bill_reader import InterBillReader


logger = logging.getLogger("statement_processor")


class OUTPUT_FILE_TYPE(str, Enum):
    JSON = "json"
    CSV = "csv"
    XLSX = "xlsx"
    PARQUET = "parquet"
    # OFX = "OFX"


def setup_logging():
    log_dir_path = Path(__file__).parent / "logs"
    log_dir_path.mkdir(exist_ok=True)

    config_file = Path(__file__).parent / "log_config.json"
    logging.config.dictConfig(json.loads(config_file.read_text()))


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def hello_world():
    html_content = Path('./landing_page.html').read_text()
    return HTMLResponse(content=html_content, status_code=200)
    # return (
    #     "Welcome to Bank Statement Processor. "
    #     "For more info go to /docs or directly to repository "
    #     "https://github.com/03felipesampaio/bank-statement-processor"
    # )


@app.post(
    "/nubank/bills",
    # response_model=dto.CreditCardBill,
    tags=["Nubank"],
    responses={
        400: {
            "description": "Invalid content type, must be a PDF file and a Nubank bill"
        }
    },
)
async def read_nubank_credit_card_bill(
    upload_file: UploadFile,
    output_format: OUTPUT_FILE_TYPE = OUTPUT_FILE_TYPE.JSON,
):
    """Read Nubank credit card bill from PDF file.
    You can find your bill files in your email.
    """
    start_time = time.time()
    logger.info(f"Reading Nubank's bill file '{upload_file.filename}'")

    if upload_file.content_type != "application/pdf":
        logger.error(f"Invalid content type for Nubank's bill file '{upload_file.filename}'")
        raise HTTPException(
            400,
            f"Invalid content type. The file must be a PDF. Got '{upload_file.content_type}'",
        )

    contents = await upload_file.read()  # .decode('utf8')
    document = fitz.Document(stream=contents)
    if not NubankBillReader().is_valid(document):
        logger.error(f"Invalid Nubank's bill file '{upload_file.filename}'")
        raise HTTPException(
            400, "This is not a valid Nubank bill file. Please upload a valid one."
        )

    bill_model = NubankBillReader().read(document)

    end_time = time.time()
    logger.info(
        f"Processed Nubank's bill file '{upload_file.filename}' in {end_time - start_time:.2f} seconds"
    )

    if output_format == OUTPUT_FILE_TYPE.JSON:
        return bill_model
    else:
        output_file = file_types.write_bill_as(output_format, bill_model)
        response = file_to_response.file_to_response(output_file.filename, output_file.content_type, output_file.content.getvalue())
        return response


@app.post(
    "/nubank/statements",
    response_model=dto.BankStatement,
    tags=["Nubank"],
    responses={400: {"description": "Invalid content type, must be an OFX file"}},
)
async def read_nubank_statement_ofx(upload_file: UploadFile, output_format: OUTPUT_FILE_TYPE = OUTPUT_FILE_TYPE.JSON):
    """Read Nubank statement from OFX file.
    You can export yout statement from Nubank app to your email
    and then load it here.

    This is the most recommended way to load your statement.
    """
    start_time = time.time()
    logger.info(f"Reading Nubank's statement file '{upload_file.filename}'")

    if not upload_file.filename.endswith(".ofx"):
    # if upload_file.content_type != "application/octet-stream" or upload_file.content_type != "application/ofx":
        logger.error(
            f"Invalid content type for Nubank's statement file '{upload_file.filename}'"
        )
        raise HTTPException(
            400,
            f"Invalid content type. The file must be an OFX. Got '{upload_file.content_type}'",
        )

    contents = upload_file.file

    bank_statement = OFXReader().read(contents)

    if bank_statement.bank_name != "NU PAGAMENTOS S.A.":
        logger.error(f"Invalid Nubank's statement file '{upload_file.filename}'")
        raise HTTPException(
            400,
            f"This is not a valid Nubank statement file, this is a {bank_statement.bank_name} statement file. Please upload a valid one.",
        )

    bank_statement.bank_name = "Nubank"

    end_time = time.time()
    logger.info(
        f"Processed Nubank's statement file '{upload_file.filename}' in {end_time - start_time:.2f} seconds"
    )
    
    if output_format == OUTPUT_FILE_TYPE.JSON:
        return bank_statement
    else:
        output_file = file_types.write_statement_as(output_format, bank_statement)
        response = file_to_response.file_to_response(output_file.filename, output_file.content_type, output_file.content.getvalue())
        return response


@app.post(
    "/inter/bills",
    # response_model=dto.CreditCardBill,
    tags=["Inter"],
    responses={
        401: {"description": "Invalid password"},
        400: {
            "description": "Invalid content type, must be a PDF file and a valid Inter bill"
        },
    },
)
async def read_inter_credit_card_bill(
    upload_file: UploadFile,
    file_password: str,
    output_format: OUTPUT_FILE_TYPE = OUTPUT_FILE_TYPE.JSON,
):
    """Read Inter credit card bill from PDF file.
    You can find your bill files in your email."""
    start_time = time.time()
    logger.info(f"Reading Inter's bill file '{upload_file.filename}'")

    if upload_file.content_type != "application/pdf":
        logger.error(f"Invalid content type for Inter's bill file '{upload_file.filename}'")
        raise HTTPException(
            400,
            f"Invalid content type. The file must be a PDF. Got '{upload_file.content_type}'",
        )

    contents = await upload_file.read()

    document = fitz.Document(stream=contents)
    if document.authenticate(file_password) == 0:
        logger.error(f"Invalid password for Inter's bill file '{upload_file.filename}'")
        raise HTTPException(
            401,
            "Invalid password. Usually the password is the first 6 digits of your CPF.",
        )

    if not InterBillReader().is_valid(document):
        logger.error(f"Invalid Inter's bill file '{upload_file.filename}'")
        raise HTTPException(
            400, "This is not a valid Inter bill file. Please upload a valid one."
        )

    bill_model = InterBillReader().read(document)

    end_time = time.time()
    logger.info(
        f"Processed Inter's bill file '{upload_file.filename}' in {end_time - start_time:.2f} seconds"
    )

    if output_format == OUTPUT_FILE_TYPE.JSON:
        return bill_model
    else:
        output_file = file_types.write_bill_as(output_format, bill_model)
        response = file_to_response.file_to_response(output_file.filename, output_file.content_type, output_file.content.getvalue())
        return response


@app.post(
    "/inter/statements",
    response_model=dto.BankStatement,
    tags=["Inter"],
    responses={400: {"description": "Invalid content type, must be an OFX file"}},
)
async def read_inter_statement_ofx(upload_file: UploadFile, output_format: OUTPUT_FILE_TYPE = OUTPUT_FILE_TYPE.JSON):
    """Read Inter statement from OFX file.
    You can export your statement from the bank app
    or from the bank web page.

    This is the most recommend way of loading your statement.


    The statements extracted from the bank web page have more information.
    """
    start_time = time.time()
    logger.info(f"Reading Inter's statement file '{upload_file.filename}'")

    if upload_file.content_type != "application/octet-stream":
        logger.error(
            f"Invalid content type for Inter's statement file '{upload_file.filename}'"
        )
        raise HTTPException(
            400,
            f"Invalid content type. The file must be an OFX. Got '{upload_file.content_type}'",
        )

    contents = await upload_file.read()

    # Gambiarra total rsrsrs
    # CONSERTAR ISSO PELO AMOR DE DEUS
    # Create a temporary file to fix encoding problem
    with open("inter_temp.ofx", "wb") as fp:
        fp.write(contents)
    with open("inter_temp.ofx", "r", encoding="utf8") as fp:
        bank_statement = OFXReader().read(fp)
    os.unlink("inter_temp.ofx")

    if bank_statement.bank_name != "Banco Intermedium S/A":
        logger.error(f"Invalid Inter's statement file '{upload_file.filename}'")
        raise HTTPException(
            400,
            f"This is not a valid Inter statement file, this is a {bank_statement.bank_name} statement file. Please upload a valid one.",
        )

    bank_statement.bank_name = "Inter"

    end_time = time.time()
    logger.info(
        f"Processed Inter's statement file '{upload_file.filename}' in {end_time - start_time:.2f} seconds"
    )

    if output_format == OUTPUT_FILE_TYPE.JSON:
        return bank_statement
    else:
        output_file = file_types.write_statement_as(output_format, bank_statement)
        response = file_to_response.file_to_response(output_file.filename, output_file.content_type, output_file.content.getvalue())
        return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000))
    )
