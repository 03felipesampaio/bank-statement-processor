import io

class ExportedFile:
    def __init__(self, data: io.BytesIO, name: str, content_type: str) -> None:
        self.data = data
        self.name = name
        self.content_type = content_type
