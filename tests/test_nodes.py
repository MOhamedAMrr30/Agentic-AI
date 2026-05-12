from src.agents.nodes import planner_node, search_node, summarizer_node


def test_planner_fallback_without_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    state = planner_node({"topic": "agentic ai"})
    assert len(state["sub_questions"]) >= 3


def test_search_fallback_without_tavily_key(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    state = search_node({"sub_questions": ["What is agentic AI?"]})
    assert state["search_results"][0]["question"] == "What is agentic AI?"


def test_summarizer_fallback_without_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    state = summarizer_node(
        {
            "search_results": [
                {
                    "question": "What is agentic AI?",
                    "snippets": ["Agentic AI systems can plan and execute actions."],
                }
            ]
        }
    )
    assert "Summary placeholder" in state["report"]
