
from typing import Any

from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def generate_report_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Generating Report...")
    
    llm = Container.resolve(ChatOpenAI)
    candidates = (
        state.get("shortlisted_candidates")
        or state.get("rankings")
        or []
    )

    messages = state.get("messages", [])
    query = messages[-1]

    if not candidates:
        return {"error": f"No candidates found for this query: '{query}'"}

    query = state.get("messages", [""])[-1]

    summarized_candidates: list[Any] = [ # type: ignore
        {
            "id": candidate.get("candidate_id") or candidate.get("id"), # type: ignore
            "name": candidate.get("name"), # type: ignore
            "score": candidate.get("score"), # type: ignore
            "skills": candidate.get("skills", []), # type: ignore
        }
        for candidate in candidates[:5]
    ]

    prompt = f"""
You are a hiring assistant.

User Query:
{query}

Candidates:
{summarized_candidates}

Generate a structured hiring report with:

1. Summary of top candidates
2. Strengths of each candidate
3. Gaps or missing skills
4. Final recommendation (who to shortlist and why)

Be concise and structured.
"""

    response = llm.invoke(prompt) # type: ignore

    return {
        "output": response.content, # type: ignore
        "error": None
    }