#!/usr/bin/env python3
"""
Lightweight validator for research reports written in Markdown.

Checks for:
- required section headings
- confidence labels
- evidence cues
- vague wording that often signals overclaiming
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = [
    "Background",
    "Method",
    "Executive",
    "Recommendation",
    "Limitation",
]

CONFIDENCE_RE = re.compile(r"\bConfidence\s*:\s*(High|Medium|Low)\b", re.IGNORECASE)
EVIDENCE_RE = re.compile(r"\b(n=|Evidence:|Source:|Confidence:)\b", re.IGNORECASE)
ROLE_RE = re.compile(r"\b(Leadership|Product|Design|Operations|Owner)\b", re.IGNORECASE)
VAGUE_PATTERNS = [
    r"\bobviously\b",
    r"\bclearly\b",
    r"\bproves\b",
    r"\ball users\b",
    r"\busers want\b",
    r"\bsignificant\b",
    r"\benhance experience\b",
    r"\bdrive value\b",
    r"\boptimi[sz]e (the )?journey\b",
    r"\bempower users\b",
    r"\bstrong demand\b",
    r"\bseamless\b",
]

SCENE_CUES_RE = re.compile(r"\b(when|while|during|because|so|trying to|ended up|at that point)\b", re.IGNORECASE)
QUOTE_RE = re.compile(r"[\"“].+?[\"”]")


def validate(text: str) -> list[str]:
    findings: list[str] = []
    lower = text.lower()

    for heading in REQUIRED_HEADINGS:
        if heading.lower() not in lower:
            findings.append(f"P1 Missing section or heading cue related to '{heading}'.")

    if not CONFIDENCE_RE.search(text):
        findings.append("P1 No explicit confidence labels found.")

    evidence_hits = len(EVIDENCE_RE.findall(text))
    if evidence_hits < 3:
        findings.append("P1 Too few evidence cues found; important claims may not be traceable.")

    role_hits = len(ROLE_RE.findall(text))
    if role_hits < 2:
        findings.append("P2 Few role-specific cues found; a shared report may not be actionable for different stakeholders.")

    quote_hits = len(QUOTE_RE.findall(text))
    scene_hits = len(SCENE_CUES_RE.findall(text))
    if quote_hits == 0:
        findings.append("P2 No user quotes found; the report may feel bloodless or overly abstract.")
    if scene_hits < 3:
        findings.append("P2 Few scene or situation cues found; key findings may be over-compressed.")

    for pattern in VAGUE_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            snippet = text[max(0, match.start() - 30): match.end() + 30].replace("\n", " ")
            findings.append(f"P2 Potential overclaiming language: '{snippet.strip()}'")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a markdown research report.")
    parser.add_argument("report", help="Path to the markdown report file")
    args = parser.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        print(f"P0 Report file not found: {report_path}")
        return 1

    text = report_path.read_text(encoding="utf-8")
    findings = validate(text)

    if not findings:
        print("PASS No obvious structural issues found.")
        return 0

    for finding in findings:
        print(finding)
    return 0


if __name__ == "__main__":
    sys.exit(main())
