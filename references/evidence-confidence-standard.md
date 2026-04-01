# Evidence and Confidence Standard

Use this standard whenever the report includes findings, implications, or recommendations.

## Claim taxonomy

Classify each important statement as one of:

- Fact: directly supported by observed data or explicit source material
- Finding: a bounded pattern supported by evidence
- Insight: an explanation of why the pattern may exist
- Hypothesis: a forward-looking or weakly supported interpretation
- Recommendation: an action proposed on top of findings and constraints

Do not label a hypothesis as a finding.

## Confidence scale

### High

Use only when:
- evidence is strong and internally consistent
- major limitations do not reverse the conclusion
- multiple sources or checks support the same direction

### Medium

Use when:
- the pattern is credible but still exposed to sample, measurement, or interpretation limits
- evidence is partly indirect or not fully triangulated

### Low

Use when:
- evidence is sparse, conflicting, or highly biased
- the statement is mainly useful for hypothesis generation

## Confidence drivers

Judge confidence using these dimensions:
- source quality
- sample quality
- consistency across sources
- clarity of metric or quote context
- plausibility of alternative explanations

## Claim-writing pattern

Recommended pattern:

```markdown
**Claim:** [bounded conclusion]
Type: Fact | Finding | Insight | Hypothesis | Recommendation
Evidence: [metric / quote / comparison]
Confidence: High | Medium | Low
Boundary: [for whom / under what condition]
```

Use citation formats from [citation-style.md](citation-style.md) so claims stay traceable across analysis and reporting.

## Minimum support rule

For major report claims, aim to include:
- one hard support item: number, denominator, or explicit pattern count
- one human support item: quote, scene, or concrete behavior description

If only one kind of support exists, say so and lower confidence when needed.

## Escalation rules

Lower confidence when:
- the denominator is unclear
- subgroup sample size is small
- only one vivid quote supports the claim
- sampling bias likely changes interpretation
- the report confuses correlation with causation

Raise confidence only when the evidence improves, not when the wording gets stronger.

## Recommendation rule

A recommendation should never have higher confidence than the finding it depends on unless there is independent operational evidence supporting it.
