

from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.agentic_profile_matcher import AgenticProfileMatcher
from agentic_profile_matching.configs import register_singletons
from agentic_profile_matching.configs.logging.logging_config import APMLogger


def main():
    for fn in (APMLogger.init, register_singletons):
        fn()
        
    state = AgentState()
    apm = AgenticProfileMatcher(state)

    apm.init_graph()
    apm.start()