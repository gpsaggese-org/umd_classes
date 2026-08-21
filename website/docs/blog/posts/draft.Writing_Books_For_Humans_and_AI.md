---
title: "How to Write Books for Humans and AI"
draft: true
authors:
  - gpsaggese
date: 2026-06-09
description: Guide on writing books optimized for both human readers and AI consumption
categories:
  - AI Research
  - Developer Tools
---

# How to Write Book and Technical Content for Humans (and AI)

- AI can answer any question with depth and proficiency
- AI can write a book on any topic you are interested in tailored to the level you
  are at (from ELI5 to PhD), with a tutor that can patiently answer questions,
  all of this instantaneously and (almost for free

- Why writing any technical content? What happens to the old concept of a "book"?

- Also how should a book be written for the era of limited attention and shortcuts
  (a "little known secret", "the 1 hr weird trick billionaires use")?

- Knowing "syntax" is useless, what matters is teaching judgement: when to apply
  a technique, what to do if the results are not what was expected, being able
  to critique, having a mental model of different approaches

- Add hard-won lessons learned on the field, AI optimizes for "consensus" and
average, while what's often interesting are edge cases and non-linear path to
  success

- Lots of content that were fundamental until few years ago (e.g., linear algebra,
  deriving backprop from scratch) are now useless or detrimental, since this
  is the kind of standard content that one can get from AI

- Embrace AI by sharing prompts and automation that can make the work easier

- Optimize for human learning
  - For humans visual structure and active recall
  - Organize information in a hierarchical, bullet-point format

- Avoid (actually abhorr) anything that is or resembles AI slop

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
