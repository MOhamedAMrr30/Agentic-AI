# Multi-agent Research Assistant

Step-by-step build of a LangGraph multi-agent research system.

## Current status

### Phase 1 (in progress)
- [x] Python project scaffold created
- [x] Core dependency list added
- [x] Environment variable template added
- [x] API connectivity check script added

### Phase 2 (started)
- [x] Shared `TypedDict` state schema scaffolded
- [x] Planner/Search/Summarizer node stubs scaffolded
- [x] Basic `StateGraph` wiring scaffolded
- [ ] Real LLM + Tavily integration

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then add your API keys to `.env`.

## Run checks

```bash
python scripts/test_api_keys.py
```

## Run API health endpoint

```bash
uvicorn src.api.main:app --reload
```
