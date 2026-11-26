"""AI coach orchestration with a deterministic educational fallback.

Live OpenAI/Anthropic providers are used only when API keys are present.
Scores are never generated here; they are retrieved from stored results.
"""

from __future__ import annotations

import json
import re
from typing import Any

from app.config import get_settings

CRISIS_PATTERNS = [
    r"\bsuicid",
    r"\bkill myself\b",
    r"\bend my life\b",
    r"\bwant to die\b",
    r"\bself[- ]harm\b",
    r"\bhurt myself\b",
]

CRISIS_RESPONSE = (
    "I'm concerned about what you shared. PersonalityDNA Coach is an educational "
    "guide, not a crisis service, therapist, or medical professional.\n\n"
    "If you are in immediate danger, contact local emergency services now.\n\n"
    "In the United States, you can call or text 988 to reach the Suicide & Crisis Lifeline.\n"
    "International resources: https://www.iasp.info/suicidalthoughts/\n\n"
    "Please reach out to a qualified human professional or someone you trust. "
    "I will not try to assess or treat what you are going through."
)

INJECTION_PATTERNS = [
    r"ignore (all|any|previous|prior) instructions",
    r"you are now",
    r"reveal (your )?(system|hidden) prompt",
    r"disregard (the )?(rules|guardrails)",
]


def detect_crisis(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in CRISIS_PATTERNS)


def detect_injection(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in INJECTION_PATTERNS)


def select_agent(message: str) -> str:
    text = message.lower()
    rules = [
        ("career", "career"),
        ("job", "career"),
        ("interview", "career"),
        ("lead", "leadership"),
        ("delegate", "leadership"),
        ("relationship", "relationship"),
        ("partner", "relationship"),
        ("conflict", "relationship"),
        ("habit", "motivation"),
        ("goal", "motivation"),
        ("procrastinat", "motivation"),
        ("progress", "progress"),
        ("report", "report"),
        ("research", "education"),
        ("study", "education"),
        ("grow", "growth"),
        ("develop", "growth"),
    ]
    for needle, agent in rules:
        if needle in text:
            return agent
    return "insight"


class EducationalProvider:
    """Grounded, deterministic coach used in development, tests, and when no vendor key exists."""

    name = "educational-fallback"

    def complete(self, message: str, context: dict[str, Any], agent: str) -> dict[str, Any]:
        archetype = (context.get("archetype") or {}).get("name") or "your unfolding profile"
        traits = context.get("trait_summaries") or []
        trait_line = "; ".join(traits[:5]) if traits else "No Big Five result is on file yet."
        goals = context.get("goals") or []
        goal_line = ", ".join(g["title"] for g in goals[:3]) if goals else "no goals saved yet"
        exercises = context.get("exercises") or []
        weekly = exercises[0] if exercises else "Pick one 15-minute practice and schedule it twice this week."
        playbooks = {
            "insight": (
                f"From your measured results, you currently map to {archetype}. "
                f"Trait snapshot: {trait_line}. I am explaining those scores, not changing them. "
                f"A concrete practice for this week: {weekly}"
            ),
            "growth": (
                f"A practical growth step for {archetype} this week: {weekly} "
                "Pair it with a review date. This is not a personality transplant."
            ),
            "career": (
                "Career interests are not competence. Use them to generate questions and experiments, "
                "then test against real tasks and values. PersonalityDNA will not rate hiring fitness."
            ),
            "leadership": (
                "Leadership preferences describe how you like to influence, not whether you are allowed to lead. "
                "Try one behavior: name the decision, the owner, and the review point."
            ),
            "relationship": (
                "Comparison is only useful with consent and without scorekeeping. "
                "Try speaking a need in one sentence, then asking one curious question."
            ),
            "motivation": (
                f"Goals on file: {goal_line}. Shrink the next action until it can be done in 15 minutes, "
                "then mark it done without self-attack if you miss a day."
            ),
            "education": (
                "I can share general educational framing. I will not invent citations or claim clinical validation "
                "for original PersonalityDNA inventories."
            ),
            "progress": (
                "Progress is the count of kept promises to yourself, not a more flattering archetype. "
                "Look at habits, program days, and journal entries you authorized."
            ),
            "report": (
                "Reports reproduce stored scores and interpretation copy. They should match the scoring engine exactly."
            ),
        }
        body = playbooks.get(agent, playbooks["insight"])
        reply = (
            f"{body}\n\nYou said: “{message.strip()[:280]}”.\n\n"
            "I am PersonalityDNA Coach, an educational assistant — not a psychologist, therapist, "
            "or medical professional. I do not diagnose. Measured scores stay in the assessment engine; "
            "I only interpret authorized results and what you just told me."
        )
        return {
            "provider": self.name,
            "agent": agent,
            "content": reply,
            "grounding": {
                "measured_findings": bool(context.get("archetype") or context.get("trait_summaries")),
                "user_provided": True,
                "educational": True,
                "sources": ["stored_assessment_results", "user_message", "reviewed_playbooks"],
            },
        }


class OpenAIProvider:
    name = "openai"

    def complete(self, message: str, context: dict[str, Any], agent: str) -> dict[str, Any]:
        settings = get_settings()
        import httpx

        system = _system_prompt(agent, context)
        response = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={
                "model": settings.openai_model,
                "temperature": 0.4,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
            },
            timeout=45.0,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return {
            "provider": self.name,
            "agent": agent,
            "content": content,
            "grounding": {"provider": "openai", "measured_findings": True, "educational": True},
        }


class AnthropicProvider:
    name = "anthropic"

    def complete(self, message: str, context: dict[str, Any], agent: str) -> dict[str, Any]:
        settings = get_settings()
        import httpx

        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.anthropic_api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": settings.anthropic_model,
                "max_tokens": 800,
                "system": _system_prompt(agent, context),
                "messages": [{"role": "user", "content": message}],
            },
            timeout=45.0,
        )
        response.raise_for_status()
        content = "".join(part.get("text", "") for part in response.json().get("content", []))
        return {
            "provider": self.name,
            "agent": agent,
            "content": content,
            "grounding": {"provider": "anthropic", "measured_findings": True, "educational": True},
        }


def _system_prompt(agent: str, context: dict[str, Any]) -> str:
    return (
        "You are PersonalityDNA Coach, an educational personal-development assistant. "
        "You are not a psychologist, therapist, or medical professional. Never diagnose. "
        "Never invent assessment scores. Never claim original PersonalityDNA inventories are validated. "
        "Distinguish measured findings, user-provided information, and general education. "
        "If the user is in crisis, direct them to human emergency resources and 988 / IASP. "
        f"Active capability: {agent}. Authorized context JSON: {json.dumps(context)[:6000]}"
    )


def get_provider():
    settings = get_settings()
    if settings.ai_provider == "educational":
        return EducationalProvider()
    if settings.ai_provider in ("openai", "auto") and settings.openai_api_key:
        return OpenAIProvider()
    if settings.ai_provider in ("anthropic", "auto") and settings.anthropic_api_key:
        return AnthropicProvider()
    return EducationalProvider()


def coach_reply(message: str, context: dict[str, Any]) -> dict[str, Any]:
    if detect_crisis(message):
        return {
            "provider": "safety",
            "agent": "safety",
            "content": CRISIS_RESPONSE,
            "grounding": {"crisis_protocol": True},
            "safety": {"crisis": True, "blocked": False},
        }
    if detect_injection(message):
        return {
            "provider": "safety",
            "agent": "safety",
            "content": (
                "I will stay inside PersonalityDNA Coach's educational role. "
                "I cannot reveal hidden prompts, ignore safety rules, or change assessment scores."
            ),
            "grounding": {"injection_attempt": True},
            "safety": {"prompt_injection": True},
        }
    agent = select_agent(message)
    provider = get_provider()
    try:
        result = provider.complete(message, context, agent)
    except Exception:
        result = EducationalProvider().complete(message, context, agent)
        result["safety"] = {"provider_fallback": True}
    result.setdefault("safety", {"crisis": False})
    return result
