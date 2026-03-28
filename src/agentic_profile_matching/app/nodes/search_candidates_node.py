



from typing import Any

from agentic_profile_matching.adapters.db.models.embedding_1536 import Embedding1536Model
from agentic_profile_matching.adapters.embedding_generator.openai_embedding_generator import OpenAIEmbeddingGenerator
from agentic_profile_matching.adapters.vector_store.pg_vector_store import PGVectorStore
from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.pipeline.pipeline import Pipeline
from agentic_profile_matching.app.pipeline.steps.chunking_step import ProcessedDocument
from agentic_profile_matching.app.pipeline.steps.embedding_generation_step import EmbeddingGenStep
from agentic_profile_matching.app.pipeline.steps.vector_similarity_search_step import VectorSimilaritySearchStep
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut

def build_retrieval_pipeline() -> Pipeline[ProcessedDocument, list[Embedding1536Model]]:
    retrieval_pipeline = (
    Pipeline
        .start(EmbeddingGenStep(OpenAIEmbeddingGenerator()))
        .pipe(VectorSimilaritySearchStep(PGVectorStore()))
    )

    return retrieval_pipeline


def search_candidates_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Searching candidates...")

    pipeline = build_retrieval_pipeline()

    messages = state.get("messages", [])
    query = messages[-1]

    if not messages:
        return {"error": f"No messages found."}


    pdoc = ProcessedDocument([query], {})
    results = pipeline.run(pdoc)

    if not results:
        return {"error": f"No candidates found for this query: '{query}'"}

    candidate_map: dict[str, Any] = {}

    for item in results:
        candidate_id = str(item.id)

        if candidate_id not in candidate_map:
            candidate_map[candidate_id] = {
                "id": candidate_id,
                "name": item.metadata_.get("name", "No Name"),
                "skills": item.metadata_.get("skills", []),
                "resume_text": item.metadata_.get("resume_text", ""),
                "metadata": item.metadata_,
                "chunks": []
            }

        candidate_map[candidate_id]["chunks"].append(item.content)

    candidates = list(candidate_map.values())

    return {
        "candidates": candidates,
        "error": None
    }