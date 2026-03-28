


from typing import Any

from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut



def filter_candidates_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Filtering candidates...")

    candidates = state.get("candidates", [])
    requirements = state.get("requirements", {})
    messages = state.get("messages", [])

    query = str(messages[-1]) if messages else ""

    if not candidates:
        return {"error": f"No candidates found for this query: '{query}'"}

    candidates_subset = candidates[:15]

    llm = Container.resolve(ChatOpenAI)

    prompt = f"""
You are a hiring assistant.

Job Requirements:
{requirements}

User Query:
{query}

Candidates:
{candidates_subset}

Task:
Filter candidates based on the job requirements.

Rules:
1. Candidates MUST satisfy most or all must-have requirements
2. Be slightly flexible (do not reject for minor gaps)
3. Use resume_text and chunks for evaluation
4. Do NOT invent candidates
5. Return ONLY candidates from the given list

Return ONLY valid JSON (list of candidates), no explanation.
"""

    try:
        response = llm.invoke(prompt)

        import json
        filtered = json.loads(response.content) # type: ignore

        return {
            "filtered_candidates": filtered,
            "error": None
        }

    except Exception as e:
        return {
            "filtered_candidates": [],
            "error": f"Filtering failed: {str(e)}"
        }