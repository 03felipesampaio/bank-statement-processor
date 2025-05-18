from fastapi.responses import JSONResponse, Response
import file_types


def build_response(file_format, data, filename):
    responses_template = {
        "json": {"media_type": "application/json"},
        "csv": {"media_type": "text/csv"},
        "excel": {
            "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        },
        "parquet": {"media_type": "application/octet-stream"},
    }

    response = responses_template.get(file_format, None)

    if not response:
        raise ValueError(
            f"Failed to convert {filename} to file format {file_format}. The file format is not supported."
        )

    return Response(
        data, headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


def build_csv_response(data, filename):
    return Response(
        content=data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


def build_excel_response(data, filename):
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
