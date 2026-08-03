---
name: prompt.check_redundant_ideas
description: Check and merge redundant research ideas
model: haiku
--- 

# Goal
- Find and potentially merge research ideas in the directory `research/ideas/*.md`

# Workflow

## Read Research Ideas
- Read `research/ideas/README.md`
- Read the template for a research idea `research/ideas/template.research_idea.md`
- Read the research ideas under `research/ideas/*.md`

## Find Redundant Ideas
- Find the ideas that are redundant or highly overlapping
- Propose which ones could be merged

## Wait for User
- Wait for the user to confirm the plan

## Merge Ideas
- Merge research ideas using the template `research/ideas/template.research_idea.md`
