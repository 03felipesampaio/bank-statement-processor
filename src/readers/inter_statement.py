from pathlib import Path


class InterStatementFileOpener:
    def __init__(self) -> None:
        pass
    
    def open(self):
        ...

class InterStatementReader:
    def __init__(self, file_opener: InterStatementFileOpener) -> None:
        pass
    
    def read(self, file_path: Path|str) -> dict:
        ...