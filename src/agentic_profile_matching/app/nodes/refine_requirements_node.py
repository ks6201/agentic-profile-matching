




import json
from typing import Any

from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut

def safe_parse_json(value: str) -> Any:
    
    try:
        parsed = json.loads(value)
        return parsed
    except Exception:
        return {}

def refine_requirements_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Refining requirements...")
    
    llm = Container.resolve(ChatOpenAI)
    
    requirements = state.get("requirements", {})

    messages = state.get("messages", [])
    query = messages[-1]

    if not query:
        return {"error": "Invalid request"}

    prompt = f"""
You are updating job requirements.

Current requirements:
{requirements}

User feedback:
{query}

Update the requirements accordingly.

Rules:
- Keep existing relevant requirements
- Add new ones if mentioned
- Remove if explicitly asked
- Maintain two lists:
  - must_have
  - nice_to_have

Return ONLY JSON:
{{
  "must_have": [...],
  "nice_to_have": [...]
}}
"""

    response = llm.invoke(prompt)

    updated = safe_parse_json(response.content) # type: ignore

    return {
        "requirements": updated,
        "error": None
    }