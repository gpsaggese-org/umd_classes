"""
Test that CDD modules work inside Docker.
Run with: pytest test/test_docker_all.py -v

These tests are designed to work WITHOUT real LLM API keys. Tests that
require an LLM call are skipped when no key is configured.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ============================================================================
# Section 1: Imports — all six modules must import cleanly
# ============================================================================
class TestImports:
    def test_import_config(self):
        import cdd_config
        assert len(cdd_config.DIAGRAM_TYPES) > 0
        assert len(cdd_config.SUPPORTED_FORMATS) == 3
        assert "graphviz" in cdd_config.SUPPORTED_FORMATS
        assert "mermaid" in cdd_config.SUPPORTED_FORMATS
        assert "plantuml" in cdd_config.SUPPORTED_FORMATS
        assert cdd_config.SYSTEM_PROMPTS["graphviz"]
        assert cdd_config.SYSTEM_PROMPTS["mermaid"]
        assert cdd_config.SYSTEM_PROMPTS["plantuml"]
        assert cdd_config.VISION_MAX_ITERATIONS == 3

    def test_import_llm(self):
        import cdd_llm
        assert hasattr(cdd_llm, "generate")
        assert hasattr(cdd_llm, "critique_image")
        assert hasattr(cdd_llm, "generate_dot")  # legacy alias

    def test_import_renderer(self):
        import cdd_renderer
        assert hasattr(cdd_renderer, "validate")
        assert hasattr(cdd_renderer, "render")
        assert hasattr(cdd_renderer, "validate_dot")  # legacy alias
        assert hasattr(cdd_renderer, "render_dot")  # legacy alias

    def test_import_orchestrator(self):
        from cdd_orchestrator import CDDOrchestrator
        orch = CDDOrchestrator()
        assert orch.state.revision_count == 0
        assert orch.state.format == "graphviz"

    def test_import_eval(self):
        import cdd_eval
        assert len(cdd_eval.EVAL_TEST_CASES) > 0
        # New eval has cases for all three formats
        formats = {c.get("format", "graphviz") for c in cdd_eval.EVAL_TEST_CASES}
        assert "graphviz" in formats
        assert "mermaid" in formats
        assert "plantuml" in formats

    def test_import_server(self):
        import cdd_server
        assert hasattr(cdd_server, "app")


# ============================================================================
# Section 2: Renderer — Graphviz works locally without network
# ============================================================================
class TestRendererGraphviz:
    def test_validate_good_dot(self):
        import cdd_renderer
        is_valid, error = cdd_renderer.validate("digraph { A -> B; }", "graphviz")
        assert is_valid is True

    def test_validate_bad_dot(self):
        import cdd_renderer
        is_valid, _ = cdd_renderer.validate("digraph { invalid syntax }}", "graphviz")
        assert is_valid is False

    def test_render_simple_dot(self):
        import cdd_renderer
        img = cdd_renderer.render("digraph { A -> B -> C; }", "graphviz")
        assert isinstance(img, bytes) and len(img) > 100

    def test_render_svg(self):
        import cdd_renderer
        svg = cdd_renderer.render_to_svg_string("digraph { X -> Y; }", "graphviz")
        assert "<svg" in svg

    def test_render_to_file(self):
        import cdd_renderer
        import tempfile
        path = os.path.join(tempfile.gettempdir(), "test_cdd.png")
        cdd_renderer.render_to_file("digraph { A -> B; }", path, format="graphviz")
        assert os.path.isfile(path)
        os.remove(path)

    # Legacy aliases must keep working
    def test_legacy_validate_dot(self):
        import cdd_renderer
        is_valid, _ = cdd_renderer.validate_dot("digraph { A -> B; }")
        assert is_valid is True

    def test_legacy_render_dot(self):
        import cdd_renderer
        img = cdd_renderer.render_dot("digraph { A -> B; }")
        assert isinstance(img, bytes) and len(img) > 100

    def test_legacy_dot_to_svg_string(self):
        import cdd_renderer
        svg = cdd_renderer.dot_to_svg_string("digraph { A -> B; }")
        assert "<svg" in svg


# ============================================================================
# Section 3: Renderer — Mermaid and PlantUML use network; integration-only
# ============================================================================
class TestRendererNetworkFormats:
    """These tests require network access. Skip if offline."""

    @pytest.mark.skip(reason="Requires network to kroki.io. Enable for integration runs.")
    def test_render_mermaid(self):
        import cdd_renderer
        img = cdd_renderer.render("graph TD\n  A --> B", "mermaid")
        assert isinstance(img, bytes) and len(img) > 100

    @pytest.mark.skip(reason="Requires network to plantuml.com. Enable for integration runs.")
    def test_render_plantuml(self):
        import cdd_renderer
        img = cdd_renderer.render("@startuml\nA -> B\n@enduml", "plantuml")
        assert isinstance(img, bytes) and len(img) > 100


# ============================================================================
# Section 4: LLM extraction — no network needed
# ============================================================================
class TestLLMExtraction:
    def test_fenced_dot(self):
        import cdd_llm
        out = cdd_llm._extract_code("```dot\ndigraph { A -> B; }\n```", "graphviz")
        assert out == "digraph { A -> B; }"

    def test_fenced_graphviz(self):
        import cdd_llm
        out = cdd_llm._extract_code("```graphviz\ndigraph G { X -> Y; }\n```", "graphviz")
        assert out == "digraph G { X -> Y; }"

    def test_raw_dot(self):
        import cdd_llm
        out = cdd_llm._extract_code("digraph { A -> B; }", "graphviz")
        assert out == "digraph { A -> B; }"

    def test_fenced_mermaid(self):
        import cdd_llm
        out = cdd_llm._extract_code("```mermaid\ngraph TD\n  A --> B\n```", "mermaid")
        assert out == "graph TD\n  A --> B"

    def test_raw_mermaid(self):
        import cdd_llm
        out = cdd_llm._extract_code("graph TD\n  X --> Y", "mermaid")
        assert "graph TD" in out

    def test_fenced_plantuml(self):
        import cdd_llm
        src = "```plantuml\n@startuml\nA -> B\n@enduml\n```"
        out = cdd_llm._extract_code(src, "plantuml")
        assert out == "@startuml\nA -> B\n@enduml"

    def test_raw_plantuml(self):
        import cdd_llm
        out = cdd_llm._extract_code("@startuml\nA -> B\n@enduml", "plantuml")
        assert out == "@startuml\nA -> B\n@enduml"

    # Legacy alias
    def test_legacy_extract_dot_code(self):
        import cdd_llm
        out = cdd_llm._extract_dot_code("```dot\ndigraph { A -> B; }\n```")
        assert out == "digraph { A -> B; }"


# ============================================================================
# Section 5: Critique parser — defensive against malformed JSON
# ============================================================================
class TestCritiqueParser:
    def test_parse_valid_critique(self):
        import cdd_llm
        raw = '{"is_acceptable": false, "issues": ["overlap"], "suggested_changes": "spread out"}'
        c = cdd_llm._parse_critique(raw)
        assert c["is_acceptable"] is False
        assert c["issues"] == ["overlap"]
        assert c["suggested_changes"] == "spread out"

    def test_parse_critique_with_fences(self):
        import cdd_llm
        raw = '```json\n{"is_acceptable": true, "issues": [], "suggested_changes": ""}\n```'
        c = cdd_llm._parse_critique(raw)
        assert c["is_acceptable"] is True

    def test_parse_critique_with_prose(self):
        import cdd_llm
        raw = 'Here is my analysis:\n{"is_acceptable": true, "issues": [], "suggested_changes": ""}\nDone.'
        c = cdd_llm._parse_critique(raw)
        assert c["is_acceptable"] is True

    def test_parse_critique_garbage_returns_safe_default(self):
        import cdd_llm
        c = cdd_llm._parse_critique("garbage that is not JSON at all")
        # Should fall back to is_acceptable=True so the loop terminates
        assert c["is_acceptable"] is True
        assert c["issues"] == []


# ============================================================================
# Section 6: Eval metrics — no network needed
# ============================================================================
class TestEvalGraphviz:
    def test_count_nodes_dot(self):
        import cdd_eval
        dot = 'digraph {\n  A [label="Start"];\n  B [label="End"];\n  A -> B;\n}'
        assert cdd_eval.count_nodes(dot, "graphviz") >= 2

    def test_count_edges_dot(self):
        import cdd_eval
        assert cdd_eval.count_edges("digraph { A -> B; B -> C; C -> D; }", "graphviz") == 3

    def test_has_labels_dot(self):
        import cdd_eval
        assert cdd_eval.has_labels('digraph { A [label="X"]; }', "graphviz") is True
        assert cdd_eval.has_labels("digraph { A -> B; }", "graphviz") is False

    def test_has_styles_dot(self):
        import cdd_eval
        assert cdd_eval.has_styles('digraph { A [color=red]; }', "graphviz") is True
        assert cdd_eval.has_styles("digraph { A -> B; }", "graphviz") is False

    def test_evaluate_single_dot(self):
        import cdd_eval
        r = cdd_eval.evaluate_single(
            "test", 'digraph { A [label="X", color=blue]; B; A -> B; }',
            format="graphviz",
        )
        assert r.syntax_valid and r.render_success


class TestEvalMermaid:
    def test_count_nodes_mermaid(self):
        import cdd_eval
        src = "graph TD\n  A[Start] --> B[Middle]\n  B --> C[End]"
        assert cdd_eval.count_nodes(src, "mermaid") >= 3

    def test_count_edges_mermaid(self):
        import cdd_eval
        src = "graph TD\n  A --> B\n  B --> C"
        assert cdd_eval.count_edges(src, "mermaid") == 2

    def test_has_labels_mermaid(self):
        import cdd_eval
        assert cdd_eval.has_labels("graph TD\n  A[Hello]", "mermaid") is True


class TestEvalPlantUML:
    def test_count_nodes_plantuml(self):
        import cdd_eval
        src = "@startuml\nactor User\nparticipant Server\nUser -> Server\n@enduml"
        assert cdd_eval.count_nodes(src, "plantuml") >= 2

    def test_count_edges_plantuml(self):
        import cdd_eval
        src = "@startuml\nA -> B\nB -> C\n@enduml"
        assert cdd_eval.count_edges(src, "plantuml") == 2


# ============================================================================
# Section 7: Orchestrator — no LLM call needed for state tests
# ============================================================================
class TestOrchestrator:
    def test_init(self):
        from cdd_orchestrator import CDDOrchestrator
        o = CDDOrchestrator()
        assert o.state.revision_count == 0
        assert o.state.format == "graphviz"

    def test_init_with_format(self):
        from cdd_orchestrator import CDDOrchestrator
        o = CDDOrchestrator(format="mermaid")
        assert o.state.format == "mermaid"

    def test_reset(self):
        from cdd_orchestrator import CDDOrchestrator
        o = CDDOrchestrator()
        o.state.diagram_source = "test"
        o.state.revision_count = 5
        o.reset()
        assert o.state.revision_count == 0
        assert o.state.diagram_source == ""

    def test_state_dict_has_legacy_dot_source(self):
        from cdd_orchestrator import CDDOrchestrator
        d = CDDOrchestrator().get_state_dict()
        # Both new and legacy keys should be present
        assert "diagram_source" in d
        assert "dot_source" in d
        assert "format" in d
        assert "revision_count" in d


# ============================================================================
# Section 8: Server routes — no LLM calls for these
# ============================================================================
class TestServerRoutes:
    @pytest.fixture
    def client(self):
        from fastapi.testclient import TestClient
        from cdd_server import app
        return TestClient(app)

    def test_get_config(self, client):
        r = client.get("/api/config")
        assert r.status_code == 200
        data = r.json()
        assert "formats" in data
        assert "graphviz" in data["formats"]
        assert "mermaid" in data["formats"]
        assert "plantuml" in data["formats"]
        assert "vision_feedback_enabled" in data
        assert data["vision_max_iterations"] == 3

    def test_reset_nonexistent(self, client):
        r = client.post("/api/reset?session_id=doesnotexist")
        assert r.status_code == 200

    def test_export_no_session(self, client):
        r = client.post(
            "/api/export",
            json={"session_id": "nope", "format": "png"},
        )
        assert r.status_code == 404

    def test_invalid_format_returns_400(self, client):
        r = client.post(
            "/api/chat",
            json={"message": "hi", "format": "invalid_format"},
        )
        assert r.status_code == 400


# ============================================================================
# Section 9: Notebook smoke test — paired .py + .ipynb files
# ============================================================================
class TestNotebookPairing:
    """Verify the jupytext-paired Python files are syntactically valid."""

    def test_api_notebook_py_imports(self):
        # The .py file paired with cdd.API.ipynb must at least be valid Python
        import ast
        path = os.path.join(os.path.dirname(__file__), "..", "cdd.API.py")
        with open(path) as f:
            ast.parse(f.read())

    def test_example_notebook_py_imports(self):
        import ast
        path = os.path.join(os.path.dirname(__file__), "..", "cdd.example.py")
        with open(path) as f:
            ast.parse(f.read())
