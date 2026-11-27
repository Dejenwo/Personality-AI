"""Educational four-letter preference codes.

These codes are product labels derived from Big Five OCEA poles. They are
not Myers-Briggs Type Indicator results, not a licensed MBTI product, and
not a claim of affiliation with The Myers-Briggs Company.
"""

from __future__ import annotations

# OCEA pattern -> original archetype slug (same grid as scoring).
# Letters: O high≈N, O low≈S; C high≈J, C low≈P; E high≈E, E low≈I; A high≈F, A low≈T.
CODE_BY_SLUG: dict[str, dict[str, str]] = {
    "analyst": {
        "code": "INTJ",
        "title": "The Strategic Thinker",
        "cluster": "analytical",
        "energy": "I",
        "information": "N",
        "decision": "T",
        "structure": "J",
    },
    "investigator": {
        "code": "INTP",
        "title": "The Deep Thinker",
        "cluster": "analytical",
        "energy": "I",
        "information": "N",
        "decision": "T",
        "structure": "P",
    },
    "strategist": {
        "code": "ENTJ",
        "title": "The Executive Leader",
        "cluster": "analytical",
        "energy": "E",
        "information": "N",
        "decision": "T",
        "structure": "J",
    },
    "innovator": {
        "code": "ENTP",
        "title": "The Innovative Challenger",
        "cluster": "analytical",
        "energy": "E",
        "information": "N",
        "decision": "T",
        "structure": "P",
    },
    "diplomat": {
        "code": "INFJ",
        "title": "The Insightful Visionary",
        "cluster": "idealistic",
        "energy": "I",
        "information": "N",
        "decision": "F",
        "structure": "J",
    },
    "creator": {
        "code": "INFP",
        "title": "The Authentic Idealist",
        "cluster": "idealistic",
        "energy": "I",
        "information": "N",
        "decision": "F",
        "structure": "P",
    },
    "mentor": {
        "code": "ENFJ",
        "title": "The Inspirational Mentor",
        "cluster": "idealistic",
        "energy": "E",
        "information": "N",
        "decision": "F",
        "structure": "J",
    },
    "visionary": {
        "code": "ENFP",
        "title": "The Creative Explorer",
        "cluster": "idealistic",
        "energy": "E",
        "information": "N",
        "decision": "F",
        "structure": "P",
    },
    "independent-thinker": {
        "code": "ISTJ",
        "title": "The Reliable Organizer",
        "cluster": "structured",
        "energy": "I",
        "information": "S",
        "decision": "T",
        "structure": "J",
    },
    "organizer": {
        "code": "ISFJ",
        "title": "The Compassionate Protector",
        "cluster": "structured",
        "energy": "I",
        "information": "S",
        "decision": "F",
        "structure": "J",
    },
    "builder": {
        "code": "ESTJ",
        "title": "The Practical Director",
        "cluster": "structured",
        "energy": "E",
        "information": "S",
        "decision": "T",
        "structure": "J",
    },
    "connector": {
        "code": "ESFJ",
        "title": "The Community Builder",
        "cluster": "structured",
        "energy": "E",
        "information": "S",
        "decision": "F",
        "structure": "J",
    },
    "explorer": {
        "code": "ISTP",
        "title": "The Practical Problem Solver",
        "cluster": "adaptive",
        "energy": "I",
        "information": "S",
        "decision": "T",
        "structure": "P",
    },
    "advocate": {
        "code": "ISFP",
        "title": "The Creative Individualist",
        "cluster": "adaptive",
        "energy": "I",
        "information": "S",
        "decision": "F",
        "structure": "P",
    },
    "motivator": {
        "code": "ESTP",
        "title": "The Dynamic Achiever",
        "cluster": "adaptive",
        "energy": "E",
        "information": "S",
        "decision": "T",
        "structure": "P",
    },
    "collaborator": {
        "code": "ESFP",
        "title": "The Social Enthusiast",
        "cluster": "adaptive",
        "energy": "E",
        "information": "S",
        "decision": "F",
        "structure": "P",
    },
}

LETTER_MEANING = {
    "I": "Inward energy — many people with this preference recover in quieter settings.",
    "E": "Outward energy — many people with this preference recover through interaction.",
    "N": "Abstract information — many people with this preference start with patterns and possibilities.",
    "S": "Concrete information — many people with this preference start with specifics they can check.",
    "T": "Impersonal criteria — many people with this preference weigh consistency and trade-offs first.",
    "F": "Interpersonal criteria — many people with this preference weigh impact on people first.",
    "J": "Scheduled structure — many people with this preference prefer a decided plan.",
    "P": "Open structure — many people with this preference prefer keeping options available.",
}

DISCLAIMER = (
    "Four-letter codes here are educational product labels mapped from measured "
    "Big Five poles (openness, conscientiousness, extraversion, agreeableness). "
    "They are not Myers-Briggs Type Indicator results and do not imply affiliation "
    "with The Myers-Briggs Company. People with the same code still differ in "
    "intensity, emotional stability, skills, values, and circumstances. Personality "
    "is one source of information, not destiny."
)


def code_for_slug(slug: str) -> dict[str, str]:
    return CODE_BY_SLUG[slug]


def slug_for_code(code: str) -> str | None:
    wanted = code.upper()
    for slug, meta in CODE_BY_SLUG.items():
        if meta["code"] == wanted:
            return slug
    return None
