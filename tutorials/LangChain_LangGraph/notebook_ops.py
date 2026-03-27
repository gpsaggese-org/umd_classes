# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## Notebook ops: nbformat + nbclient + artifacts + papermill
#
# Notebooks are just JSON documents.
# That means you can:
# - generate them (`nbformat`)
# - execute them programmatically (`nbclient`)
# - collect outputs and errors
# - parameterize runs (`papermill`)
#
# Why include this in a LangChain/LangGraph tutorial?
# Because “agents that write and run notebooks” is a surprisingly practical workflow for data work.
# We’ll keep the demos safe: everything writes under `tmp_runs/`.

# %%
from pathlib import Path

import nbformat
import nbclient

run_dir = Path("tmp_runs").resolve()
run_dir.mkdir(parents=True, exist_ok=True)

nb = nbformat.v4.new_notebook()
nb.cells = [
    nbformat.v4.new_markdown_cell("# nbclient smoke test"),
    nbformat.v4.new_code_cell("x = 2 + 3\nprint(x)"),
    nbformat.v4.new_code_cell("import math\nprint(math.sqrt(81))"),
]
nbformat.validate(nb)

in_path = run_dir / "smoke_in.ipynb"
out_path = run_dir / "smoke_out.ipynb"
nbformat.write(nb, str(in_path))

nb2 = nbformat.read(str(in_path), as_version=4)
client = nbclient.NotebookClient(
    nb2, resources={"metadata": {"path": str(run_dir)}}, timeout=60
)
client.execute()
nbformat.write(nb2, str(out_path))

str(out_path)


# %% [markdown]
# ### Write a notebook via a tool (from a spec)
#
# We’ll build a tiny notebook in memory (a title + a code cell), then write it to disk.
#
# This is the first building block for “notebook automation” — generating a notebook artifact from a structured spec.

# %%
# write_notebook is defined in langchain.API_utils.
spec = {
    "cells": [
        {"type": "markdown", "source": "# Tool-written notebook"},
        {"type": "code", "source": "print('ok')"},
    ]
}
ut.write_notebook.invoke({"spec": spec, "out_rel": "demo/tool_hello.ipynb"})


# %% [markdown]
# ### Notebook ops as tools + secure injected workspace (ToolNode)
#
# Here we treat notebook operations as **tools** inside a LangGraph workflow.
#
# The important idea:
# - tools can be powerful (file access, execution)
# - so we often want a *controlled* workspace root
#
# You’ll see us use an injected workspace directory so the graph can safely read/write only where we intend.

# %%
from pathlib import Path

import langchain_core.messages
import langgraph.graph
import langgraph.prebuilt

# Create workspace directory for notebook tool operations.
workspace = Path("tmp_runs/ipynb_tools_workspace").resolve()
workspace.mkdir(parents=True, exist_ok=True)

# Assemble ToolNode with all notebook operation tools from utils.
tool_node = langgraph.prebuilt.ToolNode(
    [
        ut.nb_write,
        ut.nb_run,
        ut.nb_extract_errors,
        ut.nb_extract_artifacts,
        ut.nb_list_files,
    ]
)

# Build a simple StateGraph with one tool execution node.
g = langgraph.graph.StateGraph(ut.ToolGraphState)
g.add_node("tools", tool_node)
g.add_edge(langgraph.graph.START, "tools")
g.add_edge("tools", langgraph.graph.END)
graph = g.compile()

print(f"Graph compiled with workspace: {workspace}")


# %%
# Define the notebook spec: a simple markdown cell and code cell.
spec = {
    "cells": [
        {"type": "markdown", "source": "# Tool-made notebook"},
        {"type": "code", "source": "print('hello')"},
    ]
}

# Invoke the tool to write the notebook to disk.
out1 = graph.invoke(
    {
        "workspace_dir": str(workspace),
        "messages": [
            langchain_core.messages.AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "nb_write",
                        "args": {"spec": spec, "out_rel": "demo/in.ipynb"},
                        "id": "t1",
                        "type": "tool_call",
                    },
                ],
            )
        ],
    }
)

print("Notebook written:")
print(out1["messages"][-1].content)

# %%
# Execute the written notebook and capture the executed version.
out2 = graph.invoke(
    {
        "workspace_dir": str(workspace),
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "nb_run",
                        "args": {
                            "in_rel": "demo/in.ipynb",
                            "out_rel": "demo/out.executed.ipynb",
                            "timeout_s": 60,
                        },
                        "id": "t2",
                        "type": "tool_call",
                    },
                ],
            )
        ],
    }
)

print("Notebook executed:")
print(out2["messages"][-1].content)

# %%
# List all files created in the workspace to show what the tools produced.
out3 = graph.invoke(
    {
        "workspace_dir": str(workspace),
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "nb_list_files",
                        "args": {},
                        "id": "t3",
                        "type": "tool_call",
                    },
                ],
            )
        ],
    }
)

# Display summary of tool results.
print("Files in workspace:")
print(out3["messages"][-1].content[:400])

# %% [markdown]
# ### Execute notebooks + collect errors
#
# We’ll execute a notebook programmatically and capture:
# - stdout
# - execution errors (if any)
#
# This is a friendly way to build “run this notebook and report back” pipelines.

# %%
from pathlib import Path

import nbformat

# Create directory for notebook execution test.
run_dir = Path("tmp_runs/execute").resolve()
run_dir.mkdir(parents=True, exist_ok=True)

# Build a notebook that intentionally errors to demonstrate error handling.
nb_err = nbformat.v4.new_notebook()
nb_err.cells = [
    nbformat.v4.new_markdown_cell("# Intentional error"),
    nbformat.v4.new_code_cell("print('before')"),
    nbformat.v4.new_code_cell("1/0"),
    nbformat.v4.new_code_cell("print('after')"),
]
nbformat.validate(nb_err)

# Write notebook to disk.
in_path = run_dir / "error_in.ipynb"
nbformat.write(nb_err, str(in_path))

print(f"Notebook with error saved to {in_path}")


# %%
import nbclient

# Execute the error notebook with error tolerance enabled.
out_path = run_dir / "error_out.executed.ipynb"
nb = nbformat.read(str(in_path), as_version=4)
client = nbclient.NotebookClient(
    nb,
    timeout=60,
    allow_errors=True,
    resources={"metadata": {"path": str(run_dir)}},
)
client.execute()
nbformat.write(nb, str(out_path))

print(f"Executed notebook saved to {out_path}")

# Extract and display errors from the executed notebook.
errors = ut.extract_errors(nb)
print(f"\nExtracted {len(errors)} errors:")
for err in errors:
    print(f"  - {err}")

# %% [markdown]
# ### Extract artifacts from executed notebooks (stdout + inline images)
#
# Executed notebooks can contain rich outputs (plots, tables, HTML).
#
# We’ll show a simple approach to pull a couple useful artifacts out of the executed notebook:
# - printed output
# - embedded images

# %%
from pathlib import Path

import nbformat

# Create notebook with code that produces stdout and inline plot output.
run_dir = Path("tmp_runs/artifacts").resolve()
run_dir.mkdir(parents=True, exist_ok=True)

nb = nbformat.v4.new_notebook()
nb.cells = [
    nbformat.v4.new_markdown_cell("# Artifact notebook"),
    nbformat.v4.new_code_cell("print('hello from stdout')"),
    nbformat.v4.new_code_cell(
        "import matplotlib.pyplot as plt\n"
        "plt.plot([0,1,2],[0,1,4])\n"
        "plt.title('inline')\n"
        "plt.show()\n"
    ),
]

# Write and execute the notebook to generate outputs.
in_nb = run_dir / "artifacts_in.ipynb"
executed_nb = run_dir / "artifacts.executed.ipynb"
nbformat.write(nb, str(in_nb))

import nbclient

nb2 = nbformat.read(str(in_nb), as_version=4)
nbclient.NotebookClient(
    nb2, timeout=120, resources={"metadata": {"path": str(run_dir)}}
).execute()
nbformat.write(nb2, str(executed_nb))

print(f"Executed notebook: {executed_nb}")


# %%
import base64
import json

# Extract all output artifacts (stdout, images, text results) from executed notebook.
out_dir = run_dir / "out"
out_dir.mkdir(parents=True, exist_ok=True)
manifest = []

# Iterate over code cells and their outputs to extract artifacts.
for i, cell in enumerate(nb2.cells):
    if cell.get("cell_type") != "code":
        continue
    for j, out in enumerate(cell.get("outputs", [])):
        # Extract stdout/stderr streams.
        if out.get("output_type") == "stream":
            txt = out.get("text", "")
            p = out_dir / f"cell_{i}_stream_{j}.txt"
            p.write_text(txt if isinstance(txt, str) else "".join(txt))
            manifest.append({"cell": i, "kind": "stream", "path": str(p)})
        # Extract display and execution result data (text, images, etc).
        if out.get("output_type") in ("display_data", "execute_result"):
            data = out.get("data", {})
            # Extract plain text representation.
            if "text/plain" in data:
                t = data["text/plain"]
                p = out_dir / f"cell_{i}_text_{j}.txt"
                p.write_text(t if isinstance(t, str) else "".join(t))
                manifest.append(
                    {"cell": i, "kind": "text/plain", "path": str(p)}
                )
            # Extract embedded PNG images.
            if "image/png" in data:
                b64 = data["image/png"]
                b = base64.b64decode(
                    b64 if isinstance(b64, str) else "".join(b64)
                )
                p = out_dir / f"cell_{i}_img_{j}.png"
                p.write_bytes(b)
                manifest.append({"cell": i, "kind": "image/png", "path": str(p)})

print(f"Extracted {len(manifest)} artifacts from {len(nb2.cells)} cells")

# %%
# Write manifest JSON file cataloging all extracted artifacts.
(out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

# Display summary of artifact extraction results.
result = {
    "executed_nb": str(executed_nb),
    "n_artifacts": len(manifest),
    "manifest": str(out_dir / "manifest.json"),
}
print(f"Artifact summary: {len(manifest)} items extracted")
print(f"Manifest written to: {out_dir / 'manifest.json'}")

# %% [markdown]
# ### Filesystem artifacts (notebooks that write files)
#
# Sometimes notebooks produce *real files* (CSVs, images, model outputs).
#
# In the next cell we execute a notebook that writes files into a run directory, then list what it produced.
# Everything stays under `tmp_runs/`.

# %%
# Create a notebook that generates file outputs (CSV and PNG).
run_dir = Path("tmp_runs/writes_files").resolve()
run_dir.mkdir(parents=True, exist_ok=True)

nb = nbformat.v4.new_notebook()
nb.cells = [
    nbformat.v4.new_markdown_cell("# Writes files"),
    nbformat.v4.new_code_cell(
        "import csv\n"
        "import matplotlib.pyplot as plt\n"
        "\n"
        "rows = [(i, i*i) for i in range(5)]\n"
        "with open('table.csv', 'w', newline='') as f:\n"
        "    w = csv.writer(f)\n"
        "    w.writerow(['x','y'])\n"
        "    w.writerows(rows)\n"
        "\n"
        "xs = [r[0] for r in rows]\n"
        "ys = [r[1] for r in rows]\n"
        "plt.plot(xs, ys)\n"
        "plt.title('y=x^2')\n"
        "plt.savefig('plot.png', dpi=120)\n"
        "print('wrote table.csv and plot.png')\n"
    ),
]

in_nb = run_dir / "writes_files.ipynb"
nbformat.write(nb, str(in_nb))

print(f"Notebook created at {in_nb}")


# %%
# Execute the notebook to generate file outputs.
out_nb = run_dir / "writes_files.executed.ipynb"
nb2 = nbformat.read(str(in_nb), as_version=4)
NotebookClient(
    nb2, timeout=120, resources={"metadata": {"path": str(run_dir)}}
).execute()
nbformat.write(nb2, str(out_nb))

# List all files produced by the notebook execution.
files = sorted([p.name for p in run_dir.iterdir() if p.is_file()])
print(f"Executed notebook, generated files: {files}")

# %% [markdown]
# ### Parameterized runs (Papermill)
#
# Papermill is a simple way to run the *same* notebook with different parameters.
#
# This is useful for:
# - experiments
# - scheduled reports
# - batch runs over multiple inputs
#
# We’ll do a tiny demo so you can see the mechanics.

# %%
# Create a notebook with a parameters cell for Papermill execution.
run_dir = Path("tmp_runs/papermill").resolve()
run_dir.mkdir(parents=True, exist_ok=True)

nb = nbformat.v4.new_notebook()
nb.cells = [
    nbformat.v4.new_markdown_cell("# Papermill demo"),
    # Tag this cell as "parameters" so Papermill can inject values.
    nbformat.v4.new_code_cell(
        "# Parameters\nx = 1\ny = 2", metadata={"tags": ["parameters"]}
    ),
    nbformat.v4.new_code_cell("print({'x': x, 'y': y, 'x_plus_y': x + y})"),
]
nb.metadata["kernelspec"] = {
    "name": "python3",
    "display_name": "Python 3",
    "language": "python",
}

in_nb = run_dir / "pm_in.ipynb"
nbformat.write(nb, str(in_nb))

print(f"Parametrized notebook created at {in_nb}")

# %%
import papermill as pm

# Execute the notebook with parameter injection: x=10, y=32.
out_nb = run_dir / "pm_out.ipynb"
pm.execute_notebook(
    str(in_nb),
    str(out_nb),
    parameters={"x": 10, "y": 32},
    cwd=str(run_dir),
    kernel_name="python3",
)

print(f"Papermill execution complete: {out_nb}")
