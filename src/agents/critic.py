from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI


def critic_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Score search results and filter out low-quality items.

    Fallback pattern: if scoring fails, assign neutral scores and keep all items.
    """
    results: List[dict[str, Any]] = state.get("search_results", [])

    if not results:
        return {**state, "critic_scores": [], "filtered_results": []}

    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        payload = json.dumps(results, ensure_ascii=False)
        prompt = (
            "You are a strict research critic. For each input result, score: "
            "relevance (0-10) and credibility (0-10). "
            "Return ONLY JSON array where each item has keys: "
            "index, relevance, credibility, reason.\n\n"
            f"Results: {payload}"
        )
        response = llm.invoke(prompt)
        text = response.content if isinstance(response.content, str) else str(response.content)
        scores = json.loads(text)
    except Exception:
        scores = [
            {"index": idx, "relevance": 5, "credibility": 5, "reason": "Fallback neutral score"}
            for idx, _ in enumerate(results)
        ]

    filtered: List[dict[str, Any]] = []
    normalized_scores: List[dict[str, Any]] = []
    for item in scores:
        idx = int(item.get("index", -1))
        rel = float(item.get("relevance", 0))
        cred = float(item.get("credibility", 0))
        avg = (rel + cred) / 2
        score_item = {**item, "average": avg}
        normalized_scores.append(score_item)
        if avg >= 5 and 0 <= idx < len(results):
            filtered.append(results[idx])

    return {**state, "critic_scores": normalized_scores, "filtered_results": filtered}
