"""Personalized 'Understanding Who You Are' — measured vs educational vs hypothesis."""

from __future__ import annotations

from typing import Any

from app.life.codes import CODE_BY_SLUG, DISCLAIMER
from app.life.encyclopedia import encyclopedia_entry
from app.scoring.archetypes import HIGH_CUT, LOW_CUT


def _band(mean: float) -> str:
    if mean >= HIGH_CUT:
        return "high"
    if mean <= LOW_CUT:
        return "low"
    return "balanced"


def who_you_are(result_payload: dict[str, Any], extras: dict[str, Any] | None = None) -> dict[str, Any]:
    extras = extras or {}
    archetype = result_payload.get("archetype") or {}
    slug = archetype.get("slug")
    traits = result_payload.get("trait_scores") or {}
    bands = {
        key: {"mean": score.get("mean"), "scaled_0_100": score.get("scaled_0_100"), "band": _band(float(score.get("mean") or 3))}
        for key, score in traits.items()
        if isinstance(score, dict) and score.get("mean") is not None
    }
    balanced = [key for key, row in bands.items() if row["band"] == "balanced"]
    strong = [key for key, row in bands.items() if row["band"] in {"high", "low"}]
    code_meta = CODE_BY_SLUG.get(slug or "", {})
    entry = encyclopedia_entry(slug) if slug in CODE_BY_SLUG else None
    mixed = bool(archetype.get("mixed"))
    distinguish = (
        "Your four-letter educational code is a coarse label. Your actual domain means show "
        f"{', '.join(balanced) or 'no clearly mid-range domains'} near the middle and "
        f"{', '.join(strong) or 'no extreme poles'} toward a pole. Two people with the same code can still differ."
        if bands
        else "No Big Five result is on file yet. General encyclopedia copy is not your personal measurement."
    )
    return {
        "title": "Understanding Who You Are",
        "version": "1.0.0",
        "measured": {
            "instrument": result_payload.get("instrument_slug"),
            "algorithm": result_payload.get("scoring_algorithm"),
            "response_hash": result_payload.get("response_hash"),
            "archetype_slug": slug,
            "preference_code": code_meta.get("code"),
            "mixed_profile": mixed,
            "trait_bands": bands,
            "scaled_are_not_percentiles": True,
        },
        "educational": {
            "encyclopedia_title": code_meta.get("title"),
            "overview": entry["overview"] if entry else None,
            "disclaimer": DISCLAIMER,
        },
        "personalized": {
            "what_this_suggests": archetype.get("description"),
            "what_may_distinguish_you": distinguish,
            "strongest_preferences": strong,
            "balanced_preferences": balanced,
            "environments": entry["sections"][31]["content"] if entry else None,
            "frustrations": entry["sections"][22]["content"] if entry else None,
            "motivation": extras.get("motivations") or (entry["sections"][8]["content"] if entry else None),
            "possible_self_misread": "You may treat a nickname as a complete biography. Check the evidence log.",
            "how_others_might_experience_you": archetype.get("communication"),
            "habits_to_consider": extras.get("goals") or [],
            "assumptions_to_question": [
                "That people with your code are all like you.",
                "That a mid-range score is a character flaw.",
                "That career or marriage can be read from four letters.",
            ],
            "opportunities": extras.get("career_interests") or [],
        },
        "user_provided": {
            "values": extras.get("values"),
            "goals": extras.get("goals"),
            "circumstances": extras.get("circumstances"),
            "communication_notes": extras.get("communication"),
        },
        "hypotheses": {
            "label": "AI or encyclopedia hypotheses — not measured findings",
            "items": [
                "Any career list generated from interests still needs a skills and constraints check.",
                "Any relationship note still needs the other person's actual words.",
            ],
        },
        "never": [
            "We do not claim to know hidden thoughts, unconscious motives, or unreported history.",
            "We do not diagnose.",
            "We do not decide marriages, jobs, or children for you.",
        ],
    }
