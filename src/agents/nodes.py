"""Phase 2 node stubs to be implemented incrementally."""

from .state import ResearchState


def planner_node(state: ResearchState) -> ResearchState:
    """Decompose a topic into sub-questions (stub)."""
    topic = state.get("topic", "")
    return {**state, "sub_questions": [f"What are the key aspects of {topic}?"] if topic else []}


def search_node(state: ResearchState) -> ResearchState:
    """Run search for a sub-question (stub)."""
    results = [{"question": q, "snippets": []} for q in state.get("sub_questions", [])]
    return {**state, "search_results": results}


def summarizer_node(state: ResearchState) -> ResearchState:
    """Summarize collected snippets (stub)."""
    summaries = [f"Summary placeholder for: {r['question']}" for r in state.get("search_results", [])]
    report = "\n".join(summaries)
    return {**state, "summaries": summaries, "report": report}
