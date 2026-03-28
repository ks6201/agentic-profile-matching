

from agentic_profile_matching.adapters.file_io.binary_io.std_bin_file_io import StdBinFileIO
from agentic_profile_matching.adapters.file_io.docx_file_io.python_docx_file_io import PythonDocxFileIO
from agentic_profile_matching.adapters.file_io.pdf_file_io.pymupdf_file_io import PyMuPdfFileIO
from agentic_profile_matching.adapters.file_io.text_io.std_txt_file_io import StdTextFileIO
from agentic_profile_matching.core.models.file_metadata import FileType
from agentic_profile_matching.core.ports.file_io import FileIO


class FileIOFactory:

    @staticmethod
    def create(file_ext: FileType) -> FileIO:
        match file_ext:
            case "pdf":
                return PyMuPdfFileIO()
            case "docx":
                return PythonDocxFileIO()
            case ("txt" | "md"):
                return StdTextFileIO()
            case _:
                return StdBinFileIO()