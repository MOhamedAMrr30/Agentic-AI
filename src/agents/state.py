"""Shared state model used by the LangGraph workflow."""

from typing import TypedDict


class ResearchState(TypedDict, total=False):
    """State container passed between graph nodes."""

    topic: str
    sub_questions: list[str]
    search_results: list[dict]
    summaries: list[str]
    report: str
