from fastapi.responses import Response


def file_to_response(filename: str, content_type: str, content: bytes) -> Response:
    return Response(
        content,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
        media_type=content_type,
    )
