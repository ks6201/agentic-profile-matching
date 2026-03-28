



from dataclasses import dataclass
from typing import Any

from agentic_profile_matching.app.pipeline.step import Step
from agentic_profile_matching.app.pipeline.steps.metatadata_extraction_step import DocumentWithMetadata

@dataclass
class ProcessedDocument:
    chunks: list[str]
    metadata: dict[str, Any]


class ChunkingStep(Step[DocumentWithMetadata, ProcessedDocument]):

    def __init__(self, chunk_size: int = 300, overlap: int = 50) -> None:
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        
        self.OVERLAP = overlap
        self.CHUNK_SIZE = chunk_size

    def execute(self, input: DocumentWithMetadata) -> ProcessedDocument:
        words = input.text.split()

        chunks: list[str] = []
        step = self.CHUNK_SIZE - self.OVERLAP

        for i in range(0, len(words), step):
            chunk_words = words[i:i + self.CHUNK_SIZE]

            if not chunk_words:
                break

            chunks.append(" ".join(chunk_words))

        return ProcessedDocument(chunks, input.metadata)