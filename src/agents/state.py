"""Shared state model used by the LangGraph workflow."""

from typing import Any, TypedDict


class SearchResult(TypedDict, total=False):
    question: str
    snippets: list[str]
    sources: list[dict[str, Any]]


class ResearchState(TypedDict, total=False):
    """State container passed between graph nodes."""

    topic: str
    sub_questions: list[str]
    search_results: list[SearchResult]
    summaries: list[str]
    report: str
