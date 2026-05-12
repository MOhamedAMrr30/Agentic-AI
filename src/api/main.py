"""FastAPI app skeleton for later phases."""

from fastapi import FastAPI

app = FastAPI(title="Multi-Agent Research Assistant")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
