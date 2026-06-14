# LLM Collaborative Editor

## Description

- Design a new editor paradigm where humans and LLMs co-edit documents, code, and
  notebooks in real time, similar to Google Docs but with an LLM as an active
  collaborator
- Build autoreload mechanisms so the LLM can see live changes to the
  document/code and re-evaluate its suggestions without requiring manual
  re-prompting
- Explore Jupyter-like cell-based editing where each cell can be authored by the
  human, the LLM, or interactively negotiated between both
- Research optimal UI patterns for showing LLM-suggested edits alongside human
  edits: inline diffs, side-by-side views, or annotation layers
- Investigate latency and context-management strategies so the LLM maintains
  coherent state across long editing sessions without losing earlier context
- Study how streaming LLM output can be integrated into incremental document
  edits rather than replacing full blocks

## Project Objective

The goal is to build a next-generation collaborative editor where the LLM is a
first-class co-author: it tracks document state via autoreload, proposes
incremental edits, and responds to human edits in near-real time — enabling a
tighter human–machine editing loop than current tools like Cursor or Copilot
provide.

## Dataset Suggestions

1. **GitHub Copilot Interaction Logs (Synthetic)**
   - Source: Reproduce via VS Code extension telemetry studies
   - Content: Accept/reject rates for inline suggestions, edit distances between suggestion and final code
   - Access: Academic papers on Copilot usage patterns (e.g., arXiv studies on code completion)

2. **Jupyter Notebook Revision History**
   - Source: nbgit or Jupyter notebook checkpoints
   - Content: Sequential cell edits, execution order, outputs — useful for modeling the human editing loop
   - Access: Public GitHub notebooks (GitHub Search API with `.ipynb` filter)

3. **Google Docs Collaborative Editing Dataset**
   - Source: Academic studies on collaborative writing (e.g., WikiDrafts, CoEdIT dataset)
   - Content: Multi-author revision sequences with timestamps
   - Access: CoEdIT dataset on HuggingFace (`grammarly/coedit`)

## Related Work

- Cursor IDE: LLM-integrated editor but not true co-editing (human drives, LLM responds)
- GitHub Copilot: inline completion, no document-level state tracking
- CoEdIT (Raheja et al., 2023): instruction-based text editing model
- GPT-4 Code Interpreter: LLM executes code but doesn't co-edit the notebook live

## Open Questions

- How do you resolve conflicts between human and LLM edits in real time?
- What is the right granularity for autoreload — per keystroke, per cell, per save?
- How should the LLM handle retracting a suggestion the human partially accepted?
