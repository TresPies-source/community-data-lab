# Community Data Lab

This is the open-source repository for Community Data Lab — an AI-assisted spatial equity research methodology, curriculum, and toolkit for community development organizations.

## Project Context

- **Owner:** Cruz Morales, TresPies
- **Proof-of-concept:** Commonwealth Development (CWD), Madison, WI
- **First target partners:** The Resurrection Project (Chicago), Mercy Housing (national)
- **Brand split:** "Community Data Lab" = open-source. "CDC Research Accelerator" = hired engagements.

## Architecture

- **Methodology:** AI-agnostic research workflow, Claude Code recommended
- **Curriculum:** 6-week cohort, virtual, async practice with live sessions
- **Starter kit:** Stdlib Python only (no pandas/numpy), portable HTML outputs
- **Prompt library:** Claude Code templates, adaptable to other AI tools

## Key Decisions

- All methodology and curriculum content is open source (MIT)
- Premium components live in CDC Research Accelerator engagements, not in this repo
- English-only for now; flag for Spanish localization when a bilingual engagement lands
- Research questions drive outputs — every metric answers a specific equity question
- Standalone, portable outputs (single HTML files, no server dependencies)

## File Organization

- `curriculum/` — 6-week cohort materials (lesson plans, exercises, assessments)
- `methodology/` — The TresPies research workflow documentation
- `prompt-library/` — AI prompt templates organized by research stage
- `starter-kit/` — Parameterized Python scripts and HTML viewer templates
- `case-studies/` — Partner city analyses and lessons learned
- `templates/` — Policy brief, viewer, and workbook templates

## When Working in This Repo

- State what something IS directly. Do not use "not merely" / "not just" constructions.
- All code must be stdlib Python (no external ML/data dependencies)
- All outputs must be self-contained and portable (no server requirements)
- Research questions must be specific and answerable with public data
- Every data source must be documented with URL, refresh schedule, and known limitations
