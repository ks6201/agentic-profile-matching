from enum import StrEnum
from typing import TypedDict
from pydantic import BaseModel


# --- Pydantic models (used with with_structured_output) ---

class Intent(StrEnum):
    SEARCH  = "search"
    COMPARE = "compare"
    EXPLAIN = "explain"
    REFINE  = "refine"
    DEEP_ANALYSIS = "deep_analysis"
    GEQ = "generate_interview_questions"

class ParsedInput(TypedDict):
    intent: Intent
    skills: list[str]
    experience: int

class Requirements(BaseModel):
    must_have: list[str]
    nice_to_have: list[str]

class CandidateScore(BaseModel):
    candidate_id: str
    score: float
    must_have_matches: list[str]
    nice_to_have_matches: list[str]
    missing_must_have: list[str]

class CandidateReasoning(BaseModel):
    strengths: list[str]
    gaps: list[str]
    explanation: str

class Candidate(TypedDict):
    id: str
    name: str
    skills: list[str]
    education: str
    resume_text: str

class AgentState(TypedDict, total=False):
    messages: list[str]

    parsed_input: ParsedInput

    job_description: str
    requirements: Requirements

    candidates: list[Candidate]
    filtered_candidates: list[Candidate]
    shortlisted_candidates: list[Candidate]

    rankings: list[CandidateScore]

    reasoning: dict[str, CandidateReasoning]  # keyed by candidate_id

    feedback: str

    advance_screening: bool

    error: str | None
    output: str | None