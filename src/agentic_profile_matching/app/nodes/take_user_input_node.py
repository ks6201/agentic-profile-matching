



from logging import Logger
import sys
from typing import Any

from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.configs.constants import Constants
from agentic_profile_matching.core.ports.console_in import ConsoleIn


def take_user_input_node(state: AgentState) -> dict[str, Any]:
    cin  = Container.resolve(ConsoleIn)
    logger = Container.resolve(Logger)

    messages = state.get("messages", [])

    user_query = ""
    try:
        while len(user_query.strip()) < 1:
            user_query = cin.read_line("[APM]> ")

            messages.append(user_query)

            if not user_query.strip() or user_query.lower() in (Constants.QUIT, Constants.EXIT):
                break
            
            return {
                "messages": messages,
                "error": None
            }

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    
    sys.exit(0)
