# # CDD Renderer
#
# Unified rendering interface for the three supported formats.
# All renderers expose the same shape: validate(code) returns (bool, error_msg)
# and render(code, fmt) returns image bytes.

# - Graphviz: local rendering via the `graphviz` Python wrapper around the
#   `dot` binary (must be installed in the container).
# - Mermaid: rendered via the public Kroki render server (kroki.io). We send
#   the Mermaid source and get back PNG/SVG bytes. Trade-off documented in
#   the report: Mermaid requires network. The CheerpJ-based browser library
#   has known correctness issues so we use the server.

# - PlantUML: rendered via the public PlantUML server. Source is encoded
#   using the deflate + base64 scheme PlantUML uses, then fetched over HTTP.

import base64
import zlib
from typing import Optional, Tuple

import graphviz
import requests

import cdd_config as config


# ## Graphviz (local)

def _validate_graphviz(dot_source: str) -> Tuple[bool, str]:
    """Validate DOT syntax by attempting a render."""
    try:
        src = graphviz.Source(dot_source)
        src.pipe(format="svg")
        return True, ""
    except graphviz.backend.execute.CalledProcessError as e:
        return False, str(e.stderr)
    except Exception as e:
        return False, str(e)


def _render_graphviz(
    dot_source: str,
    output_format: str,
    engine: Optional[str] = None,
) -> bytes:
    eng = engine or config.GRAPHVIZ_ENGINE
    src = graphviz.Source(dot_source, engine=eng)
    return src.pipe(format=output_format)


# ## Mermaid (Kroki render server)


def _kroki_encode(source: str) -> str:
    """Encode source for the Kroki URL scheme: deflate + urlsafe base64."""
    compressed = zlib.compress(source.encode("utf-8"), 9)
    return base64.urlsafe_b64encode(compressed).decode("ascii")


def _validate_mermaid(source: str) -> Tuple[bool, str]:
    """Validate Mermaid by rendering. We catch HTTP errors as syntax errors."""
    try:
        _render_mermaid(source, "svg")
        return True, ""
    except Exception as e:
        return False, str(e)


def _render_mermaid(source: str, output_format: str) -> bytes:
    """Render Mermaid via Kroki public server."""
    fmt = "png" if output_format == "png" else "svg"
    encoded = _kroki_encode(source)
    url = f"https://kroki.io/mermaid/{fmt}/{encoded}"
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        # Kroki returns the error message as text on 4xx
        raise ValueError(
            f"Mermaid render failed ({response.status_code}): {response.text[:300]}"
        )
    return response.content



# ## PlantUML (public render server)

# PlantUML's text encoding alphabet (custom base64-like)
_PLANTUML_ENCODE_ALPHABET = (
    "0123456789ABCDEFGHIJKLMNOPQRSTUV"
    "WXYZabcdefghijklmnopqrstuvwxyz-_"
)


def _plantuml_encode(source: str) -> str:
    """Encode PlantUML source using PlantUML's deflate+custom-base64 scheme."""
    compressed = zlib.compress(source.encode("utf-8"))[2:-4]  # strip zlib header/checksum
    return _plantuml_b64(compressed)


def _plantuml_b64(data: bytes) -> str:
    """PlantUML's custom 6-bit-per-char encoding."""
    out = []
    i = 0
    n = len(data)
    while i < n:
        b1 = data[i]
        b2 = data[i + 1] if i + 1 < n else 0
        b3 = data[i + 2] if i + 2 < n else 0
        out.append(_PLANTUML_ENCODE_ALPHABET[b1 >> 2])
        out.append(_PLANTUML_ENCODE_ALPHABET[((b1 & 0x3) << 4) | (b2 >> 4)])
        out.append(_PLANTUML_ENCODE_ALPHABET[((b2 & 0xF) << 2) | (b3 >> 6)])
        out.append(_PLANTUML_ENCODE_ALPHABET[b3 & 0x3F])
        i += 3
    return "".join(out)


def _validate_plantuml(source: str) -> Tuple[bool, str]:
    """Validate PlantUML by rendering."""
    if "@startuml" not in source or "@enduml" not in source:
        return False, "PlantUML source must include @startuml and @enduml"
    try:
        _render_plantuml(source, "svg")
        return True, ""
    except Exception as e:
        return False, str(e)


def _render_plantuml(source: str, output_format: str) -> bytes:
    """Render PlantUML via public server."""
    fmt = "png" if output_format == "png" else "svg"
    encoded = _plantuml_encode(source)
    url = f"{config.PLANTUML_SERVER}/{fmt}/{encoded}"
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        raise ValueError(
            f"PlantUML render failed ({response.status_code}): {response.text[:300]}"
        )
    return response.content



# ## Public unified interface

def validate(source: str, format: str = "graphviz") -> Tuple[bool, str]:
    """Validate diagram source for the given format."""
    if format == "graphviz":
        return _validate_graphviz(source)
    if format == "mermaid":
        return _validate_mermaid(source)
    if format == "plantuml":
        return _validate_plantuml(source)
    return False, f"Unsupported format: {format}"


def render(
    source: str,
    format: str = "graphviz",
    output_format: Optional[str] = None,
    engine: Optional[str] = None,
) -> bytes:
    """Render diagram source to image bytes.

    `format` is the diagram language (graphviz, mermaid, plantuml).
    `output_format` is the image type (png, svg). Defaults to png.
    """
    out = output_format or "png"
    if format == "graphviz":
        return _render_graphviz(source, out, engine)
    if format == "mermaid":
        return _render_mermaid(source, out)
    if format == "plantuml":
        return _render_plantuml(source, out)
    raise ValueError(f"Unsupported format: {format}")


def render_to_svg_string(source: str, format: str = "graphviz") -> str:
    """Convenience: render and decode SVG bytes to a string."""
    return render(source, format=format, output_format="svg").decode("utf-8")


def render_to_file(
    source: str,
    filepath: str,
    format: str = "graphviz",
    output_format: Optional[str] = None,
) -> str:
    """Render and write to disk."""
    out = output_format or "png"
    image_bytes = render(source, format=format, output_format=out)
    with open(filepath, "wb") as f:
        f.write(image_bytes)
    return filepath

# Backwards-compatible wrappers

# The original tests and notebooks call `validate_dot`, `render_dot`, and
# `dot_to_svg_string`. Keep those names working.

def validate_dot(dot_source: str) -> Tuple[bool, str]:
    """Legacy alias — validates Graphviz DOT specifically."""
    return _validate_graphviz(dot_source)


def render_dot(
    dot_source: str,
    output_format: Optional[str] = None,
    engine: Optional[str] = None,
) -> bytes:
    """Legacy alias — renders Graphviz DOT specifically."""
    fmt = output_format or config.GRAPHVIZ_FORMAT
    return _render_graphviz(dot_source, fmt, engine)


def dot_to_svg_string(dot_source: str, engine: Optional[str] = None) -> str:
    """Legacy alias — renders DOT to SVG string."""
    eng = engine or config.GRAPHVIZ_ENGINE
    src = graphviz.Source(dot_source, engine=eng)
    return src.pipe(format="svg").decode("utf-8")
