from app.scoring.catalog import IPIP50_ITEMS, instrument_by_slug
from app.scoring.engine import ScoringEngine, ScoringError


def _max_profile() -> dict[str, int]:
    return {item["id"]: 5 if item["keyed"] == "+" else 1 for item in IPIP50_ITEMS}


def _min_profile() -> dict[str, int]:
    return {item["id"]: 1 if item["keyed"] == "+" else 5 for item in IPIP50_ITEMS}


def test_reverse_scoring_maximum():
    engine = ScoringEngine()
    result = engine.score("big-five", _max_profile())
    for trait, score in result.trait_scores.items():
        assert score.raw_sum == 50, trait
        assert score.mean == 5
        assert score.scaled_0_100 == 100


def test_reverse_scoring_minimum():
    engine = ScoringEngine()
    result = engine.score("big-five", _min_profile())
    for score in result.trait_scores.values():
        assert score.raw_sum == 10
        assert score.mean == 1
        assert score.scaled_0_100 == 0


def test_all_neutral_is_midpoint():
    engine = ScoringEngine()
    responses = {item["id"]: 3 for item in IPIP50_ITEMS}
    result = engine.score("big-five", responses)
    for score in result.trait_scores.values():
        assert score.raw_sum == 30
        assert score.mean == 3
        assert score.scaled_0_100 == 50
    assert result.archetype is not None
    assert result.archetype.mixed is True


def test_determinism_identical_hash():
    engine = ScoringEngine()
    responses = {item["id"]: ((i * 3) % 5) + 1 for i, item in enumerate(IPIP50_ITEMS)}
    a = engine.score("big-five", responses)
    b = engine.score("big-five", responses)
    assert a.response_hash == b.response_hash
    assert a.to_dict()["trait_scores"] == b.to_dict()["trait_scores"]
    assert a.archetype.slug == b.archetype.slug


def test_negative_emotionality_is_inverse_of_stability():
    engine = ScoringEngine()
    result = engine.score("big-five", _max_profile())
    es = result.trait_scores["emotional_stability"]
    n = result.derived_scores["negative_emotionality"]
    assert abs((es.mean + n.mean) - 6) < 1e-9
    assert abs((es.scaled_0_100 + n.scaled_0_100) - 100) < 1e-6


def test_unknown_item_rejected():
    engine = ScoringEngine()
    responses = _max_profile()
    responses["not_an_item"] = 3
    try:
        engine.score("big-five", responses)
        raise AssertionError("expected ScoringError")
    except ScoringError:
        pass


def test_out_of_range_rejected():
    engine = ScoringEngine()
    responses = _max_profile()
    first = IPIP50_ITEMS[0]["id"]
    responses[first] = 9
    try:
        engine.score("big-five", responses)
        raise AssertionError("expected ScoringError")
    except ScoringError:
        pass


def test_archetype_strategist_pattern():
    # High O, C, E, Low A
    engine = ScoringEngine()
    responses = {}
    for item in IPIP50_ITEMS:
        if item["trait"] == "agreeableness":
            responses[item["id"]] = 1 if item["keyed"] == "+" else 5
        elif item["trait"] in {"openness", "conscientiousness", "extraversion"}:
            responses[item["id"]] = 5 if item["keyed"] == "+" else 1
        else:
            responses[item["id"]] = 3
    result = engine.score("big-five", responses)
    assert result.archetype.slug == "strategist"
    assert result.archetype.pattern == "HHHL"


def test_quick_discovery_scores():
    instrument = instrument_by_slug("quick-discovery")
    responses = {item["id"]: 4 for item in instrument["items"]}
    result = ScoringEngine().score("quick-discovery", responses)
    assert "extraversion" in result.trait_scores
    assert result.instrument_slug == "quick-discovery"


def test_missing_responses_blocked_when_required():
    engine = ScoringEngine()
    responses = _max_profile()
    del responses[IPIP50_ITEMS[0]["id"]]
    try:
        engine.score("quick-discovery", {item["id"]: 3 for item in instrument_by_slug("quick-discovery")["items"][:-1]})
        raise AssertionError("expected ScoringError")
    except ScoringError:
        pass
    # big-five allows up to 5 missing
    engine.score("big-five", responses)
