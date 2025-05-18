import io
from src.models.exported_file import ExportedFile


class ReportExporter:
    suported_file_types = None

    def __init__(self):
        if self.suported_file_types is None:
            raise NotImplementedError('Please define the supported file types')

    def export_to(self, file_type: str, report) -> ExportedFile:
        raise NotImplementedError