# Iteration Playbook

Use this when a report needs revision after review, or when the user asks to improve someone else's research output.

## Revision goals

Strengthen the report without laundering weak evidence into stronger-sounding claims.

Priority order:
1. factual correctness
2. methodological honesty
3. reasoning quality
4. decision usefulness
5. clarity and polish

## Triage model

### P0: factual or methodological blockers

Examples:
- wrong numbers
- unsupported core conclusions
- hidden sample bias that changes interpretation
- confusion between linked and unlinked datasets

Action:
- fix or remove the claim
- recompute or re-check against source material
- rewrite any downstream recommendation affected by the fix

### P1: trust and usefulness problems

Examples:
- confidence is too high
- recommendations are not directly supported
- important caveats or exceptions are missing
- insight language is stronger than the evidence

Action:
- narrow the claim
- add caveats near the finding
- reconnect actions to evidence
- label what remains hypothesis versus established finding

### P2: communication issues

Examples:
- verbose wording
- weak section order
- charts or tables do not foreground the takeaway
- mixed audiences are not handled well

Action:
- tighten writing
- move answer-first content earlier
- improve titles, grouping, and signposting

## Revision workflow

1. Create a finding list from the review.
2. Group fixes into:
   - evidence fixes
   - inference fixes
   - structure and communication fixes
3. Fix high-severity issues first.
4. If the issue originated upstream, follow [rollback-rules.md](rollback-rules.md) and return to the correct analysis stage instead of only patching report prose.
4. Re-run the review rubric against the revised report.
5. Summarize what changed and what risk still remains.

## Rewrite patterns

### Overclaim to bounded claim

Before:
`Users do not trust the onboarding flow.`

After:
`Among interviewed new users, distrust centered on identity verification and unclear data usage messaging. This is a strong qualitative signal, but not a population estimate.`

### Description to insight

Before:
`Older users asked more questions during setup.`

After:
`Users with lower digital confidence often used extra questions to reduce perceived irreversible mistakes during setup, suggesting reassurance and recoverability matter more than speed for this segment.`

### Generic recommendation to decision-ready action

Before:
`Improve the experience.`

After:
`Test a revised verification step that explains why each document is needed and what happens next, then measure completion rate, drop-off at verification, and trust perception among first-time applicants.`

## Final revision note

When handing back a revised report, state:
- what was corrected
- which claims were weakened or removed
- what still needs source validation
- whether the report is now decision-ready, directional only, or not yet reliable
