"""Deterministic personality scoring engine.

The same responses to the same instrument version always produce identical
scores. AI systems must not call this module to invent or alter scores.
"""

from __future__ import annotations

import hashlib
import json
import math
import statistics
from dataclasses import asdict, dataclass, field
from typing import Any, Iterable

from app.scoring.archetypes import ARCHETYPES, ArchetypeMatch, match_archetypes
from app.scoring.catalog import INSTRUMENTS, TRAIT_META, instrument_by_slug


class ScoringError(ValueError):
    pass


@dataclass(frozen=True)
class TraitScore:
    trait: str
    name: str
    raw_sum: float
    mean: float
    scaled_0_100: float
    item_count: int
    answered_count: int
    missing_count: int
    min_possible: float
    max_possible: float
    explanation: str


@dataclass(frozen=True)
class QualityIndicators:
    missing_ratio: float
    straightlining: bool
    max_run_length: int
    response_variance: float
    acquiescence_index: float
    flags: tuple[str, ...]


@dataclass
class ScoringResult:
    instrument_slug: str
    instrument_version: str
    framework: str
    trait_scores: dict[str, TraitScore]
    derived_scores: dict[str, TraitScore]
    archetype: ArchetypeMatch | None
    secondary_archetype: dict[str, Any] | None
    quality: QualityIndicators
    strengths: list[str]
    growth_areas: list[str]
    response_hash: str
    scoring_algorithm: str = "personalitydna.scoring.v1"
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "instrument_slug": self.instrument_slug,
            "instrument_version": self.instrument_version,
            "framework": self.framework,
            "scoring_algorithm": self.scoring_algorithm,
            "response_hash": self.response_hash,
            "trait_scores": {k: asdict(v) for k, v in self.trait_scores.items()},
            "derived_scores": {k: asdict(v) for k, v in self.derived_scores.items()},
            "quality": asdict(self.quality),
            "strengths": self.strengths,
            "growth_areas": self.growth_areas,
            "notes": self.notes,
            "archetype": None,
            "secondary_archetype": self.secondary_archetype,
        }
        if self.archetype:
            primary = ARCHETYPES[self.archetype.slug]
            payload["archetype"] = {
                **{k: primary[k] for k in ("slug", "name", "tagline", "palette", "symbol", "description")},
                "pattern": self.archetype.pattern,
                "mixed": self.archetype.mixed,
                "leaning": self.archetype.leaning,
                "preferences": primary["preferences"],
                "strengths": primary["strengths"],
                "growth_areas": primary["growth_areas"],
                "communication": primary["communication"],
                "leadership": primary["leadership"],
                "relationships": primary["relationships"],
                "work_environment": primary["work_environment"],
                "reflections": primary["reflections"],
                "exercises": primary["exercises"],
                "disclaimer": (
                    "Archetypes are descriptive product constructs mapped from measured "
                    "trait scores. They are not scientifically established personality "
                    "categories and are not a Myers-Briggs type."
                ),
            }
        return payload


class ScoringEngine:
    def __init__(self, instruments: Iterable[dict[str, Any]] | None = None) -> None:
        self._instruments = {item["slug"]: item for item in (instruments or INSTRUMENTS)}

    def get_instrument(self, slug: str) -> dict[str, Any]:
        instrument = self._instruments.get(slug) or instrument_by_slug(slug)
        if not instrument:
            raise ScoringError(f"Unknown instrument: {slug}")
        return instrument

    def list_instruments(self) -> list[dict[str, Any]]:
        public = []
        for instrument in self._instruments.values():
            public.append(self.public_instrument(instrument))
        return public

    def public_instrument(self, instrument: dict[str, Any], include_items: bool = False) -> dict[str, Any]:
        payload = {
            "slug": instrument["slug"],
            "name": instrument["name"],
            "short_name": instrument["short_name"],
            "version": instrument["version"],
            "framework": instrument["framework"],
            "duration_minutes": instrument["duration_minutes"],
            "item_count": instrument["item_count"],
            "is_free": instrument["is_free"],
            "tier": instrument["tier"],
            "category": instrument["category"],
            "description": instrument["description"],
            "scientific": instrument.get("scientific", {}),
        }
        if include_items:
            payload["instructions"] = instrument["instructions"]
            payload["scale"] = instrument["scale"]
            payload["items"] = [
                {"id": item["id"], "text": item["text"], "min_value": item["min_value"], "max_value": item["max_value"]}
                for item in instrument["items"]
            ]
        return payload

    def score(
        self,
        slug: str,
        responses: dict[str, int | float | None],
        instrument_version: str | None = None,
    ) -> ScoringResult:
        instrument = self.get_instrument(slug)
        if instrument_version and instrument_version != instrument["version"]:
            raise ScoringError(
                f"Version mismatch: requested {instrument_version}, loaded {instrument['version']}"
            )
        items = instrument["items"]
        item_by_id = {item["id"]: item for item in items}
        unknown = set(responses) - set(item_by_id)
        if unknown:
            raise ScoringError(f"Unknown item ids: {sorted(unknown)}")

        numeric_values: list[float] = []
        for item in items:
            raw = responses.get(item["id"])
            if raw is None:
                continue
            value = float(raw)
            if value < item["min_value"] or value > item["max_value"]:
                raise ScoringError(f"Response out of range for {item['id']}: {value}")
            if not float(value).is_integer():
                raise ScoringError(f"Response must be an integer Likert value for {item['id']}")
            numeric_values.append(value)

        rule = instrument.get("completion_rule", {"min_answered_ratio": 1.0, "max_missing": 0})
        answered = sum(1 for item in items if responses.get(item["id"]) is not None)
        missing = len(items) - answered
        ratio = answered / len(items) if items else 0
        if missing > rule.get("max_missing", 0) or ratio < rule.get("min_answered_ratio", 1.0):
            raise ScoringError("Assessment is incomplete under the instrument completion rules.")

        traits = sorted({item["trait"] for item in items})
        trait_scores: dict[str, TraitScore] = {}
        for trait in traits:
            trait_items = [item for item in items if item["trait"] == trait]
            scored_values = []
            answered_count = 0
            for item in trait_items:
                raw = responses.get(item["id"])
                if raw is None:
                    continue
                answered_count += 1
                scored_values.append(_keyed_score(float(raw), item["keyed"], item["min_value"], item["max_value"]))
            if not scored_values:
                raise ScoringError(f"No responses for trait {trait}")
            raw_sum = float(sum(scored_values))
            mean = raw_sum / len(scored_values)
            min_possible = float(len(trait_items) * 1)
            max_possible = float(len(trait_items) * 5)
            # Min-max scaled display score. This is NOT a population percentile.
            scaled = ((raw_sum - min_possible) / (max_possible - min_possible)) * 100.0
            meta = TRAIT_META.get(trait, {"name": trait.replace("_", " ").title(), "short": trait})
            explanation = meta.get("high") if mean >= 3.25 else meta.get("low") if mean <= 2.75 else meta.get("short")
            trait_scores[trait] = TraitScore(
                trait=trait,
                name=meta.get("name", trait),
                raw_sum=round(raw_sum, 6),
                mean=round(mean, 6),
                scaled_0_100=round(scaled, 6),
                item_count=len(trait_items),
                answered_count=answered_count,
                missing_count=len(trait_items) - answered_count,
                min_possible=min_possible,
                max_possible=max_possible,
                explanation=explanation or meta.get("short", ""),
            )

        derived: dict[str, TraitScore] = {}
        if "emotional_stability" in trait_scores:
            es = trait_scores["emotional_stability"]
            # Inverse mean on the same 1-5 scale: N = 6 - ES for each keyed item,
            # which equals 6 - mean for the trait mean.
            n_mean = 6.0 - es.mean
            n_sum = n_mean * es.answered_count
            n_scaled = 100.0 - es.scaled_0_100
            n_meta = TRAIT_META["negative_emotionality"]
            derived["negative_emotionality"] = TraitScore(
                trait="negative_emotionality",
                name=n_meta["name"],
                raw_sum=round(n_sum, 6),
                mean=round(n_mean, 6),
                scaled_0_100=round(n_scaled, 6),
                item_count=es.item_count,
                answered_count=es.answered_count,
                missing_count=es.missing_count,
                min_possible=es.min_possible,
                max_possible=es.max_possible,
                explanation=n_meta["high"] if n_mean >= 3.25 else n_meta["low"] if n_mean <= 2.75 else n_meta["short"],
            )

        quality = _quality_indicators(numeric_values, missing / len(items) if items else 0)
        archetype = None
        secondary = None
        notes = [
            "Scaled 0–100 scores are min-max transformations of raw sums, not population percentiles.",
            "AI systems do not generate or modify these scores.",
        ]
        if instrument["framework"] == "big_five" and all(
            key in trait_scores for key in ("openness", "conscientiousness", "extraversion", "agreeableness")
        ):
            means = {key: trait_scores[key].mean for key in ("openness", "conscientiousness", "extraversion", "agreeableness")}
            archetype = match_archetypes(means)
            secondary_def = ARCHETYPES[archetype.secondary_slug] if archetype.secondary_slug else None
            if secondary_def:
                secondary = {
                    "slug": secondary_def["slug"],
                    "name": secondary_def["name"],
                    "tagline": secondary_def["tagline"],
                    "description": secondary_def["description"],
                }
            if archetype.mixed:
                notes.append(
                    "One or more mapped traits were near the midpoint, so this is a mixed profile. "
                    "The primary archetype is the nearest descriptive pattern, not a rigid category."
                )

        strengths, growth = _strengths_and_growth(trait_scores, instrument["framework"], archetype)

        canonical = json.dumps(
            {"slug": slug, "version": instrument["version"], "responses": {k: responses.get(k) for k in sorted(item_by_id)}},
            separators=(",", ":"),
            sort_keys=True,
        )
        response_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        return ScoringResult(
            instrument_slug=slug,
            instrument_version=instrument["version"],
            framework=instrument["framework"],
            trait_scores=trait_scores,
            derived_scores=derived,
            archetype=archetype,
            secondary_archetype=secondary,
            quality=quality,
            strengths=strengths,
            growth_areas=growth,
            response_hash=response_hash,
            notes=notes,
        )


def _keyed_score(value: float, keyed: str, min_value: float, max_value: float) -> float:
    if keyed == "+":
        return value
    if keyed == "-":
        return (max_value + min_value) - value
    raise ScoringError(f"Invalid keyed value: {keyed}")


def _quality_indicators(values: list[float], missing_ratio: float) -> QualityIndicators:
    flags: list[str] = []
    if not values:
        return QualityIndicators(missing_ratio, False, 0, 0.0, 0.0, ("no_responses",))
    max_run = 1
    run = 1
    for prev, current in zip(values, values[1:]):
        if current == prev:
            run += 1
            max_run = max(max_run, run)
        else:
            run = 1
    variance = statistics.pvariance(values) if len(values) > 1 else 0.0
    straightlining = max_run >= max(8, math.floor(len(values) * 0.4)) and variance < 0.15
    if straightlining:
        flags.append("straightlining")
    if missing_ratio > 0.05:
        flags.append("missing_responses")
    # Acquiescence: share of 4-5 endorsements before reverse scoring.
    acquiescence = sum(1 for value in values if value >= 4) / len(values)
    if acquiescence >= 0.85:
        flags.append("high_acquiescence")
    if variance < 0.05 and len(values) >= 10:
        flags.append("low_variance")
    return QualityIndicators(
        missing_ratio=round(missing_ratio, 6),
        straightlining=straightlining,
        max_run_length=max_run,
        response_variance=round(variance, 6),
        acquiescence_index=round(acquiescence, 6),
        flags=tuple(flags),
    )


def _strengths_and_growth(
    trait_scores: dict[str, TraitScore],
    framework: str,
    archetype: ArchetypeMatch | None,
) -> tuple[list[str], list[str]]:
    strengths: list[str] = []
    growth: list[str] = []
    if framework == "big_five":
        mapping = {
            "openness": ("Intellectual curiosity and idea generation.", "Grounding new ideas in a practical next step."),
            "conscientiousness": ("Reliability and follow-through.", "Leaving room for rest and revision."),
            "extraversion": ("Initiating contact and bringing energy to a room.", "Protecting quiet recovery time."),
            "agreeableness": ("Considering other people in the decision.", "Naming your own needs without apology."),
            "emotional_stability": ("Recovering from ordinary setbacks.", "Noticing stress earlier and asking for support."),
        }
        for trait, (high, low_growth) in mapping.items():
            score = trait_scores.get(trait)
            if not score:
                continue
            low_actions = {
                "openness": "Trying one unfamiliar idea in a low-stakes setting.",
                "conscientiousness": "Using a lighter planning habit rather than none.",
                "extraversion": "Initiating one small social contact on your own terms.",
                "agreeableness": "Practicing a generous interpretation before a hard conclusion.",
                "emotional_stability": "Building a small recovery ritual after stressful days.",
            }
            if score.mean >= 3.4:
                strengths.append(high)
            elif score.mean <= 2.6:
                growth.append(low_actions[trait])
            else:
                growth.append(low_growth)
    if archetype:
        arch = ARCHETYPES[archetype.slug]
        strengths.extend(arch["strengths"][:2])
        growth.extend(arch["growth_areas"][:2])
    # Deduplicate while preserving order
    def unique(items: list[str]) -> list[str]:
        seen: set[str] = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result[:6]

    return unique(strengths), unique(growth)
