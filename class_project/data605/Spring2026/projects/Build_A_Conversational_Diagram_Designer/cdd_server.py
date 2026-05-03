# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # CDD Server
#
# FastAPI backend serving the React frontend and exposing the CDD API.
# Single-image deployment: this server, once mounted on /api/*, also serves
# the React static bundle at / for everything else.

# %%
import base64
import os
import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from cdd_orchestrator import CDDOrchestrator
import cdd_renderer as renderer
import cdd_config as config

# %%
app = FastAPI(title="CDD API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# %% [markdown]
# ## Session store
#
# In-memory only. The brief explicitly lists persistence as a non-goal for V1.

# %%
sessions: dict[str, CDDOrchestrator] = {}


def get_or_create_session(
    session_id: Optional[str],
    format: str,
    vision_feedback: bool,
) -> tuple[str, CDDOrchestrator]:
    if session_id and session_id in sessions:
        orch = sessions[session_id]
        # Update knobs in case the user toggled them
        orch.state.format = format
        orch.vision_feedback = vision_feedback
        return session_id, orch
    new_id = str(uuid.uuid4())
    sessions[new_id] = CDDOrchestrator(
        format=format, vision_feedback=vision_feedback,
    )
    return new_id, sessions[new_id]


# %% [markdown]
# ## Request / Response models

# %%
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    provider: Optional[str] = None
    format: str = config.DEFAULT_FORMAT
    vision_feedback: bool = config.VISION_FEEDBACK_ENABLED


class ChatResponse(BaseModel):
    session_id: str
    diagram_source: str
    image_base64: str
    image_mime: str
    format: str
    revision: int
    iterations: int
    trace: list
    message: str
    # Plain-English description of what the diagram shows, plus a list of
    # concrete suggestions for further changes. Both produced by a multimodal
    # LLM call after the final render. May be empty strings/lists if the
    # call failed or the model returned nothing parseable.
    description: str = ""
    suggestions: list = []


class ExportRequest(BaseModel):
    session_id: str
    format: str = "png"  # png, svg, dot/source


# %% [markdown]
# ## API endpoints

# %%
@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Send a message to generate or refine a diagram."""
    if req.format not in config.SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format: {req.format}. "
                   f"Choose from {config.SUPPORTED_FORMATS}.",
        )

    sid, orch = get_or_create_session(req.session_id, req.format, req.vision_feedback)
    if req.provider:
        orch.provider = req.provider

    try:
        diagram_source, image_bytes = orch.process_message(req.message)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    img_b64 = base64.b64encode(image_bytes).decode("utf-8")
    # Mermaid and PlantUML default to PNG; Graphviz too. We always send PNG to the UI.
    return ChatResponse(
        session_id=sid,
        diagram_source=diagram_source,
        image_base64=img_b64,
        image_mime="image/png",
        format=req.format,
        revision=orch.state.revision_count,
        iterations=len(orch.state.last_trace),
        trace=orch.state.last_trace,
        message=f"Diagram generated (revision {orch.state.revision_count})",
        description=orch.state.last_description,
        suggestions=orch.state.last_suggestions,
    )


@app.post("/api/export")
async def export_diagram(req: ExportRequest):
    """Export the current diagram in the requested format."""
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    orch = sessions[req.session_id]
    if not orch.state.diagram_source:
        raise HTTPException(status_code=400, detail="No diagram to export")

    if req.format in ("dot", "source", "txt"):
        return Response(
            content=orch.state.diagram_source,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename=diagram.{req.format}"},
        )

    fmt = req.format if req.format in ("png", "svg") else "png"
    try:
        image_bytes = renderer.render(
            orch.state.diagram_source,
            format=orch.state.format,
            output_format=fmt,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    media_types = {"png": "image/png", "svg": "image/svg+xml"}
    return Response(
        content=image_bytes,
        media_type=media_types.get(fmt, "application/octet-stream"),
        headers={"Content-Disposition": f"attachment; filename=diagram.{fmt}"},
    )


@app.post("/api/reset")
async def reset_session(session_id: str):
    """Reset a diagram session."""
    if session_id in sessions:
        sessions[session_id].reset()
    return {"status": "ok"}


@app.get("/api/config")
async def get_config():
    """Return public config (formats, providers, vision toggle)."""
    providers = []
    if config.GEMINI_API_KEY:
        providers.append("gemini")
    if config.OPENAI_API_KEY:
        providers.append("openai")
    if config.ANTHROPIC_API_KEY:
        providers.append("anthropic")
    return {
        "diagram_types": config.DIAGRAM_TYPES,
        "formats": config.SUPPORTED_FORMATS,
        "default_format": config.DEFAULT_FORMAT,
        "providers": providers,
        "default_provider": config.LLM_PROVIDER,
        "vision_feedback_enabled": config.VISION_FEEDBACK_ENABLED,
        "vision_max_iterations": config.VISION_MAX_ITERATIONS,
    }


# %% [markdown]
# ## Static frontend (must mount LAST so /api/* takes priority)

# %%
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.isdir(FRONTEND_DIR):
    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")),
        name="assets",
    )

    @app.get("/{path:path}")
    async def serve_react(path: str):
        """Serve the React SPA — non-API routes fall through to index.html."""
        file_path = os.path.join(FRONTEND_DIR, path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))