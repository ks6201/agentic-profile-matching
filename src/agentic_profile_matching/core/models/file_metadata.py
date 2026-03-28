

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

class FileType(StrEnum):
    PDF = "pdf"
    BIN = "bin"
    DOCX = "docx"
    TEXT = "text"

@dataclass
class FileMetadata:
    name: str
    size: int
    ftype: FileType
    modified_date: str

    def __init__(self, name: str, size: int, ftype: FileType, modified_date: datetime):
        self.name = name
        self.size = size
        self.ftype = ftype
        self.modified_date = modified_date.isoformat()