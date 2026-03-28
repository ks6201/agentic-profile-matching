



from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def error_router(state: AgentState) -> str:

    error = state.get("error", None)
    
    if error is None:
        return "continue"
    
    cout = Container.resolve(ConsoleOut)

    cout.write_block(f"Error: {error}")

    return "initial"