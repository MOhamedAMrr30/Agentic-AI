"""Run the phase-2 graph end-to-end with a sample topic."""

from src.agents.graph import build_graph


if __name__ == "__main__":
    graph = build_graph()
    initial_state = {"topic": "Multi-agent AI for enterprise research workflows"}
    final_state = graph.invoke(initial_state)

    print("Sub-questions:")
    for q in final_state.get("sub_questions", []):
        print(f"- {q}")

    print("\nReport:\n")
    print(final_state.get("report", ""))
