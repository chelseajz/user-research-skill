# Artifact Interface

Use this for substantial multi-step projects so each phase hands off stable outputs to the next.

## Principle

Prefer file-based handoffs over conversational memory. Later stages should read prior outputs from files whenever possible.

## Recommended directories

### Quantitative outputs

`survey_output/`

Recommended files:
- `survey_results.json`
- `survey_analysis.md`
- `charts/`

## Qualitative outputs

`code_output/`

Recommended files:
- `coding_summary.json`
- `codebook.md`
- `quote_bank.md`
- `casebook.md`
- `contradictions.md`

## Mixed-method outputs

`analyze_output/`

Recommended files:
- `integration_results.json`
- `integration_memo.md`
- `propositions.md`
- `charts/`

## Insight outputs

`insight_output/`

Recommended files:
- `insights.md`
- `finding_ledger.md`

## Report outputs

`report_output/`

Recommended files:
- `final_report.md`
- `review_findings.md`
- `revision_note.md`

## Reading rule

When a valid file path is available, read the artifact rather than relying only on the conversation history.
