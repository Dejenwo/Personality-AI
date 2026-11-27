"""Life Blueprint: include only sections the user has data or consent for."""

from __future__ import annotations

from typing import Any

from app.life.encyclopedia import encyclopedia_entry
from app.life.insights import who_you_are
from app.life.occupations import explore_for_interests

SECTION_KEYS = [
    "executive_summary",
    "preference_code",
    "big_five",
    "values",
    "motivations",
    "strengths",
    "development",
    "blind_spots",
    "communication",
    "social",
    "emotional_awareness",
    "stress",
    "career",
    "professional_development",
    "leadership",
    "entrepreneurship",
    "relationship_communication",
    "marriage",
    "parenting",
    "family",
    "financial_habits",
    "productivity",
    "learning",
    "life_decisions",
    "purpose",
    "short_term_goals",
    "long_term_goals",
    "plan_30",
    "plan_90",
    "plan_365",
]


def build_blueprint(result_payload: dict[str, Any], extras: dict[str, Any] | None = None, exclude: list[str] | None = None) -> dict[str, Any]:
    extras = extras or {}
    exclude = set(exclude or extras.get("exclude") or [])
    who = who_you_are(result_payload, extras)
    slug = (result_payload.get("archetype") or {}).get("slug")
    entry = encyclopedia_entry(slug) if slug else None
    riasec = extras.get("riasec") or []
    career = explore_for_interests(riasec, extras.get("skills")) if riasec else None

    raw_sections = {
        "executive_summary": who["personalized"]["what_this_suggests"],
        "preference_code": who["measured"]["preference_code"],
        "big_five": who["measured"]["trait_bands"],
        "values": extras.get("values"),
        "motivations": extras.get("motivations"),
        "strengths": result_payload.get("strengths"),
        "development": result_payload.get("growth_areas"),
        "blind_spots": entry["blind_spots"][:8] if entry else None,
        "communication": (result_payload.get("archetype") or {}).get("communication"),
        "social": entry["sections"][25]["content"] if entry else None,
        "emotional_awareness": entry["sections"][21]["content"] if entry else None,
        "stress": entry["sections"][22]["content"] if entry else None,
        "career": career,
        "professional_development": extras.get("skills"),
        "leadership": extras.get("leadership") or (entry["sections"][34]["content"] if entry else None),
        "entrepreneurship": extras.get("entrepreneurship"),
        "relationship_communication": extras.get("relationship"),
        "marriage": extras.get("marriage"),
        "parenting": extras.get("parenting"),
        "family": extras.get("family"),
        "financial_habits": extras.get("finance"),
        "productivity": extras.get("productivity"),
        "learning": extras.get("learning"),
        "life_decisions": extras.get("decisions"),
        "purpose": extras.get("mission") or (entry["sections"][56]["content"] if entry else None),
        "short_term_goals": extras.get("goals"),
        "long_term_goals": extras.get("long_term_goals"),
        "plan_30": "Pick one skill practice and one conversation. Review on day 30.",
        "plan_90": "Three experiments, one body of evidence (portfolio, budget, or habit log).",
        "plan_365": "Four seasonal reviews of work, relationships, money, and health-adjacent habits (non-clinical).",
    }
    sections = []
    for key in SECTION_KEYS:
        if key in exclude:
            continue
        value = raw_sections.get(key)
        if value in (None, [], {}, ""):
            continue
        sections.append({"key": key, "content": value, "basis": "included because user data or a measured result exists"})
    return {
        "title": "My Life Blueprint",
        "subtitle": "A personalized guide to understanding yourself and developing your potential",
        "price_hypothesis_usd": 39.99,
        "version": "1.0.0",
        "who_you_are": who,
        "sections": sections,
        "excluded": sorted(exclude),
        "page_estimate_note": (
            "Length depends on available information. This is not padded to a page count. "
            "A 50–100 page commercial PDF would require more user-provided material than a single Big Five result."
        ),
        "disclaimer": who["educational"]["disclaimer"],
    }
