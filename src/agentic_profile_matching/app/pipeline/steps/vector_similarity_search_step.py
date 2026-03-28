


from agentic_profile_matching.adapters.db.models.embedding_1536 import Embedding1536Model
from agentic_profile_matching.app.pipeline.step import Step
from agentic_profile_matching.core.ports.vector_store import VectorStore


class VectorSimilaritySearchStep(Step[list[Embedding1536Model], list[Embedding1536Model]]):

    def __init__(self, store: VectorStore[Embedding1536Model]):
        self.store = store

    
    def execute(self, input: list[Embedding1536Model]) -> list[Embedding1536Model]:
        result = self.store.read(input[0])

        return result