from __future__ import annotations

import os
from typing import Any, List, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from langchain_openai import ChatOpenAI
from tavily import TavilyClient


class ResearchState(TypedDict):
    topic: str
    search_results: List[dict[str, Any]]
    summary: str
    messages: List[str]


def search_node(state: ResearchState) -> ResearchState:
    """Search the web for the requested topic using Tavily."""
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY is not set in the environment.")

    client = TavilyClient(api_key=tavily_api_key)
    response = client.search(query=state["topic"], search_depth="advanced", max_results=5)
    results = response.get("results", [])

    return {
        **state,
        "search_results": results,
        "messages": state.get("messages", []) + [
            f"Collected {len(results)} search results for topic: {state['topic']}"
        ],
    }


def summarize_node(state: ResearchState) -> ResearchState:
    """Summarize Tavily search results into a concise paragraph using GPT-4o."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")

    llm = ChatOpenAI(model="gpt-4o", api_key=openai_api_key, temperature=0)

    formatted_results = "\n\n".join(
        f"Title: {item.get('title', 'N/A')}\n"
        f"URL: {item.get('url', 'N/A')}\n"
        f"Content: {item.get('content', '')}"
        for item in state.get("search_results", [])
    )

    prompt = (
        "You are a research assistant. Summarize the following search findings "
        "into one concise, factual paragraph:\n\n"
        f"Topic: {state['topic']}\n\n"
        f"Search Results:\n{formatted_results}"
    )

    response = llm.invoke(prompt)
    summary_text = response.content.strip() if isinstance(response.content, str) else str(response.content)

    return {
        **state,
        "summary": summary_text,
        "messages": state.get("messages", []) + ["Generated final summary."],
    }


def build_graph():
    workflow = StateGraph(ResearchState)

    workflow.add_node("search_node", search_node)
    workflow.add_node("summarize_node", summarize_node)

    workflow.add_edge(START, "search_node")
    workflow.add_edge("search_node", "summarize_node")
    workflow.add_edge("summarize_node", END)

    return workflow.compile()


def main(topic: str) -> None:
    load_dotenv()

    graph = build_graph()
    initial_state: ResearchState = {
        "topic": topic,
        "search_results": [],
        "summary": "",
        "messages": [],
    }

    final_state = graph.invoke(initial_state)
    print(final_state["summary"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a LangGraph research assistant.")
    parser.add_argument("topic", type=str, help="Topic to research")
    args = parser.parse_args()

    main(args.topic)
