
from langgraph.graph import StateGraph

from agentic_profile_matching.app.agent_state import AgentState
from agentic_profile_matching.app.nodes.compare_candidates_node import compare_candidates_node
from agentic_profile_matching.app.nodes.deep_analysis_node import deep_analysis_node
from agentic_profile_matching.app.nodes.explain_ranking_node import explain_ranking_node
from agentic_profile_matching.app.nodes.extract_requirements_node import extract_requirements_node
from agentic_profile_matching.app.nodes.final_decision_node import final_decision_node
from agentic_profile_matching.app.nodes.generate_interview_questions_node import generate_interview_questions_node
from agentic_profile_matching.app.nodes.generate_report_node import generate_report_node
from agentic_profile_matching.app.nodes.output_node import output_node
from agentic_profile_matching.app.nodes.rank_candidates_node import rank_candidates_node
from agentic_profile_matching.app.nodes.refine_requirements_node import refine_requirements_node
from agentic_profile_matching.app.nodes.search_candidates_node import search_candidates_node
from agentic_profile_matching.app.nodes.take_user_input_node import take_user_input_node
from agentic_profile_matching.app.routers.error_router import error_router
from agentic_profile_matching.app.routers.intent_router import intent_router
from agentic_profile_matching.app.nodes.parse_input_node import parse_input_node
from agentic_profile_matching.app.nodes.shortlist_candidates_node import shortlist_candidates_node

class AgenticProfileMatcher:
    

    def __init__(self, state: AgentState) -> None:
        self.state = state
        self.graph = StateGraph(AgentState)

    def init_graph(self):
        self.graph.add_node("take_user_input_node", take_user_input_node) # type: ignore
        self.graph.add_node("parse_input_node", parse_input_node) # type: ignore

        self.graph.add_node("extract_requirements_node", extract_requirements_node) # type: ignore
        self.graph.add_node("search_candidates_node", search_candidates_node) # type: ignore
        self.graph.add_node("rank_candidates_node", rank_candidates_node) # type: ignore
        self.graph.add_node("shortlist_candidates_node", shortlist_candidates_node) # type: ignore
        self.graph.add_node("generate_report_node", generate_report_node) # type: ignore
        self.graph.add_node("output_node", output_node) # type: ignore

        self.graph.add_node("refine_requirements_node", refine_requirements_node) # type: ignore

        self.graph.add_node("explain_ranking_node", explain_ranking_node) # type: ignore

        self.graph.add_node("generate_interview_questions_node", generate_interview_questions_node) # type: ignore

        self.graph.add_node("deep_analysis_node", deep_analysis_node) # type: ignore
        self.graph.add_node("final_decision_node", final_decision_node) # type: ignore
        
        self.graph.add_node("compare_candidates_node", compare_candidates_node) # type: ignore


        # ----
        # Edges
        # ----
        self.graph.add_edge("take_user_input_node", "parse_input_node")

        # ---
        # Normal Flow
        # ---        
        self.graph.add_conditional_edges(
            "parse_input_node",
            intent_router,
            {
                "extract_requirements": "extract_requirements_node",
                "compare_candidates": "compare_candidates_node",
                "explain_ranking": "explain_ranking_node",
                "refine_requirements": "refine_requirements_node",
                "deep_analysis": "deep_analysis_node",
                "generate_interview_questions": "generate_interview_questions_node",
                "continue": "take_user_input_node"
            }
        )

        self.safe_edge(
            "extract_requirements_node",
            "search_candidates_node"
        )

        self.safe_edge(
            "search_candidates_node",
            "rank_candidates_node"
        )
        self.safe_edge(
            "rank_candidates_node",
            "shortlist_candidates_node"
        )
        
        self.safe_edge(
            "shortlist_candidates_node",
            "generate_report_node"
        )
        
        self.safe_edge(
            "generate_report_node",
            "output_node"
        )

        self.safe_edge(
            "output_node",
            "take_user_input_node"
        )


        # ---
        # Refinement Flow
        # ---
        self.safe_edge(
            "refine_requirements_node",
            "search_candidates_node"
        )

        # ---
        # Compare Flow
        # ---
        self.safe_edge(
            "compare_candidates_node",
            "output_node"
        )
        
        
        # ---
        # Explain ranking Flow
        # ---
        self.safe_edge(
            "explain_ranking_node",
            "output_node"
        )


        # ---
        # Generate interview questions
        # ---
        self.safe_edge(
            "generate_interview_questions_node",
            "output_node"
        )

        # ---
        # Advance Screening
        # ---
        self.safe_edge(
            "deep_analysis_node",
            "final_decision_node"
        )

        self.safe_edge(
            "final_decision_node",
            "generate_report_node"
        )

    def safe_edge(self, from_node: str, to_node: str):
        self.graph.add_conditional_edges(
            from_node,
            error_router,
            {
                "initial": "take_user_input_node",
                "continue": to_node
            }
        )

    def start(self):
        self.graph.set_entry_point("take_user_input_node")
        
        app = self.graph.compile() # type: ignore
        return app.invoke(self.state) # type: ignore
