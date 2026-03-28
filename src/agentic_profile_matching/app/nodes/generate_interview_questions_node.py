




from typing import Any

from agentic_profile_matching.app.agent_state import AgentState


from typing import Any
from agentic_profile_matching.app.agent_state import AgentState
from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def generate_interview_questions_node(state: AgentState) -> dict[str, Any]:
    cout = Container.resolve(ConsoleOut)
    cout.write_block("Generating interview questions...")
    
    shortlisted = state.get("shortlisted_candidates") or state.get("rankings") or state.get("candidates", [])
    requirements = state.get("requirements", {})
    messages = state.get("messages", [])

    if not shortlisted:
        return {"error": "No shortlisted candidates available."}

    query = str(messages[-1]) if messages else ""

    candidates = shortlisted[:3]

    llm = Container.resolve(ChatOpenAI)

    prompt = f"""
You are a technical interviewer.

User Query (Strictly follow this query answer accordingly):
{query}

Job Requirements:
{requirements}

Candidates:
{candidates}

Task:
Generate tailored interview questions for each candidate.

Instructions:
1. Create 5 questions per candidate
2. Focus on:
   - must-have skills validation
   - real-world problem solving
   - gaps or missing skills
3. Questions should be specific to each candidate’s profile
4. Include a mix of:
   - technical questions
   - scenario-based questions
5. Clearly separate questions per candidate

Output format:

Candidate <name | id>:
- Question 1
- Question 2
...
"""

    response = llm.invoke(prompt)

    return {
        "output": response.content,  # type: ignore
        "error": None
    }