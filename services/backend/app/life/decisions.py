"""Transparent decision matrix. User weights only. Not a prediction model."""

from __future__ import annotations

from typing import Any

DEFAULT_CRITERIA = [
    "financial_stability",
    "personal_fulfillment",
    "family_considerations",
    "professional_growth",
    "geographic_preferences",
    "personal_values",
    "time_commitments",
    "risk",
    "long_term_opportunities",
    "lifestyle_preferences",
]


def score_matrix(
    criteria: list[dict[str, Any]],
    options: list[dict[str, Any]],
) -> dict[str, Any]:
    """criteria: [{id, weight 0-10}], options: [{id, title, ratings: {criterion_id: 0-10}}]."""
    if not criteria or not options:
        raise ValueError("criteria and options are required")
    weight_sum = sum(float(item["weight"]) for item in criteria)
    if weight_sum <= 0:
        raise ValueError("weights must sum to more than zero")
    scored = []
    for option in options:
        total = 0.0
        breakdown = []
        for item in criteria:
            cid = item["id"]
            weight = float(item["weight"]) / weight_sum
            rating = float((option.get("ratings") or {}).get(cid, 0))
            contribution = weight * rating
            total += contribution
            breakdown.append(
                {
                    "criterion": cid,
                    "weight_share": round(weight, 4),
                    "rating": rating,
                    "contribution": round(contribution, 4),
                }
            )
        scored.append(
            {
                "id": option.get("id") or option.get("title"),
                "title": option.get("title"),
                "score": round(total, 4),
                "breakdown": breakdown,
            }
        )
    scored.sort(key=lambda row: row["score"], reverse=True)
    return {
        "version": "1.0.0",
        "method": "weighted_sum_of_user_ratings",
        "options": scored,
        "leader": scored[0] if scored else None,
        "disclaimer": (
            "Scores only reflect the numbers you entered. They are not scientifically "
            "established predictions and do not decide for you. Change a weight and the ranking can change."
        ),
        "reversible_note": "Separate reversible experiments from irreversible commitments before acting.",
    }
