# Workflow

## 1. Start from the decision

Before analyzing, identify:
- the business question
- the decision this work should inform
- the audience
- the time horizon

If the user asks for "a report" without a decision context, default to:
- Audience: product, design, ops, and leadership
- Goal: explain what is happening, why it matters, and what to do next

## 2. Select the research mode

### Planning mode

Use when data has not been collected yet.

Output:
- research objective
- decision statement
- hypotheses or learning goals
- sample plan
- method mix
- risk and limitation forecast

### Qualitative mode

Use when the input is interviews, support tickets, chats, reviews, open-text answers, or notes.

This mode is not complete without the deeper procedure in [qualitative-deep-dive.md](qualitative-deep-dive.md). For substantial interview work, use that document as the main operating guide.

Recommended flow:
1. Data inventory and cleaning
2. Source and sample description
3. Immersion reading
4. Coding and pattern grouping
5. Contradictions and exceptions
6. Draft findings and implications

### Quantitative mode

Use when the input is survey data or numeric summaries.

For substantial work, package outputs using [artifact-interface.md](artifact-interface.md) so later stages can read stable results from files.

Recommended flow:
1. Metric and denominator definition
2. Cleaning and deduplication rules
3. Descriptive analysis
4. Segmentation or cross-tab analysis
5. Validity checks and limitations
6. Draft findings and implications

### Mixed-method mode

Use when qual and quant both exist.

This mode should follow [mixed-method-integration.md](mixed-method-integration.md). Do not collapse single-source analysis and integration into one step.

Recommended flow:
1. Confirm whether datasets can be linked
2. Check sample comparability and bias
3. Finish single-source analysis first
4. Triangulate: agreement, tension, and complementarity
5. Separate descriptive findings from explanatory claims
6. Draft integrated findings and implications

If interviews are part of the study, the qualitative side should still follow [qualitative-deep-dive.md](qualitative-deep-dive.md) before synthesis.

## 3. Qualitative guardrails

- Preserve the original wording and context of quotes.
- Keep an audit trail from code to finding.
- Look for negative cases, not only dominant patterns.
- Distinguish what users say from what they appear to optimize for.
- Group users by behaviors, needs, or decision logic before demographics.

## 4. Quantitative guardrails

- Define the denominator for every rate.
- State whether a number comes from raw counts, filtered samples, or modeled estimates.
- Treat weak samples and self-report data cautiously.
- Separate statistical significance, practical significance, and business significance.
- If tests are not run, use neutral language like "difference observed" rather than "significant difference."

## 5. Mixed-method synthesis rules

Use three buckets:

- Agreement: qual and quant point in the same direction
- Tension: they appear to conflict
- Complementarity: one explains what the other cannot

For each integrated finding, note:
- what happened
- why it may be happening
- what evidence supports that view
- what would falsify or weaken it

## 6. Confidence labels

Use these labels consistently:

- High: multiple strong sources align, limitations do not materially change the conclusion
- Medium: evidence is decent but incomplete, biased, or partly inferential
- Low: directional signal only, useful for hypothesis generation rather than decision finalization

## 7. Common failure modes

- Jumping from quote to universal truth
- Repeating user accounts without analyzing underlying mechanism
- Calling every pattern an insight
- Hiding method limitations in fine print
- Writing generic recommendations that cannot be staffed or measured
