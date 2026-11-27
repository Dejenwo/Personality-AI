"""Safety heuristics for life-guidance content."""

from __future__ import annotations

import re

ABUSE_PATTERNS = [
    r"\bhit(s)? me\b",
    r"\bbeats me\b",
    r"\bstrangl",
    r"\bthreaten",
    r"\bwill kill\b",
    r"\block(ed)? me\b",
    r"\btake(s)? my (money|phone|passport)\b",
    r"\bstalk",
    r"\bforced me\b",
    r"\brape",
]

ABUSE_RESPONSE = (
    "What you described may be abuse or danger, not a personality difference. "
    "I will not suggest joint exercises, confrontation scripts, or 'trying harder to understand their type' "
    "if that could increase risk.\n\n"
    "If you are in immediate danger, contact local emergency services.\n\n"
    "In the United States, the National Domestic Violence Hotline is 1-800-799-7233 "
    "or https://www.thehotline.org/.\n\n"
    "PersonalityDNA is educational. It cannot protect you in the room. A qualified local service can help with a safety plan."
)


def detect_abuse(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in ABUSE_PATTERNS)
