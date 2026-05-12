from __future__ import annotations

from typing import Any, Dict, List

from tavily import TavilyClient


def search_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Search a single sub-question.

    Expects `current_sub_question` in state for parallel branch execution.
    Fallback pattern: if Tavily fails, return empty results for this branch.
    """
    query = state.get("current_sub_question") or state.get("topic", "")
    tavily_api_key = state.get("tavily_api_key")
    if not tavily_api_key:
        import os

        tavily_api_key = os.getenv("TAVILY_API_KEY")

    try:
        client = TavilyClient(api_key=tavily_api_key)
        response = client.search(query=query, search_depth="advanced", max_results=5)
        results = response.get("results", [])
    except Exception:
        results = []

    # Each parallel branch returns just its own list for reducer fan-in.
    return {
        "search_results": results,
    }
