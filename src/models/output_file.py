import io

class OutputFile:
    def __init__(self, filename: str, content_type: str, content: io.BytesIO):
        self.filename = filename
        self.content_type = content_type
        self.content = content
