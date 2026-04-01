# Single Report for Multiple Stakeholders

Use this when one report must serve leadership, product, design, operations, and other cross-functional readers.

## Principle

Do not create separate report versions by default. Instead, write one report with:
- a shared top-line story
- clear decision implications
- role-specific takeaways embedded in the same structure

## Recommended structure additions

### In the executive findings section

For each major finding, include:
- what happened
- why it matters overall
- which roles should care most

Suggested format:

```markdown
**Finding X:** [bounded conclusion]
What we saw: [evidence]
User reality: [quote or scene]
Who should care: Leadership | Product | Design | Operations
Why it matters: [decision implication]
```

### In the recommendations section

Use one shared table rather than role-specific appendices.

Suggested columns:
- priority
- action
- owner role
- supported by
- expected impact
- risk or dependency

## Role-specific reading guidance

Make it easy for each role to scan the same report:

- Leadership: what decision changes now, what risk remains
- Product: what behavior or journey step to change
- Design: what user confusion, expectation gap, or interaction problem is visible
- Operations: what service, process, or communication gap shows up in the data

## Failure mode to avoid

One-report does not mean one-size-fits-all wording. The report should still make it obvious why different functions should care, without fragmenting into separate versions.
