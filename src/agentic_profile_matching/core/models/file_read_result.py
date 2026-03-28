


from dataclasses import dataclass

from agentic_profile_matching.core.models.file_metadata import FileMetadata



@dataclass
class FileReadResult:
    is_binary: bool
    content: str | bytes
    metadata: FileMetadata