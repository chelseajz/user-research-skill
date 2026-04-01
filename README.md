# user-research-skill

`user-research` is a reusable research skill for turning messy product questions, interview data, survey outputs, and draft reports into decision-ready user research deliverables.

It is built for teams that want research outputs to be:
- evidence-based
- methodologically honest
- easy for leadership to scan
- detailed enough for practitioners to act on
- resilient under skeptical review

## What It Does

This skill helps with the full user research workflow:
- research planning and study design
- qualitative coding and synthesis
- survey and crosstab analysis
- mixed-method integration
- research report writing
- executive-ready summarization
- rigorous review and hardening of draft reports

It is especially useful when a team needs to move from:
- scattered interviews to a structured insight system
- fragmented quant and qual outputs to one coherent report
- “interesting observations” to decisions with explicit evidence and confidence
- weak or overclaimed draft reports to stronger, more defensible versions

## What Makes It Different

Compared with lightweight “summarize these notes” prompts, this skill emphasizes:
- denominator discipline
- evidence traceability
- confidence labeling
- sharp separation between observation, interpretation, and recommendation
- realistic handling of research limitations
- better alignment between executive summaries, section titles, body evidence, and action recommendations

It also includes guardrails for common report quality failures such as:
- overstating weak evidence
- mixing incompatible bases or respondent IDs
- burying proof inside appendices or embedded tables
- duplicating recommendation layers
- treating prototype feedback as product validation
- leaving drafting residue in a “final” report

## Best Use Cases

This repository is a strong fit for:
- product researchers
- PMs and designers doing mixed-method synthesis
- strategy and operations teams writing internal user insight reports
- AI-assisted research workflows that need stronger structure and review discipline

Typical scenarios:
- “Review this report and tell me what is overclaimed.”
- “Turn these interviews and crosstabs into one polished report.”
- “Help me write an executive-ready user research document.”
- “Audit this agency report before I send it upward.”
- “Make this demo feedback section more actionable and less repetitive.”

## Repository Structure

- [`SKILL.md`](./SKILL.md): main skill instructions and operating rules
- [`references/README.md`](./references/README.md): reference map
- [`references/`](./references): workflow, standards, templates, and review rubrics
- [`scripts/validate_report.py`](./scripts/validate_report.py): report validation helper
- [`generate_research_outputs.py`](./generate_research_outputs.py): generation helper used in this workflow

## Branches

- `codex`: Codex-oriented version of the skill
- `claude`: branch reserved for the Claude-oriented variant
- `main`: shared baseline / repository default

## Design Philosophy

The skill is opinionated about research quality:
- one report should usually be readable by leaders and usable by practitioners
- strong reports should survive format conversion, not just look good in markdown
- research recommendations should be decision-ready, not generic
- product feedback should be structured into concrete friction types
- qualitative quotes should preserve user voice instead of being flattened into abstractions

In short, this repository is meant to help produce research outputs that feel like they were written by a strong human researcher, not a generic AI summarizer.

## Getting Started

1. Start with [`SKILL.md`](./SKILL.md).
2. Use [`references/README.md`](./references/README.md) to navigate the supporting materials.
3. If you are reviewing a report, go first to the review workflow and rubric.
4. If you are creating a new report, use the workflow, standards, and report template together.

## Status

This repository is actively evolving through real report review and revision work. The current updates include stronger guidance on:
- keeping top-layer strategy language aligned with evidence strength
- separating recommendation layers cleanly
- restating key proof in the body instead of hiding it in embeds
- labeling supplementary examples when they are off-denominator
- keeping summary, title, and body caveats synchronized
