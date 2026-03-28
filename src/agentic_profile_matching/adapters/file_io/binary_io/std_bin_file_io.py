

from datetime import datetime
from logging import Logger
import os

from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.models.file_metadata import FileMetadata, FileType
from agentic_profile_matching.core.models.file_read_result import FileReadResult
from agentic_profile_matching.core.ports.file_io import FileIO
from agentic_profile_matching.core.types.result import Result



class StdBinFileIO(FileIO):

    def __init__(self) -> None:
        super().__init__()
        self.logger = Container.resolve(Logger)

    def read_file(self, filepath: str) -> Result[FileReadResult, str]:
        try:
            stats = os.stat(filepath)

            file_metadata = FileMetadata(
                name=os.path.basename(filepath),
                size=stats.st_size,
                ftype=FileType.BIN,
                modified_date=datetime.fromtimestamp(stats.st_mtime),
            )
            
            with open(filepath, "rb") as reader:
                result = FileReadResult(
                    metadata=file_metadata,
                    content=reader.read(),
                    is_binary=True
                )

                return Result.ok(result)
        except Exception:
            return Result.err("Failed to read binary file.")

    def write_file(self, filepath: str, content: str | bytes) -> Result[bool, str]:
        try:
            with open(filepath, "wb") as writer:
                if isinstance(content, str):
                    writer.write(content.encode("utf-8"))
                else:
                    writer.write(content)

                return Result.ok(True)
            
        except FileNotFoundError as e:
            self.logger.error(e)
            return Result.err("File not found")
        except Exception as e:
            self.logger.error(e)
            return Result.err("Something went wrong")