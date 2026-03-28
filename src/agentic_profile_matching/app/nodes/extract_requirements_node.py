

from typing import Any, cast

from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.agent_state import AgentState, Requirements
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def extract_requirements_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Extracting requirements...")
    
    llm = Container.resolve(ChatOpenAI)
 
    jd = state.get("job_description", "") or state.get("messages", ["empty"])[-1]

    if "empty" in jd:
        return { "error": "No Job description found" }

    structured_llm = llm.with_structured_output(Requirements) # type: ignore

    response = cast(
        Requirements,
        structured_llm.invoke(f"Extract requirements from:\n{jd}")
    )

    return {
        "requirements": response.model_dump(),
        "error": None
    }