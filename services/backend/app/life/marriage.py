"""Relationship education and premarital discussion.

No compatibility percentages. No marriage verdicts. Abuse is not a personality difference.
"""

from __future__ import annotations

from typing import Any

from app.life.codes import CODE_BY_SLUG, DISCLAIMER, LETTER_MEANING

PREMARITAL_CATEGORIES = [
    "values_and_beliefs",
    "marriage_expectations",
    "financial_responsibilities",
    "children_and_parenting",
    "communication",
    "conflict_management",
    "family_relationships",
    "career_and_education",
    "household_responsibilities",
    "lifestyle",
    "personal_boundaries",
    "emotional_needs",
    "future_goals",
    "trust_and_commitment",
    "health_expectations",
]


def _q(category: str, text: str) -> dict[str, str]:
    return {"category": category, "text": text, "mode": "discussion_not_test"}


PREMARITAL_QUESTIONS: list[dict[str, str]] = []

_BANK = {
    "values_and_beliefs": [
        "What does a good life mean to you in the next ten years?",
        "Which values are non-negotiable, and which are preferences?",
        "How do you want faith, philosophy, or non-religion to show up in a household, if at all?",
        "What traditions do you want to keep, adapt, or stop?",
        "How should we handle disagreement about politics without humiliating each other?",
        "What does honesty require when the truth will disappoint me?",
        "How do we treat people who have less power than we do?",
        "What does 'family' mean to you beyond blood relatives?",
        "Which secrets are never acceptable in a marriage?",
        "How will we revisit values as we age?",
    ],
    "marriage_expectations": [
        "What does commitment mean in practice on an ordinary Tuesday?",
        "What would make you feel married besides a ceremony?",
        "How much time together is enough in a typical week?",
        "What does loyalty look like with phones, friends, and travel?",
        "How should we handle attraction to other people?",
        "What does a trial separation mean to you, if anything?",
        "Who do we tell about marital conflict, and who is off-limits?",
        "What does a healthy apology include?",
        "How will we celebrate and how will we grieve?",
        "What would 'we failed this marriage' mean, and who would we ask for help before that?",
    ],
    "financial_responsibilities": [
        "What does financial responsibility mean to you in numbers, not slogans?",
        "Will we merge accounts, keep some separate, or use another structure?",
        "What debt are you bringing, and what is the plan?",
        "What does an emergency fund mean in months of expenses?",
        "Who pays which bills, and how is that reviewed?",
        "How much can either of us spend without a conversation?",
        "How do we handle family members who ask for money?",
        "What does financial infidelity mean to you?",
        "How do we plan for disability, death, and aging parents?",
        "Which professional (planner, counselor, attorney) would we consult for a large decision?",
    ],
    "children_and_parenting": [
        "Do you want children, and how sure are you?",
        "If we cannot or do not have children, what then?",
        "What does discipline mean to you, and what is off-limits?",
        "How should household labor change after a child arrives?",
        "What role should grandparents play, and what is a boundary?",
        "How will we talk about screens, food, and sleep?",
        "How will we handle disagreement about a child's education?",
        "What support would we need to be decent parents?",
        "How do we protect a child's privacy from social media?",
        "What would we do if a child needed more support than we expected?",
    ],
    "communication": [
        "How do you prefer to handle disagreements?",
        "How do you prefer to receive appreciation?",
        "How much personal time do you need after work?",
        "What does 'being heard' look like in your body, not in theory?",
        "When is texting acceptable for hard topics, and when is it not?",
        "What tone crosses a line for you?",
        "How do we pause a fight that is getting cruel?",
        "What do you need after a repair — space, touch, or a plan?",
        "Which topics are hard for you to start?",
        "How will we check that we understood, not just replied?",
    ],
    "conflict_management": [
        "What did conflict look like in the home you grew up in?",
        "What is your first move when you feel criticized?",
        "Is raising a voice ever acceptable, and when does it become intimidation?",
        "What does stonewalling look like for you?",
        "How do we handle a fight in front of other people?",
        "What is the difference between a preference and a deal-breaker in conflict?",
        "Who is allowed to referee, and who is not?",
        "What would make you afraid in an argument?",
        "How do we come back after a bad night?",
        "When is professional help required, not optional?",
    ],
    "family_relationships": [
        "What boundaries should exist with extended family?",
        "How should major family decisions be made?",
        "How often will we visit whose parents, and who decides?",
        "What information about our marriage is not for relatives?",
        "How do we handle a relative who is unkind to one of us?",
        "What does holidays fairness look like?",
        "How will we support a sibling or parent in crisis without disappearing from each other?",
        "What family secrets are we refusing to carry?",
        "How do we talk about in-laws without contempt?",
        "What happens if a family member asks us to take sides?",
    ],
    "career_and_education": [
        "What are your long-term career goals?",
        "Whose job would we relocate for, and under what terms?",
        "How do we handle a season when one of us earns less?",
        "What education or training is still on the table?",
        "How many hours of work per week feels sustainable?",
        "What does ambition mean in this marriage?",
        "How do we protect a job search from becoming a secret?",
        "What happens if one of us hates their work?",
        "How do we handle a business owned by one of us?",
        "What support looks like during a credential program?",
    ],
    "household_responsibilities": [
        "How should household responsibilities be divided?",
        "What is the standard of clean that we can both live with?",
        "Who notices unpaid labor, and how do we make it visible?",
        "How do we handle different energy levels for chores?",
        "What do we outsource if we can afford it, and what do we never outsource?",
        "Who owns cars, trash, meals, and admin?",
        "How do we renegotiate after a job change or a baby?",
        "What is a fair way to call out dropped balls without contempt?",
        "How do we handle guests and the work they create?",
        "What does rest look like for each of us at home?",
    ],
    "lifestyle": [
        "How do you want a typical weekend to feel?",
        "What substances are acceptable, and what is a hard no?",
        "How much socializing is enough?",
        "What does travel mean — rest, adventure, or family duty?",
        "How do we handle different sleep schedules?",
        "What hobbies are protected time?",
        "How do we feel about pets?",
        "What does privacy in a shared home look like?",
        "How do we handle phones at meals and in bed?",
        "What lifestyle change would you refuse?",
    ],
    "personal_boundaries": [
        "What does personal time mean, and how do we ask for it without punishment?",
        "What is okay to share about our marriage with friends?",
        "How do we handle exes, including digital contact?",
        "What physical space do you need when upset?",
        "What jokes are off-limits?",
        "How do we treat each other's work time?",
        "What does consent look like on an ordinary night, not only a first date?",
        "How do we handle a 'no' without sulking?",
        "What tracking of location or devices is never okay?",
        "How do we protect each other's medical and journal privacy?",
    ],
    "emotional_needs": [
        "How do you prefer to receive comfort — words, presence, help, or space?",
        "What does emotional availability mean on a work night?",
        "How do we handle one of us being depressed or anxious without diagnosing the other?",
        "What support is a partner's job, and what belongs to a professional?",
        "How do we talk about loneliness inside the relationship?",
        "What does feeling desired mean to you besides sex?",
        "How do we handle different desire levels with respect?",
        "What childhood pattern are you trying not to repeat?",
        "How will we notice we are roommates, not partners?",
        "What would make you feel emotionally unsafe?",
    ],
    "future_goals": [
        "Where do you want to live in five years, and what would change that?",
        "What does retirement even mean to you?",
        "How do we handle aging parents as a joint project?",
        "What big purchase needs a shared yes?",
        "What does a meaningful life look like if careers stall?",
        "How do we plan for climate, health, or economic shocks without panic theater?",
        "What is a five-year relationship review?",
        "Which friendships do we want to still have?",
        "What would we regret not trying?",
        "How often do we update the plan on purpose?",
    ],
    "trust_and_commitment": [
        "What does commitment mean to you?",
        "What rebuilds trust after a break, and what never does?",
        "How transparent should phones, passwords, and locations be — and why?",
        "What is the difference between privacy and secrecy here?",
        "How do we handle a lie of omission?",
        "What does faithfulness include besides sex?",
        "How do we talk about past relationships without scorekeeping?",
        "What would you need if I broke your trust?",
        "Who is our emergency contact besides each other?",
        "How do we keep promises small enough to keep?",
    ],
    "health_expectations": [
        "What health information are you willing to share, and what stays with a clinician?",
        "How do we support each other through illness without becoming a parent?",
        "What are our views on preventive care?",
        "How do we handle different risk tolerances about the body?",
        "What substances, sleep, and food patterns are we willing to negotiate?",
        "How do we plan for disability?",
        "What mental-health care is expected, not optional, when functioning drops?",
        "How do we talk about fertility and reproductive health if relevant?",
        "What is never a partner's job to treat?",
        "When do we call a professional instead of googling?",
    ],
}

for category, questions in _BANK.items():
    for text in questions:
        PREMARITAL_QUESTIONS.append(_q(category, text))

assert len(PREMARITAL_QUESTIONS) == 150, len(PREMARITAL_QUESTIONS)

ABUSE_NOT_PERSONALITY = (
    "Personality differences do not excuse physical violence, threats, coercion, "
    "controlling behavior, financial abuse, sexual coercion, intimidation, stalking, "
    "or emotional abuse. If you are in danger, contact local emergency services. "
    "In the United States, the National Domestic Violence Hotline is 1-800-799-7233 "
    "or https://www.thehotline.org/. This app will not recommend joint exercises or "
    "confrontation when they could increase danger."
)


def pairing_notes(slug_a: str, slug_b: str) -> dict[str, Any]:
    a = CODE_BY_SLUG[slug_a]
    b = CODE_BY_SLUG[slug_b]
    diffs = []
    sims = []
    for key, label in (
        ("energy", "social energy"),
        ("information", "information style"),
        ("decision", "decision style"),
        ("structure", "planning style"),
    ):
        if a[key] == b[key]:
            sims.append(f"Both codes lean {a[key]} on {label}. {LETTER_MEANING[a[key]]}")
        else:
            diffs.append(
                f"{a['code']} leans {a[key]} and {b['code']} leans {b[key]} on {label}. "
                f"This is a discussion topic, not a verdict."
            )
    return {
        "code_a": a["code"],
        "code_b": b["code"],
        "title_a": a["title"],
        "title_b": b["title"],
        "similarities": sims or ["These codes differ on the four educational letters."],
        "differences": diffs or ["These codes share the four educational letters; people still differ in intensity and skill."],
        "complementary_tendencies": [
            "Different paces can help a pair cover more ground if both people consent to the split of labor.",
            "Different paces can also become contempt. Watch for scorekeeping.",
        ],
        "misunderstandings": [
            "Silence may be recovery for one person and rejection for the other.",
            "A fast decision may look like care to one person and steamrolling to the other.",
        ],
        "strategies": [
            "Translate needs into one sentence plus one question.",
            "Do not use a preference code to win an argument.",
            "Keep money, children, and safety as explicit topics, not type inferences.",
        ],
        "exercises": [
            "Each person writes three needs and three offers, then swaps without rebuttal for five minutes.",
            "Schedule a weekly 30-minute state of the union with a pause word.",
        ],
        "compatibility_percent": None,
        "verdict": None,
        "disclaimer": DISCLAIMER,
        "safety": ABUSE_NOT_PERSONALITY,
    }


def marriage_prep_report(individual_a: dict[str, Any], individual_b: dict[str, Any] | None, shared_answers: list[dict] | None) -> dict[str, Any]:
    return {
        "title": "Marriage Preparation Discussion Report",
        "version": "1.0.0",
        "individuals": [individual_a, individual_b] if individual_b else [individual_a],
        "pairing": pairing_notes(individual_a["slug"], individual_b["slug"]) if individual_b else None,
        "shared_answers": shared_answers or [],
        "unresolved": [row for row in (shared_answers or []) if row.get("status") == "unresolved"],
        "approval": None,
        "disclaimer": "This report supports discussion. It does not approve, reject, or rank a marriage.",
        "safety": ABUSE_NOT_PERSONALITY,
    }
