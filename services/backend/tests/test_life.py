from tests.conftest import auth_header

from app.life.codes import CODE_BY_SLUG, slug_for_code
from app.life.decisions import score_matrix
from app.life.encyclopedia import encyclopedia_entry, list_encyclopedia
from app.life.finance import score_finance
from app.life.marriage import PREMARITAL_QUESTIONS, pairing_notes
from app.life.occupations import list_occupations
from app.life.safety import detect_abuse
from app.scoring.engine import ScoringEngine
from app.scoring.catalog import IPIP50_ITEMS


def test_encyclopedia_has_sixteen_times_sixty():
    profiles = list_encyclopedia()
    assert len(profiles) == 16
    for row in profiles:
        entry = encyclopedia_entry(row["slug"])
        assert len(entry["sections"]) == 60
        assert entry["preference_code"] == CODE_BY_SLUG[row["slug"]]["code"]
        assert len(entry["strengths_library"]) >= 20
        assert len(entry["growth_library"]) >= 20
        assert len(entry["blind_spots"]) >= 15
        assert "Myers-Briggs Type Indicator" in entry["disclaimer"]
        assert entry["free"] is True


def test_preference_code_for_strategist_pattern():
    engine = ScoringEngine()
    responses = {item["id"]: 5 if item["keyed"] == "+" else 1 for item in IPIP50_ITEMS}
    # Force OCEA high,high,high,low by using max extraversion/openness/conscientiousness and min agreeableness.
    for item in IPIP50_ITEMS:
        if item["trait"] == "agreeableness":
            responses[item["id"]] = 1 if item["keyed"] == "+" else 5
        elif item["trait"] in {"openness", "conscientiousness", "extraversion"}:
            responses[item["id"]] = 5 if item["keyed"] == "+" else 1
        else:
            responses[item["id"]] = 3
    result = engine.score("big-five", responses)
    assert result.archetype is not None
    payload = result.to_dict()
    assert payload["archetype"]["preference_code"] == CODE_BY_SLUG[result.archetype.slug]["code"]
    assert slug_for_code("INTJ") == "analyst"


def test_decision_matrix_is_transparent_and_user_weighted():
    scored = score_matrix(
        [{"id": "money", "weight": 10}, {"id": "joy", "weight": 0}],
        [
            {"id": "a", "title": "A", "ratings": {"money": 10, "joy": 0}},
            {"id": "b", "title": "B", "ratings": {"money": 1, "joy": 10}},
        ],
    )
    assert scored["leader"]["id"] == "a"
    assert "not scientifically" in scored["disclaimer"].lower()


def test_pairing_has_no_compatibility_percent():
    notes = pairing_notes("analyst", "collaborator")
    assert notes["compatibility_percent"] is None
    assert notes["verdict"] is None
    assert "abuse" in notes["safety"].lower()


def test_premarital_bank_has_one_hundred_fifty():
    assert len(PREMARITAL_QUESTIONS) == 150
    assert len({row["category"] for row in PREMARITAL_QUESTIONS}) == 15


def test_occupations_do_not_fabricate_wages():
    rows = list_occupations()
    assert len(rows) >= 60
    assert all(row["salary"] is None and row["outlook"] is None for row in rows)
    assert all("onetonline.org" in row["source_url"] for row in rows)


def test_finance_independent_of_personality():
    scored = score_finance({f"fin_{i:02d}": 4 for i in range(1, 13)})
    assert scored["not_inferred_from_personality"] is True
    assert "investment" in scored["disclaimer"].lower()


def test_abuse_heuristic():
    assert detect_abuse("He hits me when I disagree") is True
    assert detect_abuse("We argue about chores") is False


def test_life_api_encyclopedia_and_matrix(client):
    encyclopedia = client.get("/api/v1/life/encyclopedia")
    assert encyclopedia.status_code == 200
    assert encyclopedia.json()["free"] is True
    headers = auth_header(client)
    matrix = client.post(
        "/api/v1/life/decisions/matrix",
        headers=headers,
        json={
            "title": "Test",
            "criteria": [{"id": "a", "weight": 1}],
            "options": [{"id": "x", "title": "X", "ratings": {"a": 8}}],
        },
    )
    assert matrix.status_code == 200
    assert matrix.json()["leader"]["id"] == "x"
    pairing = client.get("/api/v1/life/marriage/pairing/analyst/mentor")
    assert pairing.status_code == 200
    assert pairing.json()["compatibility_percent"] is None
