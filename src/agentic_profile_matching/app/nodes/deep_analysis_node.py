



from typing import Any

from agentic_profile_matching.app.agent_state import AgentState


from typing import Any
from agentic_profile_matching.app.agent_state import AgentState
from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def deep_analysis_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Deep analysis in progress...")
    
    candidates = state.get("shortlisted_candidates") or state.get("rankings") or state.get("candidates", [])
    requirements = state.get("requirements", {})
    reasoning = state.get("reasoning", {})
    messages = state.get("messages", [])

    if not candidates:
        return {"error": "No shortlisted candidates available."}

    query = str(messages[-1]) if messages else ""

    llm = Container.resolve(ChatOpenAI)

    prompt = f"""
You are a senior hiring panel performing a deep candidate evaluation.

User Query (Strictly follow this):
{query}

Job Requirements:
{requirements}

Candidates:
{candidates}

Previous Evaluation:
{reasoning}

Tasks:
Perform deep analysis for each candidate considering:
1. Skill depth (not just presence)
2. Real-world experience relevance
3. Problem-solving ability (infer from profile)
4. Potential risks or concerns
5. Overall role fit

Output format:

Candidate <[name | id]>:
- Strengths (detailed)
- Weaknesses / Risks
- Role Fit (High / Medium / Low)
- Justification (2-3 lines)

Be analytical and critical. Do NOT repeat shallow keyword matching.
Use only provided data.
"""

    response = llm.invoke(prompt)

    return {
        "shortlisted_candidates": candidates,
        "deep_analysis": response.content,  # type: ignore
        "error": None
    }