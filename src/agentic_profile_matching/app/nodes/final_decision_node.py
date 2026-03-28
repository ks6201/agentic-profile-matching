

from typing import Any


from agentic_profile_matching.app.agent_state import AgentState
from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def final_decision_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Finalizing things...")

    candidates = state.get("shortlisted_candidates") or state.get("rankings") or state.get("candidates", [])
    deep_analysis = state.get("deep_analysis", "")
    rankings = state.get("rankings", [])
    requirements = state.get("requirements", {})
    messages = state.get("messages", [])

    if not candidates:
        return {"error": "No candidates available for final decision."}

    query = str(messages[-1]) if messages else ""

    if not query:
        return { "error": "No query found to finalize" }

    llm = Container.resolve(ChatOpenAI)

    prompt = f"""
You are a hiring decision panel.

User Query:
{query}

Job Requirements:
{requirements}

Top Candidates:
{candidates}

Ranking Data:
{rankings}

Deep Analysis:
{deep_analysis}

Tasks:
1. Decide for each candidate:
   - Hire / Strong Hire / Maybe / No Hire
2. Provide a short justification (2–3 lines)
3. Identify the best overall candidate
4. Provide final recommendation summary

Output format:

Candidate <id>:
- Decision: <Strong Hire / Hire / Maybe / No Hire>
- Justification: ...

Best Candidate:
<id>

Final Recommendation:
<short summary of hiring decision>

Be decisive, structured, and grounded in the provided data.
Do NOT invent information.
"""

    response = llm.invoke(prompt)

    return {
        "final_decision": response.content,  # type: ignore
        "error": None
    }