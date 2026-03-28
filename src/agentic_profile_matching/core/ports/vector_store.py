


from typing import Generic, Protocol, TypeVar

MODEL_TYPE = TypeVar("MODEL_TYPE")

class VectorStore(Protocol, Generic[MODEL_TYPE]):

    def read(self, embedding: MODEL_TYPE) -> list[MODEL_TYPE]:
        ...
        
    def insert(self, embeddings: list[MODEL_TYPE]) -> bool:
        ...
