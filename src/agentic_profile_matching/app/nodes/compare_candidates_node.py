



from typing import Any
from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut

def compare_candidates_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Comparing candidates...")

    shortlisted = state.get("shortlisted_candidates", [])
    rankings = state.get("rankings", [])
    reasoning = state.get("reasoning", {})
    messages = state.get("messages", [])

    if not shortlisted and not rankings:
        return {"error": "No candidates available for comparison."}

    query = str(messages[-1]) if messages else ""

    candidates = shortlisted if shortlisted else rankings

    llm = Container.resolve(ChatOpenAI)

    prompt = f"""
You are a hiring expert comparing candidates.

User Query (Strictly follow this):
{query}

Candidates:
{candidates}

Candidate Evaluation Data:
{reasoning}

Tasks:
1. Compare candidates based on:
   - skills match
   - strengths
   - gaps
   - overall fit
2. Highlight key differences clearly
3. Identify which candidate is stronger and why
4. If the user asked about specific candidates, focus on them
5. Be concise but analytical

Output format:

Comparison:
- Candidate A vs Candidate B: <key differences>

Summary:
- Stronger candidate: <id>
- Reason: <short explanation>
"""

    response = llm.invoke(prompt)

    return {
        "output": response.content,  # type: ignore
        "error": None
    }