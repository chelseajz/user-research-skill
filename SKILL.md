---
name: user-research
description: Use when the user needs internet-company user research planning, qualitative coding, survey analysis, mixed-method synthesis, research report writing, research report review, or revision of someone else's report. Especially suitable for producing and auditing professional, rigorous, objective research reports with explicit evidence chains, confidence labels, limitations, and decision-ready recommendations.
---

# User Research

This skill turns broad "do research" requests into a disciplined workflow that protects evidence quality and report credibility.

Reference map:
- For a quick overview of the reference library, start with [references/README.md](references/README.md).

Use it for:
- Research planning for product, growth, monetization, retention, trust, service, or experience topics
- Qualitative analysis of interviews, tickets, feedback, chats, or call notes
- Survey analysis and mixed-method synthesis
- Writing or reviewing research reports for product, design, operations, strategy, or leadership
- Auditing and revising reports written by agencies, vendors, teammates, or other AI systems

Do not use it for:
- Pure market news lookups with no user data
- Fabricating research findings or overstating weak evidence
- Treating small qualitative samples as representative population estimates

## Core principles

- Be objective: separate observation, interpretation, and recommendation.
- Be traceable: every important claim should point to a metric, quote, or both.
- Be bounded: state what the data can and cannot support.
- Be decision-oriented: recommendations must connect to concrete product or business choices.
- Be anti-hallucination: if evidence is missing, say so plainly and lower confidence.
- Be denominator-disciplined: do not mix raw rows, deduped respondents, valid-question bases, and target-segment bases without naming each base explicitly.
- Be identifier-disciplined: do not mix interview ids, questionnaire ids, row ids, and linkage ids in reader-facing case labels.
- Be concrete in language: avoid inflated AI-style phrasing, empty abstractions, and generic business cliches.
- Keep researcher voice in the body: write as analysis, not as delivery management. Avoid meta narration about handoff, packaging, or "how to use this file" inside the research正文.
- Keep the user alive on the page: preserve real scenes, tensions, and phrasing instead of over-compressing everything into abstract labels.
- Prefer integrated reporting over siloed reporting: when quant and qual answer the same question, combine them into one finding rather than writing two parallel sections.
- Make leadership findings scannable: leadership-facing conclusions should usually resolve to one bounded takeaway line, one compact support table or chart, and a few bullets rather than dense explanatory prose.
- Make product-feedback findings granular: for demo or prototype feedback, explicitly separate issues such as funds destination, currency logic, repayment mechanism, pricing/rule clarity, and institutional backing when the data supports that level.
- Treat user-requested capabilities as signals first, not promises: if feasibility is unknown or constrained, frame the item as a discussion point, dependency, or unresolved product decision.
- Never leave drafting residue in the final report: placeholders such as "待补", "to fill", or internal drafting notes must be resolved or removed before the report is treated as final.
- Keep top-layer strategy language aligned with evidence strength: executive summaries, section titles, and action recommendations must not sound more certain than the body evidence allows.
- Do not duplicate the action layer: if a report contains both a narrative recommendation block and a priority table, give them different jobs or collapse them into one system.
- Embedded support objects are not enough on their own: when a chart, sheet, or appendix table carries critical proof, restate the key numbers and takeaway in the body so the report remains auditable without clicking away.
- If you use off-denominator or conflicting-mouth examples to illustrate a pattern, label them explicitly as supplementary evidence for hidden demand, wording mismatch, or mechanism explanation rather than as the core support set.

## Workflow selection

Choose the lightest path that fits the request:

### Quick mode menu

1. Planning only
   Best for: study design, hypotheses, sample plan, screener logic, discussion guide
   Read: [workflow.md](references/workflow.md) and [analysis-standards.md](references/analysis-standards.md)

2. Qualitative only
   Best for: interviews, transcripts, notes, feedback, tickets, open text
   Read: [workflow.md](references/workflow.md), [qualitative-deep-dive.md](references/qualitative-deep-dive.md), plus the qualitative sections in [analysis-standards.md](references/analysis-standards.md)

3. Quantitative only
   Best for: survey data, crosstabs, statistical tests, chartbooks
   Read: [workflow.md](references/workflow.md), [artifact-interface.md](references/artifact-interface.md), and the quantitative sections in [analysis-standards.md](references/analysis-standards.md)

4. Mixed methods
   Best for: linked or parallel qual + quant, triangulated reporting, one complete report for multiple stakeholders
   Read: all core reference files, [qualitative-deep-dive.md](references/qualitative-deep-dive.md), [mixed-method-integration.md](references/mixed-method-integration.md), [artifact-interface.md](references/artifact-interface.md), and the confidence standard

5. Report review
   Best for: auditing, critiquing, hardening, or rewriting a report
   Works as:
   - the final review stage inside a research project
   - a standalone mode to review a report written by a teammate, vendor, agency, or another AI system
   Read: [review-rubric.md](references/review-rubric.md) and [iteration-playbook.md](references/iteration-playbook.md)

6. Executive-ready reporting
   Best for: leadership audiences, cross-functional decision makers, one-page summaries, decision-ready framing
   Read: [executive-report-template.md](references/executive-report-template.md) and [evidence-confidence-standard.md](references/evidence-confidence-standard.md)

7. Research asset packaging
   Best for: reusable research artifacts, stronger traceability, multi-layer deliverables, handoff-ready packages
   Read: [finding-ledger-template.md](references/finding-ledger-template.md), [research-assets-template.md](references/research-assets-template.md), and [single-report-multistakeholder.md](references/single-report-multistakeholder.md)

8. Citation and rollback discipline
   Best for: substantial, multi-step, or heavily revised work
   Read: [citation-style.md](references/citation-style.md) and [rollback-rules.md](references/rollback-rules.md)

## Default operating procedure

1. Clarify the business decision and audience if missing and materially important.
2. Inventory available evidence:
   - raw data
   - processed tables
   - existing research outputs
   - source-of-truth definitions
3. Detect method type: qualitative, quantitative, or mixed.
4. State important assumptions before analysis when they may affect conclusions.
5. For quantitative work, lock the sample funnel before interpretation:
   - raw rows
   - invalid-row removal
   - stable respondent deduplication
   - target-population filter
   - question-valid base where relevant
6. Name each denominator explicitly and keep it stable across the package.
7. If older analyses or legacy reports exist, compare their sample funnel before reusing any number, chart, or conclusion.
8. Analyze with explicit evidence tracking.
9. Draft findings using confidence labels: `High`, `Medium`, or `Low`.
10. Produce a report using [report-standard.md](references/report-standard.md).
11. Red-team the report against [review-rubric.md](references/review-rubric.md) before presenting it as final.
12. If the report is weak, revise it using [iteration-playbook.md](references/iteration-playbook.md) and clearly separate factual fixes, inference fixes, and framing improvements.
13. When the report matters for leadership review, use [executive-report-template.md](references/executive-report-template.md) and [evidence-confidence-standard.md](references/evidence-confidence-standard.md), then run `scripts/validate_report.py` if a markdown file exists.
14. For substantial projects, maintain a finding ledger and reusable research assets so conclusions remain traceable after the report is finished.
15. For interview-heavy or open-text-heavy projects, do not jump straight from transcripts to report prose. Run the qualitative deep-dive workflow first and produce the required qualitative assets.
16. For mixed-method work, do not skip linkage and single-source analysis. Link data first when possible, complete qual and quant analysis separately, then integrate.
17. Prefer file-based handoffs between stages over conversational memory for substantial projects.
18. For executive-facing mixed-method deliverables, default to one complete report that combines core conclusions and detailed findings in the same document; use separate quant and qual files as supporting layers, not as the only readable output.
19. For chart-heavy work, enforce one chart system across the whole package: unified palette, consistent footnotes, subgroup sample sizes on cross charts, and human-readable chartbook labels.
20. For deep qualitative work, require pattern logic, decision logic, conversion drivers, product feedback analysis, and a case sampling explanation when a casebook is included.
21. For leadership-facing delivery packages, default to two synchronized top-layer outputs: one formal main report with full analysis support and one compressed meeting version for readout.
22. In the formal main report, front-load concise conclusions and decisions, then support them in the same document with detailed analysis, case summaries, quotes, and method boundaries.
23. When delivering in Feishu or another rich-doc format, do not leave raw markdown image syntax, broken local paths, or appendix-style chart dumps in the reader-facing document. Build the document in reading order and place charts next to the claim they support.
24. For Feishu or similar rich-doc output, prefer sequential construction: append the text for a section, then place the relevant chart immediately after the supporting claim. Avoid one-shot overwrite if it causes charts to collapse into the appendix or end of file.
25. Use the naming convention the business asked for. Formal main reports should keep the requested main title, and reference materials should use `参考-<topic>-<subtopic>` naming so the source-of-truth layer is obvious.
26. For quantitative support files that will be reused for charts or downstream analysis, separate absolute counts and percentages into different fields or columns, include navigation or index cues, and keep a quick-reading crosstab companion when stakeholders need direct table scanning.
27. For casebooks, make bucket names faithful to the actual inclusion logic. Do not label a section as `no need` if it mixes weak demand, edge cases, strong substitutes, or non-priority opportunities. Keep the "why selected" note consistent with the segment label and the quote content.
28. When qualitative quotes are linked back to survey data, use the interview/case id as the visible case number and use survey linkage fields only behind the scenes. Never let a questionnaire id leak into the polished `案例#...` label by mistake.
29. When one section combines raw multi-select usage counts with simplified mutually-exclusive usage recoding, explain the two systems explicitly or choose one system for the main report. Do not let readers infer that conflicting `N` values refer to the same cut.
30. When one segment label is statistically non-significant but directionally interesting, keep that caveat synchronized across the title, summary, recommendation block, and detailed body. Do not soften the caveat only in the appendix.
31. If a main report uses embedded Feishu sheets or support tables to justify a people strategy or priority call, include a compact in-body comparison table or numeric summary instead of leaving the proof only inside the embedded object.
32. If the report includes both a top recommendation callout and a recommendation table, separate them by layer:
   - the callout should contain only the few highest-level decisions
   - the table should contain execution priority, concrete action, and why now
   - do not restate the same action twice in different wording

## Interaction rules

- Do not force a questionnaire-style intake if the needed facts are already in the prompt or files.
- Ask only for missing information that changes research validity, such as sample origin, metric definition, or whether two datasets can be linked.
- If blocked by missing inputs, name the exact blocker and offer the smallest next step.
- Prefer making a reasonable assumption and labeling it over stalling.
- When reviewing a third-party report, default to reviewer mode: findings first, severity-ordered, with direct references to the weak claim, missing evidence, or methodological risk.
- For decision-critical deliverables, prefer reporting against an explicit template rather than inventing structure from scratch.
- When the user provides comments on a shared doc, treat the comment trail as revision input. Read comments, identify repeated issues, and iterate against the comment-driven backlog instead of relying only on the latest document snapshot.

## Evidence rules

- Never describe a pattern as universal without support.
- Never convert qualitative signals into population size estimates.
- When quantitative significance is unknown, do not imply certainty.
- When quotes are edited for clarity, say they were lightly edited without changing meaning.
- When samples are biased or narrow, surface that limitation near the affected conclusion, not only in an appendix.
- Use the confidence scale and claim taxonomy from [evidence-confidence-standard.md](references/evidence-confidence-standard.md).
- If a feature request appears frequently in interviews but product feasibility is unknown, report it as a validated user need or friction signal, then explicitly separate the product implication from the implementation commitment.

## Deliverable bar

A strong output from this skill should:
- answer the research question quickly
- preserve methodological honesty
- show the strongest supporting evidence
- include counter-signals or caveats
- lead to actionable product or business decisions
- survive adversarial review from a skeptical research lead
- sound like a strong human researcher, not a generic AI summary
- give the reader one clear main report to read, plus thicker appendices for auditability
- keep chart and table systems reusable without manual cleanup
- preserve enough user voice and scene detail that the report feels credible to practitioners
- survive copy into Feishu or similar document tools without exposing markdown residue, misplaced charts, or broken formatting artifacts
- survive format conversion into Feishu or similar tools without stray markdown artifacts, broken image placement, or support tables that need manual restructuring

If the task is substantial, consult the references below as needed:
- [workflow.md](references/workflow.md)
- [qualitative-deep-dive.md](references/qualitative-deep-dive.md)
- [mixed-method-integration.md](references/mixed-method-integration.md)
- [artifact-interface.md](references/artifact-interface.md)
- [analysis-standards.md](references/analysis-standards.md)
- [report-standard.md](references/report-standard.md)
- [review-rubric.md](references/review-rubric.md)
- [iteration-playbook.md](references/iteration-playbook.md)
- [executive-report-template.md](references/executive-report-template.md)
- [evidence-confidence-standard.md](references/evidence-confidence-standard.md)
- [citation-style.md](references/citation-style.md)
- [rollback-rules.md](references/rollback-rules.md)
- [single-report-multistakeholder.md](references/single-report-multistakeholder.md)
- [finding-ledger-template.md](references/finding-ledger-template.md)
- [research-assets-template.md](references/research-assets-template.md)
- `scripts/validate_report.py`
