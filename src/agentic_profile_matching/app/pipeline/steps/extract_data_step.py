
from pathlib import Path

from agentic_profile_matching.adapters.file_io.file_ext import is_file_ext_supported
from agentic_profile_matching.adapters.file_io.file_io_factory import FileIOFactory
from agentic_profile_matching.app.pipeline.step import Step

FILE_NAME_OR_PATH = str

class ExtractDataStep(Step[FILE_NAME_OR_PATH, str]):

    def get_file_extension(self, filepath: str) -> str:
        return Path(filepath).suffix.lstrip(".").lower()


    def execute(self, input: FILE_NAME_OR_PATH) -> str:
        ext = self.get_file_extension(input)
        
        if not is_file_ext_supported(ext):
            return ""
        
        file_io = FileIOFactory.create(ext)
        result = file_io.read_file(input)
        
        if result.is_err():
            return ""

        value = result.unwrap()
    
        content = value.content
    
        if not isinstance(content, str):
            return ""

        return content