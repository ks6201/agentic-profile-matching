


from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def shortlist_candidate_router(state: AgentState) -> str:

    advance_screening = state.get("advance_screening", False)

    error = state.get("error", None)

    if error is not None:
        cout = Container.resolve(ConsoleOut)
        cout.write_block(f"Error: {error}")
        return "initial"

    if advance_screening:
        return "advance_screening"
    
    return "continue"