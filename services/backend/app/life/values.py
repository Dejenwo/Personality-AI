"""User-ranked values. Nothing is inferred from personality type."""

from __future__ import annotations

from typing import Any

VALUE_KEYS = [
    "family",
    "independence",
    "creativity",
    "financial_security",
    "achievement",
    "community",
    "faith_or_spirituality",
    "education",
    "freedom",
    "stability",
    "adventure",
    "service",
    "leadership",
    "relationships",
    "personal_growth",
    "integrity",
    "contribution",
    "meaningful_work",
]


def rank_values(rankings: dict[str, int], skip: list[str] | None = None) -> dict[str, Any]:
    skip = set(skip or [])
    items = []
    for key in VALUE_KEYS:
        if key in skip:
            continue
        if key not in rankings:
            continue
        items.append({"key": key, "rank": int(rankings[key])})
    items.sort(key=lambda row: row["rank"])
    top = [row["key"] for row in items[:5]]
    conflicts = []
    pair_checks = [
        ("independence", "family"),
        ("adventure", "stability"),
        ("achievement", "relationships"),
        ("financial_security", "meaningful_work"),
        ("freedom", "community"),
    ]
    ranks = {row["key"]: row["rank"] for row in items}
    for a, b in pair_checks:
        if a in ranks and b in ranks and abs(ranks[a] - ranks[b]) <= 2:
            conflicts.append({"pair": [a, b], "note": "These may compete in real calendars. That is information, not failure."})
    mission = None
    if top:
        mission = (
            f"I want a life that protects {top[0].replace('_', ' ')}"
            + (f" and {top[1].replace('_', ' ')}" if len(top) > 1 else "")
            + ", without pretending the other values disappeared."
        )
    return {
        "ranked": items,
        "core": top,
        "conflicts": conflicts,
        "mission_draft": mission,
        "inferred_religion_or_politics": False,
        "disclaimer": "These are self-reported ranks. Personality type was not used to infer faith, politics, or other protected characteristics.",
    }
