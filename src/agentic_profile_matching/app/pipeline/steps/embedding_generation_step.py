

from agentic_profile_matching.adapters.db.models.embedding_1536 import Embedding1536Model
from agentic_profile_matching.app.pipeline.steps.chunking_step import ProcessedDocument
from agentic_profile_matching.core.ports.embedding_generator import EmbeddingGenerator
from agentic_profile_matching.app.pipeline.step import Step

EBD_VECTOR = list[float]

class EmbeddingGenStep(Step[ProcessedDocument, list[Embedding1536Model]]):

    def __init__(self, generator: EmbeddingGenerator[EBD_VECTOR]) -> None:
        self.ebd_generator = generator



    def execute(self, input: ProcessedDocument) -> list[Embedding1536Model]:

        embeddings: list[Embedding1536Model] = []

        for txt in input.chunks:

            vector = self.ebd_generator.generate(txt)

            ebd = Embedding1536Model(
                content=txt,
                embedding=vector,
                metadata_=input.metadata
            )

            embeddings.append(ebd)

        return embeddings