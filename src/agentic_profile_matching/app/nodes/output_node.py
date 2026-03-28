




from typing import Any

from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def output_node(state: AgentState) -> dict[str, Any]:
    output = state.get("output", "")

    cout = Container.resolve(ConsoleOut)

    cout.write_block(output)

    return {
        "output": None
    }