# Analysis Standards

## What counts as a finding

A good finding includes:
- an observable pattern
- supporting evidence
- an explanation or plausible mechanism
- a clear boundary condition

Useful structure:

```text
Observation -> Interpretation -> Implication
```

Do not collapse these into one sentence when certainty is limited.

## Qualitative analysis standards

For substantial interview studies, use these standards together with [qualitative-deep-dive.md](qualitative-deep-dive.md). The deep-dive guide defines the required phases and artifacts.

### Coding

- Start broad, then tighten the code set as repeated themes emerge.
- Keep code names concrete and product-friendly.
- Maintain a codebook with definitions and example excerpts when the analysis is non-trivial.
- Track frequency carefully, but do not confuse frequency with importance.
- Do not code away the scene: preserve what the user was trying to do, what happened, and what made the moment matter.
- Use at least two coding passes for meaningful interview work. For deeper projects, use open coding followed by focused coding, and add theory coding only when it genuinely sharpens interpretation.

### Pattern development

- Build patterns around needs, motivations, workarounds, barriers, and decision strategies.
- Prefer behavioral archetypes over pure demographic buckets.
- Capture within-group variation, not just between-group differences.
- Include at least one counterexample for major patterns when available.
- Keep each major pattern grounded in lived situations, not only abstract categories.
- Build patterns from repeated coded evidence plus case comparison, not from one memorable respondent.

### Quote usage

For each important claim, include one or more quotes with source context such as:
- respondent ID
- segment or relevant profile
- source question or touchpoint

Avoid anonymous labels like "a user said" when traceability matters.
Prefer quotes that reveal the user's logic, emotion, or trade-off, not only short slogan-like lines.

### Scene reconstruction

When the data allows, reconstruct the user's situation in plain language:
- what they were trying to get done
- what step they were in
- what made the task feel easy, risky, frustrating, or worth doing
- what workaround or decision followed

This keeps the report vivid and prevents over-abstraction.

### Required qualitative assets for substantial studies

Unless the user explicitly wants a lightweight pass, substantial interview analysis should preserve:
- immersion memos
- codebook
- casebook or participant profiles
- quote bank
- contradiction / negative-case notes

## Quantitative analysis standards

### Metrics

- Define key metrics the first time they appear.
- Keep definitions stable across the document.
- Report `n=` for subgroup results.
- Flag where weights, filters, or exclusions were applied.

### Comparison

- Compare groups only when the grouping logic is meaningful.
- Prefer a small set of decision-relevant cuts over exhaustive slicing.
- When testing is unavailable, avoid overclaiming precision.

### Visualization

- Chart titles should state the takeaway, not just the variable names.
- Do not use charts when a simple table is clearer.
- Every chart should reconcile with the text and underlying numbers.

## Insight standards

An insight should do more than summarize.

Ask:
- Why does this happen?
- For whom is it most true?
- Under what conditions does it break?
- Why does it matter to the product or business?

If those questions cannot be answered, call it a finding or hypothesis, not an insight.

## Writing and tone standards

- Prefer specific nouns and verbs over abstract phrasing.
- Ban empty phrases such as `empower users`, `enhance experience`, `drive value`, `optimize journey`, or `strong demand` unless followed immediately by concrete evidence.
- Avoid black-box labels that flatten meaning, such as `pain point around trust`, when the real issue is more specific like `users hesitate to upload ID because they do not know who will see it or how long it is stored`.
- Keep conclusions crisp, but do not squeeze out the user's scene, motive, or wording.
- If a sentence could be said about almost any product, rewrite it.

## Evidence density standard

For major findings, try to include both:
- one concrete data point
- one concrete quote or scene fragment

This combination usually produces reports that are both credible and readable.

## Objectivity standards

- Present meaningful disconfirming evidence.
- Separate user account from analyst interpretation.
- Mark conjecture explicitly with language like `may`, `suggests`, or `likely`.
- Avoid advocacy disguised as research.

## Decision linkage

Every major finding should map to one of:
- product opportunity
- experience risk
- operational gap
- go-to-market implication
- measurement need

If it maps to none of these, reconsider whether it belongs in the main body.
