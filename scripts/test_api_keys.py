"""Quick connectivity checks for OpenAI and Tavily."""

import os

from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient


def main() -> None:
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

    if not openai_key or not tavily_key:
        raise SystemExit("Missing OPENAI_API_KEY or TAVILY_API_KEY in environment.")

    openai_client = OpenAI(api_key=openai_key)
    openai_models = openai_client.models.list()
    print(f"OpenAI connectivity OK. Retrieved {len(openai_models.data)} models.")

    tavily_client = TavilyClient(api_key=tavily_key)
    search_resp = tavily_client.search(query="ping", max_results=1)
    count = len(search_resp.get("results", []))
    print(f"Tavily connectivity OK. Retrieved {count} result(s).")


if __name__ == "__main__":
    main()
