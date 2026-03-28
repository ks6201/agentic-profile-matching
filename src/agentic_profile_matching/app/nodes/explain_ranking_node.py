

from typing import Any

from agentic_profile_matching.app.agent_state import AgentState


from typing import Any
from agentic_profile_matching.app.agent_state import AgentState
from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def explain_ranking_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Explaining rankings...")
    
    rankings = state.get("rankings", [])
    reasoning = state.get("reasoning", {})
    messages = state.get("messages", [])

    query = str(messages[-1]) if messages else ""

    if not rankings:
        return {"error": f"No ranked candidates found for this query: '{query}'"}



    llm = Container.resolve(ChatOpenAI)

    prompt = f"""
You are a hiring assistant.

User Query (Strictly follow this):
{query}

Candidate Rankings:
{rankings}

Candidate Reasoning:
{reasoning}

Tasks:
1. Answer the user's question about the ranking
2. If comparing candidates, explain clearly why one ranks higher
3. If general explanation, explain top candidates and reasoning
4. Highlight strengths and gaps
5. Be concise but clear

Do NOT invent data. Use only provided information.
"""

    response = llm.invoke(prompt)

    return {
        "output": response.content,  # type: ignore
        "error": None
    }