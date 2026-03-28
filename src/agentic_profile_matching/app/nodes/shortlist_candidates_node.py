



from typing import Any

from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


# top 10
def shortlist_candidates_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Shortlisting candidates...")

    rankings = state.get("rankings", [])
    candidates = state.get("filtered_candidates", [])

    messages = state.get("messages", [])
    query = messages[-1]

    if not rankings:
        return {"error": f"No ranked candidates found for this query: '{query}'"}

    # map candidates by id
    candidate_map = {candidate["id"]: candidate for candidate in candidates}

    sorted_rankings = sorted(
        rankings,
        key=lambda x: x.get("score", 0), # type: ignore
        reverse=True
    )

    shortlisted = []

    for rank in sorted_rankings[:10]:
        cid = rank["candidate_id"] # type: ignore
        candidate = candidate_map.get(cid) # type: ignore

        if candidate:
            shortlisted.append({ # type: ignore
                **candidate,
                **rank # type: ignore
            })

    return {
        "shortlisted_candidates": shortlisted,
        "error": None
    }