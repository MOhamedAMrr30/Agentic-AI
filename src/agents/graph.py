"""LangGraph wiring for Phase 2 (Planner -> Search -> Summarizer)."""

from langgraph.graph import END, StateGraph

from .nodes import planner_node, search_node, summarizer_node
from .state import ResearchState


def build_graph():
    graph = StateGraph(ResearchState)
    graph.add_node("planner", planner_node)
    graph.add_node("search", search_node)
    graph.add_node("summarizer", summarizer_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "search")
    graph.add_edge("search", "summarizer")
    graph.add_edge("summarizer", END)
    return graph.compile()
