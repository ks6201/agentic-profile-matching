


from agentic_profile_matching.app.agent_state import AgentState, Intent


def intent_router(state: AgentState) -> str:
    parsed = state.get("parsed_input")
    if not parsed:
        raise ValueError("parsed_input missing from state")

    intent = parsed.get("intent", "")

    match intent:
        case Intent.SEARCH:
            return "extract_requirements"
        case Intent.EXPLAIN:
            return "explain_ranking"
        case Intent.COMPARE:
            return "compare_candidates"
        case Intent.REFINE:
            return "refine_requirements"
        case Intent.DEEP_ANALYSIS:
            return "deep_analysis"
        case Intent.GEQ:
            return "generate_interview_questions"
        case _:
            return "continue"