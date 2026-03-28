

from typing import Any, Dict, cast

from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.agent_state import AgentState, ParsedInput
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut

def parse_input_node(state: AgentState) -> Dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Parsing user input...")

    llm = Container.resolve(ChatOpenAI)
    
    messages = state.get("messages", "")

    query = messages[-1] if messages else ""

    if not query:
        return { "error": "No query found to be parsed." }

    structured_llm = llm.with_structured_output(ParsedInput) # type: ignore

    prompt = f"""
    Extract structured intent from this query:

    Query: {query}
    """
    
    response = cast(
        ParsedInput,
        structured_llm.invoke(prompt)
    )

    return {
        "parsed_input": response,
        "error": None
    }