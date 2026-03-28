
from typing import Any, TypeGuard


from typing import Any, TypeGuard

from agentic_profile_matching.core.models.file_metadata import FileType

def is_file_ext_supported(value: Any) -> TypeGuard[FileType]:
    if not isinstance(value, str):
        return False
    try:
        FileType(value)
        return True
    except ValueError:
        return False