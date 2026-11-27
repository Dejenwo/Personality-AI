"""Independent financial-behavior education. Not inferred from personality type."""

from __future__ import annotations

from typing import Any

QUESTIONS = [
    {"id": "fin_01", "text": "I know roughly what I spent last month.", "facet": "tracking"},
    {"id": "fin_02", "text": "I avoid looking at my account balances.", "facet": "avoidance", "keyed": "-"},
    {"id": "fin_03", "text": "I have a written list of bills and due dates.", "facet": "organization"},
    {"id": "fin_04", "text": "I often buy things in the same hour I want them.", "facet": "impulse", "keyed": "-"},
    {"id": "fin_05", "text": "I can delay a purchase for a week without distress.", "facet": "delay"},
    {"id": "fin_06", "text": "I have money set aside for surprises (even a small amount).", "facet": "emergency"},
    {"id": "fin_07", "text": "I discuss money with the people who share expenses with me.", "facet": "communication"},
    {"id": "fin_08", "text": "I feel ashamed when I think about money, so I postpone it.", "facet": "avoidance", "keyed": "-"},
    {"id": "fin_09", "text": "I could explain my largest three expenses to a friend.", "facet": "tracking"},
    {"id": "fin_10", "text": "I take financial risks I do not understand.", "facet": "risk", "keyed": "-"},
    {"id": "fin_11", "text": "I have a goal that is written as an amount and a date.", "facet": "goals"},
    {"id": "fin_12", "text": "Household money tasks mostly fall on one person without agreement.", "facet": "communication", "keyed": "-"},
]


def score_finance(responses: dict[str, int]) -> dict[str, Any]:
    facets: dict[str, list[int]] = {}
    for item in QUESTIONS:
        raw = int(responses.get(item["id"], 0))
        if raw < 1 or raw > 5:
            continue
        value = 6 - raw if item.get("keyed") == "-" else raw
        facets.setdefault(item["facet"], []).append(value)
    means = {facet: round(sum(vals) / len(vals), 2) for facet, vals in facets.items() if vals}
    return {
        "instrument": "financial-behavior-v1",
        "validation_status": "original_unvalidated",
        "facet_means": means,
        "not_inferred_from_personality": True,
        "disclaimer": (
            "This is a self-report of habits, not a credit score, net-worth estimate, or investment recommendation. "
            "Personality type was not used. For significant financial decisions, speak with a qualified professional."
        ),
        "education": [
            "Write last month's expenses into three buckets: needs, wants, obligations.",
            "If you have no emergency buffer, start with a small automatic transfer, not a personality story.",
            "Debt: list lender, rate, minimum, and a call-to-action date. Do not shame; schedule.",
            "Couples: a weekly 20-minute money meeting beats a quarterly blow-up.",
            "Investing, tax, and legal choices are out of scope for this app.",
        ],
    }
