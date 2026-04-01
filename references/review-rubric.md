# Review Rubric

Use this rubric before treating a report as publish-ready. It is also the default audit framework when reviewing a report written by someone else.

## Reviewer mode

When the user asks for a review:
- list findings first
- order them by severity
- focus on factual errors, evidence gaps, reasoning flaws, bias, and decision risk
- keep praise brief and secondary

Use severity labels:
- P0: report should not be used for decision-making until fixed
- P1: important weakness that materially lowers trust or usefulness
- P2: worthwhile improvement in clarity, framing, or structure

For each finding, include:
- what is wrong
- why it matters
- what evidence is missing or contradictory
- the smallest credible fix

## 1. Method transparency

Check:
- Can a reader understand where the data came from?
- Are sample, timeframe, cleaning, and linkage rules described?
- Are limitations concrete rather than generic?

## 2. Evidence integrity

Check:
- Do important numbers reconcile across sections?
- Does each key claim have evidence?
- Are quote sources and metric definitions traceable?
- Are chart takeaways consistent with the underlying data?

## 3. Reasoning quality

Check:
- Is the jump from evidence to conclusion justified?
- Are correlation and causation kept separate?
- Are alternative explanations or exceptions considered?
- Are confidence labels proportional to the evidence?

## 4. Insight depth

Check:
- Does the report explain why, not only what?
- Does it identify tensions, trade-offs, or hidden mechanisms?
- Does it avoid repackaging obvious observations as insights?

## 5. Communication quality

Check:
- Can the reader grasp the main message quickly?
- Are findings concise, scannable, and decision-relevant?
- Are vague terms replaced by numbers or bounded statements?
- Does the report sound concrete and human, rather than generic or AI-written?
- Do key sections retain user scenes, tensions, and real wording instead of flattening everything into abstract labels?

## 6. Decision usefulness

Check:
- Do recommendations clearly connect to findings?
- Are they specific enough to execute?
- Are risks, dependencies, and measurement considerations noted?
- Is it clear which functions should act on which conclusion, even though the report is shared?

## 7. Multi-stakeholder usefulness

Check:
- Can leadership quickly see the decision implications?
- Can product see which journey step or behavior needs intervention?
- Can design see what confusion, unmet expectation, or trust issue is actually happening?
- Can operations see what service or process issue needs attention?
- Does the report achieve this without duplicating itself into separate audience versions?

## Adversarial checks

Stress-test each major conclusion with questions like:
- What would make this conclusion false?
- Is this actually description disguised as explanation?
- Does the data support scope, or only direction?
- Is the report confusing self-report, observed behavior, and inferred motivation?
- Would a skeptical product lead say "show me the evidence" and get a clear answer?
- Are recommendations stronger than the evidence allows?

## Evidence trace test

For each executive finding, verify the chain:

```text
Finding -> source metric or quote -> definition / context -> limitation
```

If any link is missing, the claim is not yet publish-ready.

## Common report failures

- Executive summary overclaims compared with the body
- Limitations exist but do not constrain the final recommendation
- Quotes are vivid but not representative of the underlying pattern
- Quantitative cuts are exhaustive but not decision-relevant
- A causal story is presented without enough support
- Recommendations are generic, unprioritized, or not traceable to findings
- The prose is polished but interchangeable, with too many empty words and too little observed reality
- The report over-summarizes users until their actual need, fear, or workaround is no longer visible

## Final gate

A report is not ready if any of these remain:
- core figures cannot be traced
- limitations are omitted or materially understated
- key recommendations are not grounded in findings
- qualitative evidence is used as if it were population-representative
