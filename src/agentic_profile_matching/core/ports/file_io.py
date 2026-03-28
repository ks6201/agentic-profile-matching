


from typing import Protocol

from agentic_profile_matching.core.models.file_read_result import FileReadResult
from agentic_profile_matching.core.types.result import Result


class FileIO(Protocol):

    def read_file(self, filepath: str) -> Result[FileReadResult, str]:
        ...
    
    def write_file(self, filepath: str, content: str) -> Result[bool, str]:
        ...