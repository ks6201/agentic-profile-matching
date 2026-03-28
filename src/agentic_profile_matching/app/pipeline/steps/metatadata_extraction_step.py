

from dataclasses import dataclass
import json
import re
from typing import Any

from langchain_openai import ChatOpenAI

from agentic_profile_matching.app.pipeline.step import Step
from agentic_profile_matching.app.utils.education_generator import generate_education
from agentic_profile_matching.app.utils.name_generator import generate_name

@dataclass
class DocumentWithMetadata:
    text: str
    metadata: dict[str, Any]

class MetadataExtractionStep(Step[str, DocumentWithMetadata]):
    SYSTEM_PROMPT = """
You are a structured information extraction system.

Extract candidate metadata from the provided resume text.

Return JSON only using this schema:

{
  "name": string | null,
  "skills": string[] | null,
  "experience_years": number | null,
  "education": string[] | null
}

Extraction rules:

1. name
- Extract the candidate's full human name if it appears in the resume.
- The name usually appears at the beginning or in contact information.

- Validate that the extracted name is a real human name:
  • Must consist of alphabetic words (no IDs, emails, company names, or usernames).
  • Typically 2–4 words (e.g., "John Doe", "Amit Kumar Singh").
  • Should not contain numbers or special characters (except periods in initials).
  • Should not match organization names, job titles, domains, or technologies.
  • Avoid all-uppercase strings unless clearly formatted as a name.
  • Reject phrases like: "Curriculum Vitae", "Resume", "Software Engineer", "Google LLC", etc.

- If the extracted value does NOT clearly represent a human personal name, return null.

2. skills
- List technical or professional skills explicitly mentioned.
- Do not invent skills.
- If no skills are identifiable, return null.

3. experience_years
- Total years of professional experience if stated explicitly
  (e.g., "5 years experience", "over 10 years").
- If only job dates exist, estimate roughly from them.
- If impossible to determine, return null.

4. education
- List degrees, certifications, or educational qualifications.
- Example: "BSc Computer Science", "MBA", "Cisco CCNA".
- If not present, return null.

Strict output requirements:
- Return JSON only.
- Do not include explanations.
- Do not include markdown.
- Do not include extra fields.
"""

    def __init__(self, llm: ChatOpenAI) -> None:
        super().__init__()
        self.llm = llm

    def _safe_json_parse(self, text: Any) -> dict[str, Any]:
        try:
            return json.loads(text)

        except Exception:
            match = re.search(r"\{.*\}", text, re.DOTALL)

            if match:
                try:
                    return json.loads(match.group())
                except Exception:
                    pass

        return {}

    def _validate_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:

        name = metadata.get("name")
        skills = metadata.get("skills")
        experience_years = metadata.get("experience_years")
        education = metadata.get("education")

        """
        Note:
            - The resume dataset used in this project omits candidate names in some cases due to PII restrictions.
            - For demonstration purposes, random name generators are used to populate these fields.
            - In a production setting, such records would typically be rejected or processed using alternative
              identifying attributes (e.g., phone number or other unique identifiers).
        """
        return {
            "name": name or generate_name(),
            "skills": skills,
            "education": education or generate_education(),
            "experience_years": experience_years
        }

    def _extract_metadata(self, text: str) -> dict[str, Any]:

                prompt = f"""
        {self.SYSTEM_PROMPT}

        Resume Text:
        {text}
        """
                response = self.llm.invoke(prompt)

                metadata = self._safe_json_parse(response.content) # type: ignore
                
                return self._validate_metadata(metadata)

    def execute(self, input: str) -> DocumentWithMetadata:
        metadata = self._extract_metadata(input)

        metadata["resume_text"] = input

        return DocumentWithMetadata(input, metadata)