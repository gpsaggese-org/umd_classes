"""
FastAPI server exposing the agentic research pipeline.

Endpoints:
  - GET  /                  : health probe + capability summary
  - POST /research          : run the pipeline synchronously, return one
                              JSON document with the full trace
  - POST /research/stream   : run the pipeline as Server-Sent Events so a
                              UI can show each step as it happens

Run:
  uvicorn app.api.server:app --host 0.0.0.0 --port 8000
"""

import json
import logging
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.agents.research_agent import run_research, run_research_sync

_LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="txtai Market Research Agent",
    description="Agentic search over SEC filings + news for 67 tickers.",
    version="0.1.0",
)

# Allow the Streamlit UI (running on :8501) to call us.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# #############################################################################
# Schemas
# #############################################################################


class ResearchRequest(BaseModel):
    """
    Request body for ``/research`` and ``/research/stream``.
    """

    query: str


# #############################################################################
# Routes
# #############################################################################


@app.get("/")
def root() -> dict[str, Any]:
    """
    Health probe; lists the available endpoints so a fresh dev knows what's
    wired up without opening the OpenAPI docs.
    """
    return {
        "service": "txtai Market Research Agent",
        "endpoints": {
            "POST /research": "Run pipeline, return full result as JSON.",
            "POST /research/stream": "Run pipeline, stream events as SSE.",
        },
    }


@app.post("/research")
def research(req: ResearchRequest) -> dict[str, Any]:
    """
    Run the research pipeline and return the final answer plus trace.

    :param req: JSON body with a ``query`` field
    :return: dict with keys ``query``, ``route``, ``retrievals``, ``answer``,
             ``used_llm``, ``chunk_count``
    """
    _LOG.info("Sync research query=%s", req.query)
    return run_research_sync(req.query)


def _sse_stream(query: str):
    """
    Adapt the research generator to the Server-Sent Events wire format.

    Each yielded event is encoded as ``data: <json>\\n\\n`` so any standard
    SSE client (browser EventSource, httpx, requests with stream=True) can
    parse it.

    :param query: user query passed through to ``run_research``
    :yield: bytes ready to send on the wire
    """
    try:
        for event in run_research(query):
            # Strip the heavyweight "chunks" payload from the wire — full
            # text would blow up the SSE buffer for large responses.  We
            # send a compact preview instead; the final synthesise step
            # already references the originals via citations.
            payload = dict(event["payload"])
            if "chunks" in payload:
                payload["chunks"] = [
                    {
                        "score": c.get("score"),
                        "text": (c.get("text") or "")[:400],
                        "metadata": c.get("metadata"),
                        "tags": c.get("tags"),
                    }
                    for c in payload["chunks"]
                ]
            line = json.dumps({"step": event["step"], "payload": payload})
            yield f"data: {line}\n\n"
    except Exception as e:
        _LOG.exception("Stream failed")
        err = json.dumps({"step": "error", "payload": {"message": str(e)}})
        yield f"data: {err}\n\n"


@app.post("/research/stream")
def research_stream(req: ResearchRequest) -> StreamingResponse:
    """
    Run the pipeline as Server-Sent Events.

    The response media type is ``text/event-stream`` and each event is a
    single ``data: {...}`` line followed by a blank line, exactly as
    specified by the EventSource protocol.

    :param req: JSON body with a ``query`` field
    :return: streaming response that emits one event per pipeline step
    """
    _LOG.info("Stream research query=%s", req.query)
    return StreamingResponse(
        _sse_stream(req.query),
        media_type="text/event-stream",
    )
