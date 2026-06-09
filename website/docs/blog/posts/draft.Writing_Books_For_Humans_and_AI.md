---
title: "How to Write Books for Humans and AI"
draft: true
authors:
  - gpsaggese
date: 2026-06-09
description: Guide on writing books optimized for both human readers and AI consumption
categories:
  - Writing
  - AI Tools
---

# How to write books for humans and AI

- Writing a textbook optimized for learning using notes means prioritizing
  clarity, brevity
  - For humans visual structure and active recall
- Organize information in a hierarchical, bullet-point format
  - Starting with the main topic, then indenting subtopics and details underneath

## Pedagogical Progression
- **Start with motivation**: Explain why the topic matters before diving into
  details
- **Intuition before formalism**: Explain the concept intuitively, then provide
  mathematical formalism
- **Build incrementally**: Progress from simple to complex, referencing earlier
  concepts
- **Use multiple representations**: Combine text, equations, diagrams, and
  real-world examples
- **Concrete examples**: Always include practical examples labeled
- **Reference context**: Connect new concepts to previously introduced material

## Engagement Strategies
- **Open with motivation**: "Why does this matter?"
- **Use questions**: Mark rhetorical questions with `**Question**:`
- **Ground in examples**: Always include `**Example**:` with concrete scenarios
- **Reference prior knowledge**: "As we saw in [previous topic]..."
- **Contrast approaches**: Show what doesn't work vs what does

- Think of it as a hybrid between a textbook and a student’s notebook

- Structure Everything Around Questions
  - Begin each section with a key question the content aims to answer
  - "Why does this matter?"

- Bullet Everything Possible
  - Use nested bullet points to show hierarchy of concepts
  - Keep each bullet to 1 idea
  - Group bullets under clear headings.
    ```
    ### Causes of X:
    - Environmental
      - Pollution
      - Resource scarcity
    - Economic
      - Inflation
      - Market failures
    ```

- Chunking: One Section = One Concept
  - Use 1 idea per page/section
  - Use boxed summaries, figures, or formulas

- Use Note-Like Formatting
  * Checklists for processes
  * Questions for reflection
  * Insights and mnemonics
  * Recap points or links to earlier topics

- Write Like You’re Explaining to Yourself

  - Avoid long prose.
  - Use first-person note voice:
     “Key thing to remember: entropy increases.”
  - Prefer plain language over academic jargon

- Use Diagrams Over Text
  - Summarize systems or relationships in graphviz, mermaid, or tikz style charts.
  - Add annotation arrows and layered explanations.

- Mark core ideas with tags such as

- Recommended Layout Conventions

| Element | Format Example |
| :---- | :---- |
| Section headers | \#\# Concept Name |
| Sub-concepts | \#\#\# Why it matters |
| Definitions | \*\*Term:\*\* definition |
| Equations | Displayed in LaTeX with context |
| Diagrams | Centered with labels |
| Summaries | Boxed bullets with takeaways |

- Structure as a math book
  - Definition, theorem, claim

// See .claude/skills/slides.rules.md
// [https://developers.google.com/style/highlights](https://developers.google.com/style/highlights)
