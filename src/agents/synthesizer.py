from __future__ import annotations

from typing import Any, Dict, List

from langchain_openai import ChatOpenAI


def synthesizer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Build a structured final report.

    Fallback pattern: if synthesis fails, create a simple deterministic report.
    """
    filtered_results: List[dict[str, Any]] = state.get("filtered_results", [])
    topic = state.get("topic", "")

    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        prompt = (
            "Create a structured research report with sections exactly:\n"
            "Introduction\nKey Findings\nSource Analysis\nConclusion\n\n"
            "Use the provided filtered search results and be concise but specific.\n\n"
            f"Topic: {topic}\n\n"
            f"Filtered Results: {filtered_results}"
        )
        response = llm.invoke(prompt)
        report = response.content if isinstance(response.content, str) else str(response.content)
    except Exception:
        report = (
            f"Introduction\nThis report summarizes findings about {topic}.\n\n"
            "Key Findings\nNo high-confidence synthesized findings available.\n\n"
            "Source Analysis\nAutomatic synthesis fallback was used.\n\n"
            "Conclusion\nCollect additional credible sources for stronger conclusions."
        )

    return {**state, "final_report": report}
