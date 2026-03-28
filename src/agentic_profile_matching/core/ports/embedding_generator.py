


from typing import Generic, Protocol, TypeVar

GEN_VEC_TYPE = TypeVar("GEN_VEC_TYPE", covariant=True)

class EmbeddingGenerator(Protocol, Generic[GEN_VEC_TYPE]):

    def generate(self, input: str) -> GEN_VEC_TYPE:
        ...