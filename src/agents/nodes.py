"""Phase 2 nodes for Planner -> Search -> Summarizer."""

from __future__ import annotations

import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

from .state import ResearchState, SearchResult


SYSTEM_PLANNER_PROMPT = (
    "Decompose the user's research topic into 3 to 5 concise sub-questions. "
    "Return each sub-question on a new line with no numbering."
)


SYSTEM_SUMMARIZER_PROMPT = (
    "You are a research summarizer. Given snippets for one sub-question, "
    "write a concise 3-5 sentence summary grounded in the snippets."
)


def _fallback_sub_questions(topic: str) -> list[str]:
    return [
        f"What is the current landscape of {topic}?",
        f"What are key technical approaches in {topic}?",
        f"What are the risks, limitations, or trade-offs in {topic}?",
    ]


def planner_node(state: ResearchState) -> ResearchState:
    """Decompose a topic into sub-questions via LLM, fallback if no API key."""
    topic = state.get("topic", "").strip()
    if not topic:
        return {**state, "sub_questions": []}

    openai_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    if not openai_key or OpenAI is None:
        return {**state, "sub_questions": _fallback_sub_questions(topic)}

    client = OpenAI(api_key=openai_key)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PLANNER_PROMPT},
            {"role": "user", "content": topic},
        ],
        temperature=0.2,
    )

    lines = [line.strip(" -\t") for line in response.output_text.splitlines() if line.strip()]
    sub_questions = lines[:5] if lines else _fallback_sub_questions(topic)
    return {**state, "sub_questions": sub_questions}


def search_node(state: ResearchState) -> ResearchState:
    """Run Tavily search for each sub-question and collect snippets/sources."""
    sub_questions = state.get("sub_questions", [])
    tavily_key = os.getenv("TAVILY_API_KEY")

    if not tavily_key or TavilyClient is None:
        results: list[SearchResult] = [
            {"question": q, "snippets": ["No Tavily key configured; search skipped."], "sources": []}
            for q in sub_questions
        ]
        return {**state, "search_results": results}

    client = TavilyClient(api_key=tavily_key)
    search_results: list[SearchResult] = []

    for question in sub_questions:
        resp = client.search(query=question, max_results=5)
        raw_items = resp.get("results", [])
        snippets = [item.get("content", "").strip() for item in raw_items if item.get("content")]
        sources = [{"title": item.get("title"), "url": item.get("url")} for item in raw_items]
        search_results.append({"question": question, "snippets": snippets[:5], "sources": sources})

    return {**state, "search_results": search_results}


def summarizer_node(state: ResearchState) -> ResearchState:
    """Summarize each search result into 3-5 sentences and build report."""
    openai_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    results = state.get("search_results", [])

    summaries: list[str] = []

    if openai_key and OpenAI is not None:
        client = OpenAI(api_key=openai_key)
        for item in results:
            question = item.get("question", "Unknown question")
            snippets = item.get("snippets", [])
            snippet_block = "\n".join(f"- {s}" for s in snippets) if snippets else "- No snippets available"
            response = client.responses.create(
                model=model,
                input=[
                    {"role": "system", "content": SYSTEM_SUMMARIZER_PROMPT},
                    {
                        "role": "user",
                        "content": f"Sub-question: {question}\n\nSnippets:\n{snippet_block}",
                    },
                ],
                temperature=0.2,
            )
            summaries.append(f"{question}\n{response.output_text.strip()}")
    else:
        for item in results:
            question = item.get("question", "Unknown question")
            snippets = item.get("snippets", [])
            preview = snippets[0] if snippets else "No snippet available."
            summaries.append(f"{question}\nSummary placeholder: {preview}")

    report = "\n\n".join(summaries)
    return {**state, "summaries": summaries, "report": report}
