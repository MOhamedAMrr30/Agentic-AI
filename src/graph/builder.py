from __future__ import annotations

from operator import add
from typing import Annotated, Any, Dict, List, TypedDict

from dotenv import load_dotenv
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph

from src.agents.critic import critic_node
from src.agents.planner import planner_node
from src.agents.search import search_node
from src.agents.synthesizer import synthesizer_node


class ResearchState(TypedDict):
    topic: str
    sub_questions: List[str]
    search_results: Annotated[List[dict[str, Any]], add]
    summaries: List[str]
    critic_scores: List[dict[str, Any]]
    filtered_results: List[dict[str, Any]]
    final_report: str


def route_sub_questions(state: ResearchState):
    sub_questions = state.get("sub_questions", [])
    if not sub_questions:
        return [Send("search_node", {"current_sub_question": state.get("topic", "")})]
    return [Send("search_node", {"current_sub_question": sq}) for sq in sub_questions]


def build_graph():
    load_dotenv()
    graph = StateGraph(ResearchState)

    graph.add_node("planner_node", planner_node)
    graph.add_node("search_node", search_node)
    graph.add_node("critic_node", critic_node)
    graph.add_node("synthesizer_node", synthesizer_node)

    graph.add_edge(START, "planner_node")
    graph.add_conditional_edges("planner_node", route_sub_questions, ["search_node"])
    graph.add_edge("search_node", "critic_node")
    graph.add_edge("critic_node", "synthesizer_node")
    graph.add_edge("synthesizer_node", END)

    return graph.compile()
