

from openai import embeddings
from agentic_profile_matching.app.pipeline.steps.embedding_generation_step import EBD_VECTOR
from agentic_profile_matching.core.ports.embedding_generator import EmbeddingGenerator


class OpenAIEmbeddingGenerator(EmbeddingGenerator[list[float]]):

    def generate(self, input: str) -> EBD_VECTOR:
        response = embeddings.create(
            model="text-embedding-3-small",
            input=input
        )

        return response.data[0].embedding