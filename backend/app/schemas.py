from typing import TypedDict, Optional


class DhaleeState(TypedDict):
    cv_text: str
    desired_role: str
    extracted_skills: list[str]
    skill_gaps: list[str]
    market_requirements: list[str]
    curated_resources: list[dict]
    learning_roadmap: dict
    coach_feedback: str
    readiness_report: dict
    error: Optional[str]
