"""Adult parenting education. No child typing. No inferred developmental conditions."""

from __future__ import annotations

from typing import Any

from app.life.encyclopedia import encyclopedia_entry
from app.life.codes import DISCLAIMER

PROGRAMS = [
    {
        "slug": "attentive-parent-7",
        "name": "7-day attentive parent reflection",
        "days": 7,
        "summary": "Notice your own reactions. Do not type your child.",
    },
    {
        "slug": "family-communication-30",
        "name": "30-day family communication",
        "days": 30,
        "summary": "Repair scripts, listening, and household meetings.",
    },
    {
        "slug": "patience-practice-30",
        "name": "30-day patience practice",
        "days": 30,
        "summary": "Pause skills for adults. Not a diagnosis of a child.",
    },
    {
        "slug": "family-routines-60",
        "name": "60-day family routines",
        "days": 60,
        "summary": "Sleep, meals, and screens as agreements, not personality wars.",
    },
]


def parenting_guide(slug: str) -> dict[str, Any]:
    entry = encyclopedia_entry(slug)
    return {
        "adult_profile": {"slug": slug, "preference_code": entry["preference_code"], "title": entry["title"]},
        "potential_strengths": entry["sections"][47]["content"],
        "potential_blind_spots": [
            "Reading a child's mood as defiance of your type.",
            "Using adult preference language to label a child.",
            "Skipping the other caregiver's actual agreement.",
        ],
        "exercises": [
            "Describe a hard moment as behavior + need, not as the child's 'personality'.",
            "Ask the other adult what they saw, then do not rebut for one minute.",
            "Protect one stretch of child-led play with no teaching.",
        ],
        "activities": [
            "A weekly family meeting with one appreciation and one logistics item.",
            "A repair after a raised voice: what happened, what you wish, what you will try.",
        ],
        "reflections": [
            "Which of my reactions is about my history, not this child?",
            "Where am I asking a child to regulate me?",
        ],
        "never": [
            "Do not assign a four-letter code to a child.",
            "Do not infer ADHD, autism, or future ability from an adult assessment.",
            "Do not choose discipline solely from your type.",
        ],
        "disclaimer": DISCLAIMER,
    }
