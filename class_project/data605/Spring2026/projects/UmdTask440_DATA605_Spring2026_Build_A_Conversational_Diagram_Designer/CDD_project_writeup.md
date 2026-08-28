# Conversational Diagram Designer (CDD)

## What this project is

CDD takes a plain English description and turns it into a rendered technical diagram, then checks its own work before showing it to you. You type something like "class diagram for an e-commerce app" or "state machine for an order lifecycle," and the system picks one of three diagram formats, writes the source code for it, and renders it as an image. Then a multimodal model looks at that rendered image and judges whether it actually matches what was asked for. If it doesn't, the code gets rewritten and the process repeats, up to three times.

That last part is what I actually care about here. Most text-to-diagram tools write code blindly, the model never sees the picture it just produced. So if two boxes end up overlapping or an edge is missing, nothing catches it. I wanted the model to look at its own output the way a person would, and correct it if it's wrong.

The project started as a DATA605 deliverable and I'm continuing it now as a research project, on the `UmdTask537_Review_students_research_projects` branch, under `UmdTask440_DATA605_Spring2026_Build_A_Conversational_Diagram_Designer`.

## How a request actually flows through the system

1. You describe a diagram in plain English.
2. The system picks a format (Graphviz DOT, Mermaid, or PlantUML) and asks the LLM to write valid source code for it.
3. The renderer turns that code into a PNG.
4. If the code has a syntax error, there's one repair pass before moving on.
5. With vision feedback on (the default), the rendered image and the original request go back to the model together, and it returns a structured critique: is this acceptable, what's wrong, what should change.
6. If the critique flags real problems and we're still under the cap of three iterations, the diagram gets regenerated with that critique folded into the next prompt.
7. Once it stops, either because the diagram was accepted or the cap was hit, you get the final diagram, the source code behind it, and a trace of everything that happened along the way.

## Seeing it work

I asked for "an order lifecycle state machine with draft, submitted, approved, shipped, cancelled states," and it produced a clean Graphviz diagram on the first pass, along with a description and a few suggested next transitions:

![CDD after generating an order lifecycle state machine, showing the diagram, description, and suggestions panel](https://github.com/user-attachments/assets/0dc6736b-142f-4425-b153-979be4f8f8ce)

I then asked it to add a "Discard Draft" transition from Draft to Cancelled, which moved things into a second revision. The history panel keeps every version, so clicking back into revision 1 shows exactly how it looked before that edit, next to the current one:

![Revision history comparing rev 1 and rev 2 side by side](https://github.com/user-attachments/assets/9cb6e475-ab18-4ba7-96c7-6333de29865a)

## What's still rough

That same edit gave me a real example of a problem I've been thinking about: telling elegant diagrams from messy ones. The follow-up request happened to switch the renderer to Mermaid, and the output got noticeably harder to read, edge labels overlapping nodes, layout feeling cramped compared to the clean Graphviz version above.

![The same diagram re-rendered in Mermaid after a follow-up edit, with overlapping labels](https://github.com/user-attachments/assets/f8446a80-6053-4469-baca-4ced34c5913d)

It's a good example of the diagram being technically correct, every node and edge that was asked for is there, while still looking messy, and right now nothing in the pipeline actually evaluates for that. That feels like a natural thing to fold into the vision critique step alongside correctness.

The other thing I haven't nailed down yet is generation temperature. It's not fixed, so the same prompt can give different output across runs, which makes it harder to tell whether a change actually helped or I'm just looking at noise.

## What each file does

- **cdd_config.py**: all the settings, LLM provider, format definitions, system prompts, and the vision feedback config (on by default, capped at three iterations).
- **cdd_llm.py**: the unified client for both text and multimodal calls. Gemini 2.5 Flash is the main provider, with OpenAI and Anthropic as fallbacks.
- **cdd_renderer.py**: one entry point for all three formats, validates the generated code and turns it into an image. Graphviz renders locally, Mermaid goes through Kroki, PlantUML goes through the public PlantUML server.
- **cdd_orchestrator.py**: the core of the project. A state machine that drives one full turn, generate, render, critique, regenerate if needed, with every step logged into a trace so I can see exactly what happened and why.
- **cdd_server.py**: the FastAPI backend that serves the React frontend and the API it talks to.
- **cdd_eval.py**: the evaluation harness. Runs the same prompts with vision on and off and compares them on syntax validity, render success, and structural correctness, with an optional LLM-as-judge step for semantic correctness and visual quality.
- **frontend/**: a single React component built with Vite. No extra framework, no state library, kept simple on purpose.
- **test/**: the pytest suite, 46 passing tests, two integration tests skipped by default since they need external render servers.

## Where things stand

The core loop works end to end, and the correction pass is doing real work, not just decorative, it catches actual issues like missing edges or mismatched intent and produces a visibly better diagram on the next pass. All three diagram formats are working, not stubbed. The test suite is solid, and the eval harness gives me a real way to compare vision-on against vision-off instead of just eyeballing it.

Beyond the temperature and messy-diagram questions above, I also don't have a good way yet to unit test or benchmark the LLM loop itself beyond what the eval harness already compares in aggregate, so a bad prompt change is hard to catch quickly. All three of these are next on my list.

## What's next

Two things came directly out of feedback I got on this: leaving the temperature as something the user can set, rather than hardcoding it, and building an actual test/benchmark layer for the LLM loop, since right now I have no clean way to catch a bad prompt change before it ships, which was flagged as a real, still-unsolved problem worth tackling here.
