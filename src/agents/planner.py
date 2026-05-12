from __future__ import annotations

from typing import Any, Dict, List

from langchain_openai import ChatOpenAI


def planner_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Plan sub-questions from a topic.

    Fallback pattern: if the LLM call fails, use a deterministic single sub-question.
    """
    topic = state.get("topic", "")
    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        prompt = (
            "Break the research topic into 3 concise sub-questions. "
            "Return each on its own line.\n\n"
            f"Topic: {topic}"
        )
        response = llm.invoke(prompt)
        text = response.content if isinstance(response.content, str) else str(response.content)
        sub_questions = [line.strip("- •\t ") for line in text.splitlines() if line.strip()]
        if not sub_questions:
            sub_questions = [f"What are the key facts about {topic}?"]
    except Exception:
        sub_questions = [f"What are the key facts about {topic}?"]

    return {**state, "sub_questions": sub_questions}
