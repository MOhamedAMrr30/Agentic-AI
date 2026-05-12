# Multi-agent Research Assistant

Step-by-step build of a LangGraph multi-agent research system.

## Current status

### Phase 1
- [x] Python project scaffold created
- [x] Core dependency list added
- [x] Environment variable template added
- [x] API connectivity check script added

### Phase 2
- [x] Shared `TypedDict` state schema scaffolded
- [x] Planner node implemented (LLM + fallback)
- [x] Search node implemented (Tavily + fallback)
- [x] Summarizer node implemented (LLM + fallback)
- [x] `StateGraph` wiring scaffolded
- [x] Sample end-to-end runner added

### Next
- [ ] Phase 3 parallel fan-out/fan-in
- [ ] Critic node
- [ ] Synthesizer node

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your API keys to `.env`.

## Run checks

```bash
python scripts/test_api_keys.py
pytest -q
```

## Run sample graph

```bash
python -m src.agents.run_sample
```

## Run API health endpoint

```bash
uvicorn src.api.main:app --reload
```
