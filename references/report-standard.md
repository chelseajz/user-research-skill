# Report Standard

## Default structure

Use this structure unless the user asks for another format:

1. Background and objective
2. Method and sample
3. Executive findings
4. Detailed analysis
5. Recommended actions
6. Limitations and open questions
7. Appendix

For mixed-method work, also use [mixed-method-integration.md](mixed-method-integration.md).
For substantial multi-step work, keep outputs aligned with [artifact-interface.md](artifact-interface.md).
Use consistent references from [citation-style.md](citation-style.md).

## Section requirements

For one-report workflows serving multiple roles, also use [single-report-multistakeholder.md](single-report-multistakeholder.md).

### 1. Background and objective

Include:
- why this research was conducted
- the decision it supports
- the research questions

### 2. Method and sample

Include:
- data source description
- collection window
- sample size and important segment definitions
- cleaning, deduplication, or linkage notes
- limitations that affect interpretation

If the study is mixed-method, explicitly state:
- whether data sources were linked
- what the match rate was
- whether the interview sample differs from the survey base

### 3. Executive findings

Include 3-7 findings. Each should have:
- a one-sentence takeaway
- supporting evidence in brief
- confidence label
- plain language that a non-research stakeholder can understand on first read

Suggested format:

```markdown
**Finding:** [one-sentence conclusion]
Evidence: [metric, quote, or both]
Confidence: High | Medium | Low
Why it matters: [decision relevance]
```

Preferred format when space allows:

```markdown
**Finding:** [clear bounded conclusion]
What we saw: [specific metric, subgroup, or behavioral pattern]
User reality: [short quote or scene]
Confidence: High | Medium | Low
Why it matters: [decision relevance]
```

### 4. Detailed analysis

For each key theme:
- present evidence
- explain interpretation
- note meaningful variation or exceptions
- tie back to the business context
- include enough user context that readers can picture the situation, not just memorize a label

For mixed-method findings, make clear whether the relationship is:
- agreement
- tension
- complementarity

### 5. Recommended actions

Recommendations must be:
- specific
- attributable to findings
- realistic to execute
- measurable where possible

Suggested fields:
- priority
- action
- supported by finding(s)
- expected impact
- risk or dependency

Also state who most needs to act on the recommendation:
- leadership
- product
- design
- operations

### 6. Limitations and open questions

Always include:
- sample and method limitations
- places where evidence is directional only
- what requires follow-up validation

### 7. Appendix

May include:
- codebook
- cross-tabs
- extra charts
- respondent profiles
- glossary and metric definitions
- finding ledger
- segment cards
- quote bank
- decision log
- linkage note
- integration memo
- proposition list

## Writing bar

- Lead with the answer, not the process.
- Use precise language and concrete numbers.
- Avoid inflated certainty.
- Keep the tone neutral and professional.
- Make it easy for a busy stakeholder to scan.
- Avoid AI-sounding filler, management cliches, and vague intensifiers.
- Use short, direct sentences for conclusions.
- For important findings, pair summary language with supporting data and at least one vivid user quote or scene.
- Do not over-compress the report so much that users stop sounding like real people.

## Anti-generic writing test

Rewrite a passage if any of these are true:
- it could describe almost any app or service
- it names a `pain point` but not the concrete moment causing it
- it says users `need trust`, `want convenience`, or `seek efficiency` without showing how that appeared in the data
- it recommends `optimize`, `strengthen`, or `improve` without naming the object and expected effect

## Leadership-ready additions

When the audience includes executives, also include:
- one page of decision-ready summary before the body
- a short list of decisions enabled by this research
- the top risks of misreading the data
- a note on what should happen now versus what needs more validation

For that format, use [executive-report-template.md](executive-report-template.md).
