
from typing import Any

from agentic_profile_matching.app.agent_state import AgentState, CandidateScore
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def rank_candidates_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Ranking candidates...")

    candidates = state.get("filtered_candidates", []) or state.get("candidates", [])
    requirements = state.get("requirements", {})

    messages = state.get("messages", [])
    query = messages[-1]

    if not candidates:
        return {"error": f"No candidates found for this query: '{query}'"}
    
    must_have = requirements.get("must_have", []) # type: ignore
    nice_to_have = requirements.get("nice_to_have", []) # type: ignore

    rankings: list[CandidateScore] = []
    reasoning: dict[str, Any] = {}

    for candidate in candidates:
        text = (
            candidate.get("resume_text", "") + " " + " ".join(candidate.get("chunks", []))
        ).lower()

        must_matches = [s for s in must_have if s.lower() in text] # type: ignore
        nice_matches = [s for s in nice_to_have if s.lower() in text] # type: ignore
        missing = [s for s in must_have if s.lower() not in text] # type: ignore

        score = (
            0.6 * len(must_matches) + # type: ignore
            0.3 * len(nice_matches) - # type: ignore
            0.2 * len(missing) # type: ignore
        )

        rankings.append({
            "candidate_id": candidate["id"],
            "score": score,
            "name": candidate["name"],
            "skills": candidate["skills"],
            "must_have_matches": must_matches,
            "nice_to_have_matches": nice_matches,
            "missing_must_have": missing
        }) # type: ignore

        reasoning[candidate["id"]] = {
            "strengths": must_matches + nice_matches,
            "gaps": missing
        }

    rankings.sort(key=lambda x: x["score"], reverse=True) # type: ignore

    if not rankings:
        return {"error": f"No ranked candidates found for this query: '{query}'"}

    return {
        "rankings": rankings,
        "reasoning": reasoning,
        "error": None
    }