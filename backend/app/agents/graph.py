from langgraph.graph import StateGraph, START, END
from app.schemas import DhaleeState
from app.agents.auditor import skill_auditor_node
from app.agents.scout import market_scout_node
from app.agents.curator import content_curator_node
from app.agents.architect import roadmap_architect_node
from app.agents.coach import performance_coach_node
from app.agents.advocate import talent_advocate_node


def build_graph():
    builder = StateGraph(DhaleeState)

    builder.add_node("skill_auditor", skill_auditor_node)
    builder.add_node("market_scout", market_scout_node)
    builder.add_node("content_curator", content_curator_node)
    builder.add_node("roadmap_architect", roadmap_architect_node)
    builder.add_node("performance_coach", performance_coach_node)
    builder.add_node("talent_advocate", talent_advocate_node)

    builder.add_edge(START, "skill_auditor")
    builder.add_edge("skill_auditor", "market_scout")
    builder.add_edge("market_scout", "content_curator")
    builder.add_edge("content_curator", "roadmap_architect")
    builder.add_edge("roadmap_architect", "performance_coach")
    builder.add_edge("performance_coach", "talent_advocate")
    builder.add_edge("talent_advocate", END)

    return builder.compile()
