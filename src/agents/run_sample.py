from __future__ import annotations

import argparse

from src.graph.builder import build_graph


def main(topic: str) -> None:
    app = build_graph()
    initial_state = {
        "topic": topic,
        "sub_questions": [],
        "search_results": [],
        "summaries": [],
        "critic_scores": [],
        "filtered_results": [],
        "final_report": "",
    }

    final_state = app.invoke(initial_state)

    print("=== Critic Scores ===")
    for score in final_state.get("critic_scores", []):
        print(score)

    print("\n=== Final Report ===")
    print(final_state.get("final_report", ""))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Phase 3 parallel research graph")
    parser.add_argument("topic", type=str)
    args = parser.parse_args()
    main(args.topic)
