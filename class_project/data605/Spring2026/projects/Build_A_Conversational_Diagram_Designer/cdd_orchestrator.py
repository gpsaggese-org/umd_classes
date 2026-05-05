# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # CDD Orchestrator
#
# Coordinates the user-turn pipeline:
#
#   user message
#     -> LLM generate (text -> diagram code)
#     -> renderer (code -> image bytes)
#     -> if vision feedback enabled:
#          -> multimodal critique (image + intent -> JSON critique)
#          -> if not acceptable and iterations < cap:
#               -> regenerate with critique appended
#               -> loop
#     -> return final code, image, and trace
#
# The trace records every step so the eval harness and the report can
# answer "what happened during this turn".

# %%
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

import cdd_config as config
import cdd_llm as llm
import cdd_renderer as renderer


# %% [markdown]
# ## State container

# %%
@dataclass
class DiagramState:
    """Holds the current state of a diagram conversation."""
    diagram_source: str = ""
    format: str = config.DEFAULT_FORMAT
    conversation_history: list = field(default_factory=list)
    diagram_type: str = ""
    revision_count: int = 0
    created_at: str = ""
    last_modified: str = ""
    last_trace: list = field(default_factory=list)
    # New: diagram description + suggestions for further changes,
    # produced after the final render by a multimodal LLM call.
    last_description: str = ""
    last_suggestions: list = field(default_factory=list)

    # Legacy alias for backwards compatibility with the original tests
    @property
    def dot_source(self) -> str:
        return self.diagram_source

    @dot_source.setter
    def dot_source(self, value: str) -> None:
        self.diagram_source = value

    def to_dict(self) -> dict:
        return {
            "diagram_source": self.diagram_source,
            "dot_source": self.diagram_source,  # legacy key
            "format": self.format,
            "conversation_history": self.conversation_history,
            "diagram_type": self.diagram_type,
            "revision_count": self.revision_count,
            "created_at": self.created_at,
            "last_modified": self.last_modified,
            "last_trace": self.last_trace,
            "last_description": self.last_description,
            "last_suggestions": self.last_suggestions,
        }


# %% [markdown]
# ## Orchestrator

# %%
class CDDOrchestrator:
    """Drives one user turn through the full CDD pipeline."""

    def __init__(
        self,
        provider: Optional[str] = None,
        format: str = config.DEFAULT_FORMAT,
        vision_feedback: bool = config.VISION_FEEDBACK_ENABLED,
        max_iterations: int = config.VISION_MAX_ITERATIONS,
    ):
        self.state = DiagramState(format=format)
        self.provider = provider
        self.vision_feedback = vision_feedback
        self.max_iterations = max_iterations

    # ---- Public API ----

    def process_message(self, user_message: str) -> tuple:
        """Process a user message: generate, render, optionally critique-and-iterate.

        Returns (diagram_source, image_bytes). The trace is on self.state.last_trace.
        """
        trace: list = []

        # Build context-aware prompt: include the current diagram if there is one
        prompt_for_llm = self._build_prompt(user_message)

        diagram_source = ""
        image_bytes = b""

        for iteration in range(1, self.max_iterations + 1):
            # 1. Generate
            diagram_source = llm.generate(
                prompt_for_llm,
                format=self.state.format,
                conversation_history=self.state.conversation_history,
                provider=self.provider,
            )
            trace.append({
                "iteration": iteration,
                "step": "generate",
                "format": self.state.format,
                "code_length": len(diagram_source),
            })

            # 2. Validate / render. If render fails, do one syntax-repair pass
            # within this iteration. Vision-loop iterations are separate.
            is_valid, error = renderer.validate(diagram_source, self.state.format)
            if not is_valid:
                trace.append({
                    "iteration": iteration, "step": "syntax_error",
                    "error": error[:200],
                })
                diagram_source = self._syntax_repair(
                    diagram_source, error, user_message,
                )
                is_valid, error = renderer.validate(diagram_source, self.state.format)
                if not is_valid:
                    if iteration < self.max_iterations:
                        # Try a fresh generation with the syntax error context
                        prompt_for_llm = (
                            f"The previous attempt produced invalid {self.state.format} "
                            f"code with this error: {error[:200]}\n\n"
                            f"Original request: {user_message}\n\n"
                            f"Produce a corrected diagram."
                        )
                        continue
                    raise ValueError(f"Failed to generate valid code: {error}")

            try:
                image_bytes = renderer.render(diagram_source, self.state.format)
            except Exception as e:
                trace.append({
                    "iteration": iteration, "step": "render_failed",
                    "error": str(e)[:200],
                })
                if iteration < self.max_iterations:
                    prompt_for_llm = (
                        f"The previous diagram rendered but produced an error: {e}\n\n"
                        f"Original request: {user_message}\n\n"
                        f"Produce a corrected diagram."
                    )
                    continue
                raise

            trace.append({
                "iteration": iteration, "step": "rendered",
                "image_bytes": len(image_bytes),
            })

            # 3. Vision feedback (if enabled and we have iterations left)
            if not self.vision_feedback:
                trace.append({"iteration": iteration, "step": "stop_vision_disabled"})
                break

            if iteration >= self.max_iterations:
                trace.append({"iteration": iteration, "step": "stop_max_iterations"})
                break

            critique = self._safe_critique(image_bytes, user_message, diagram_source)
            trace.append({
                "iteration": iteration,
                "step": "vision_critique",
                "is_acceptable": critique["is_acceptable"],
                "issue_count": len(critique["issues"]),
            })

            if critique["is_acceptable"]:
                trace.append({"iteration": iteration, "step": "stop_accepted"})
                break

            # Build the next-iteration prompt
            issues_text = "\n".join(f"- {i}" for i in critique["issues"])
            prompt_for_llm = (
                f"The diagram has these visual issues:\n{issues_text}\n\n"
                f"Suggested changes: {critique['suggested_changes']}\n\n"
                f"Original request: {user_message}\n\n"
                f"Current code:\n```\n{diagram_source}\n```\n\n"
                f"Produce a corrected diagram in valid {self.state.format} syntax."
            )

        # 4. Describe the final diagram + suggest further changes.
        # Non-fatal: if this call fails, fields stay empty and the UI
        # just shows the diagram without the description block.
        describe_result = self._safe_describe(
            image_bytes, user_message, diagram_source,
        )
        trace.append({
            "step": "describe_suggest",
            "has_description": bool(describe_result["description"]),
            "suggestion_count": len(describe_result["suggestions"]),
        })

        # 5. Commit state
        now = datetime.now().isoformat()
        if not self.state.created_at:
            self.state.created_at = now
        self.state.last_modified = now
        self.state.diagram_source = diagram_source
        self.state.revision_count += 1
        self.state.last_trace = trace
        self.state.last_description = describe_result["description"]
        self.state.last_suggestions = describe_result["suggestions"]
        self.state.conversation_history.append(
            {"role": "user", "content": user_message}
        )
        self.state.conversation_history.append(
            {"role": "assistant", "content": diagram_source}
        )

        return diagram_source, image_bytes

    def export_dot(self, filepath: str) -> str:
        """Legacy: write current diagram source (any format) to disk."""
        with open(filepath, "w") as f:
            f.write(self.state.diagram_source)
        return filepath

    def export_image(self, filepath: str, fmt: str = "png") -> str:
        return renderer.render_to_file(
            self.state.diagram_source, filepath,
            format=self.state.format, output_format=fmt,
        )

    def get_state_dict(self) -> dict:
        return self.state.to_dict()

    def reset(self):
        fmt = self.state.format
        self.state = DiagramState(format=fmt)

    # ---- Internals ----

    def _build_prompt(self, user_message: str) -> str:
        if self.state.diagram_source:
            return (
                f"Current diagram ({self.state.format}):\n"
                f"```\n{self.state.diagram_source}\n```\n\n"
                f"User request: {user_message}"
            )
        return user_message

    def _syntax_repair(self, code: str, error: str, original_intent: str) -> str:
        """One-shot syntax repair pass when validation fails."""
        repair_msg = (
            f"The {self.state.format} code below has a syntax error:\n{error}\n\n"
            f"Original code:\n```\n{code}\n```\n\n"
            f"Original user request: {original_intent}\n\n"
            f"Return corrected {self.state.format} code only."
        )
        return llm.generate(
            repair_msg, format=self.state.format, provider=self.provider,
        )

    def _safe_critique(
        self, image_bytes: bytes, intent: str, code: str,
    ) -> dict:
        """Critique with defensive error handling — never crash the loop."""
        try:
            return llm.critique_image(
                image_bytes=image_bytes,
                user_intent=intent,
                diagram_code=code,
                provider=self.provider,
            )
        except Exception:
            # If the critique call fails (network, parse, quota), accept the
            # current diagram and stop iterating.
            return {
                "is_acceptable": True,
                "issues": [],
                "suggested_changes": "",
            }

    def _safe_describe(
        self, image_bytes: bytes, intent: str, code: str,
    ) -> dict:
        """Describe + suggest with defensive error handling.

        Returns {"description": str, "suggestions": list[str]}. If the call
        fails for any reason, returns empty fields so the user still gets
        their diagram with no surprises.
        """
        try:
            return llm.describe_and_suggest(
                image_bytes=image_bytes,
                user_intent=intent,
                diagram_code=code,
                diagram_format=self.state.format,
                provider=self.provider,
            )
        except Exception:
            return {"description": "", "suggestions": []}