


from agentic_profile_matching.adapters.db.models.embedding_1536 import Embedding1536Model
from agentic_profile_matching.app.pipeline.step import Step


class ContextAssemblyStep(Step[list[Embedding1536Model], str]):

    def execute(self, input: list[Embedding1536Model]) -> str:
        chunks: list[str] = []

        for index, chunk in enumerate(input):
            chunks.append(
                f"""
Candidate {index+1}:
{chunk.content}
Candidate {index+1} Metadata:
{chunk.metadata_}
"""
            )

        return "\n".join(chunks)