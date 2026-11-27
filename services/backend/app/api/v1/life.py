from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.life.blueprint import build_blueprint
from app.life.codes import CODE_BY_SLUG, DISCLAIMER
from app.life.decisions import DEFAULT_CRITERIA, score_matrix
from app.life.encyclopedia import encyclopedia_entry, list_encyclopedia
from app.life.finance import QUESTIONS as FINANCE_QUESTIONS, score_finance
from app.life.insights import who_you_are
from app.life.marriage import PREMARITAL_CATEGORIES, PREMARITAL_QUESTIONS, marriage_prep_report, pairing_notes
from app.life.occupations import explore_for_interests, get_occupation, list_occupations
from app.life.parenting import PROGRAMS as PARENT_PROGRAMS, parenting_guide
from app.life.values import VALUE_KEYS, rank_values
from app.models import AssessmentResult, DecisionJournal, GuidanceRecord, User, new_id, utcnow
from app.reports import render_pdf

router = APIRouter(prefix="/life", tags=["life-guidance"])


def _latest_big_five(db: Session, user: User) -> AssessmentResult | None:
    return (
        db.query(AssessmentResult)
        .filter(
            AssessmentResult.user_id == user.id,
            AssessmentResult.instrument_slug.in_(
                ["big-five", "quick-discovery", "quick-discovery-plain", "comprehensive", "advanced"]
            ),
        )
        .order_by(AssessmentResult.created_at.desc())
        .first()
    )


@router.get("/encyclopedia")
def encyclopedia_index():
    return {"disclaimer": DISCLAIMER, "free": True, "profiles": list_encyclopedia()}


@router.get("/encyclopedia/{slug}")
def encyclopedia_profile(slug: str, section: int | None = None):
    try:
        entry = encyclopedia_entry(slug)
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown profile")
    if section:
        found = next((item for item in entry["sections"] if item["id"] == section), None)
        if not found:
            raise HTTPException(status_code=404, detail="Unknown section")
        return {"profile": {k: entry[k] for k in ("slug", "preference_code", "title", "disclaimer")}, "section": found}
    return entry


@router.get("/who-you-are")
def who(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest = _latest_big_five(db, user)
    if not latest:
        raise HTTPException(status_code=404, detail="Complete a Big Five assessment first")
    extras = {}
    values_row = (
        db.query(GuidanceRecord)
        .filter(GuidanceRecord.user_id == user.id, GuidanceRecord.kind == "values")
        .order_by(GuidanceRecord.created_at.desc())
        .first()
    )
    if values_row:
        extras["values"] = values_row.payload
    return who_you_are(latest.payload or {}, extras)


class ValuesIn(BaseModel):
    rankings: dict[str, int]
    skip: list[str] = Field(default_factory=list)


@router.get("/values/catalog")
def values_catalog():
    return {"keys": VALUE_KEYS, "disclaimer": "Self-report only. Nothing is inferred from personality type."}


@router.post("/values")
def save_values(payload: ValuesIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ranked = rank_values(payload.rankings, payload.skip)
    row = GuidanceRecord(id=new_id(), user_id=user.id, kind="values", payload=ranked)
    db.add(row)
    db.commit()
    return ranked


class FinanceIn(BaseModel):
    responses: dict[str, int]


@router.get("/finance/questions")
def finance_questions():
    return {"questions": FINANCE_QUESTIONS, "not_inferred_from_personality": True}


@router.post("/finance")
def save_finance(payload: FinanceIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scored = score_finance(payload.responses)
    db.add(GuidanceRecord(id=new_id(), user_id=user.id, kind="finance", payload=scored))
    db.commit()
    return scored


@router.get("/occupations")
def occupations(riasec: str | None = None, q: str | None = None):
    return {"count": len(list_occupations()), "items": list_occupations(riasec, q)}


@router.get("/occupations/{slug}")
def occupation(slug: str):
    row = get_occupation(slug)
    if not row:
        raise HTTPException(status_code=404, detail="Unknown occupation")
    return row


class CareerExploreIn(BaseModel):
    riasec: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    education: str | None = None
    constraints: dict = Field(default_factory=dict)


@router.post("/career/explore")
def career_explore(payload: CareerExploreIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = explore_for_interests(payload.riasec, payload.skills)
    result["constraints"] = payload.constraints
    result["education"] = payload.education
    result["personality_not_used_to_exclude"] = True
    db.add(GuidanceRecord(id=new_id(), user_id=user.id, kind="career_explore", payload={"riasec": payload.riasec, "skills": payload.skills}))
    db.commit()
    return result


@router.get("/marriage/questions")
def marriage_questions(category: str | None = None):
    items = PREMARITAL_QUESTIONS
    if category:
        items = [row for row in items if row["category"] == category]
    return {"count": len(items), "categories": PREMARITAL_CATEGORIES, "items": items, "not_a_test": True}


@router.get("/marriage/pairing/{slug_a}/{slug_b}")
def marriage_pairing(slug_a: str, slug_b: str):
    if slug_a not in CODE_BY_SLUG or slug_b not in CODE_BY_SLUG:
        raise HTTPException(status_code=404, detail="Unknown profile")
    return pairing_notes(slug_a, slug_b)


class MarriageReportIn(BaseModel):
    partner_slug: str | None = None
    answers: list[dict] = Field(default_factory=list)


@router.post("/marriage/report")
def marriage_report(payload: MarriageReportIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest = _latest_big_five(db, user)
    if not latest or not (latest.payload or {}).get("archetype"):
        raise HTTPException(status_code=404, detail="Complete a Big Five assessment first")
    slug = latest.payload["archetype"]["slug"]
    partner = {"slug": payload.partner_slug} if payload.partner_slug else None
    report = marriage_prep_report({"slug": slug, "email": user.email}, partner, payload.answers)
    db.add(GuidanceRecord(id=new_id(), user_id=user.id, kind="marriage_report", payload=report))
    db.commit()
    return report


@router.get("/parenting/{slug}")
def parenting(slug: str):
    if slug not in CODE_BY_SLUG:
        raise HTTPException(status_code=404, detail="Unknown profile")
    return {"programs": PARENT_PROGRAMS, **parenting_guide(slug)}


class MatrixIn(BaseModel):
    title: str = "Decision"
    criteria: list[dict]
    options: list[dict]


@router.post("/decisions/matrix")
def decisions_matrix(payload: MatrixIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        scored = score_matrix(payload.criteria, payload.options)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    scored["title"] = payload.title
    return {"criteria_catalog": DEFAULT_CRITERIA, **scored}


class JournalIn(BaseModel):
    title: str
    decision: str = ""
    alternatives: list = Field(default_factory=list)
    assumptions: str = ""
    expected_outcomes: str = ""
    chosen_action: str = ""
    follow_up_date: str = ""
    actual_outcomes: str = ""
    lessons: str = ""
    matrix: dict = Field(default_factory=dict)


@router.get("/decisions")
def list_decisions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(DecisionJournal).filter(DecisionJournal.user_id == user.id).order_by(DecisionJournal.created_at.desc()).all()
    return [
        {
            "id": row.id,
            "title": row.title,
            "decision": row.decision,
            "chosen_action": row.chosen_action,
            "follow_up_date": row.follow_up_date,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]


@router.post("/decisions", status_code=201)
def create_decision(payload: JournalIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = DecisionJournal(id=new_id(), user_id=user.id, **payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "title": row.title}


@router.get("/decisions/{decision_id}")
def get_decision(decision_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.get(DecisionJournal, decision_id)
    if not row or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": row.id,
        "title": row.title,
        "decision": row.decision,
        "alternatives": row.alternatives,
        "assumptions": row.assumptions,
        "expected_outcomes": row.expected_outcomes,
        "chosen_action": row.chosen_action,
        "follow_up_date": row.follow_up_date,
        "actual_outcomes": row.actual_outcomes,
        "lessons": row.lessons,
        "matrix": row.matrix,
    }


class BlueprintIn(BaseModel):
    exclude: list[str] = Field(default_factory=list)
    riasec: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    values: dict | None = None
    goals: list = Field(default_factory=list)
    finance: dict | None = None
    marriage: dict | None = None
    parenting: dict | None = None
    mission: str | None = None


@router.post("/blueprint")
def create_blueprint(payload: BlueprintIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest = _latest_big_five(db, user)
    if not latest:
        raise HTTPException(status_code=404, detail="Complete a Big Five assessment first")
    extras = payload.model_dump()
    values_row = (
        db.query(GuidanceRecord)
        .filter(GuidanceRecord.user_id == user.id, GuidanceRecord.kind == "values")
        .order_by(GuidanceRecord.created_at.desc())
        .first()
    )
    finance_row = (
        db.query(GuidanceRecord)
        .filter(GuidanceRecord.user_id == user.id, GuidanceRecord.kind == "finance")
        .order_by(GuidanceRecord.created_at.desc())
        .first()
    )
    if values_row and not extras.get("values"):
        extras["values"] = values_row.payload
    if finance_row and not extras.get("finance"):
        extras["finance"] = finance_row.payload
    blueprint = build_blueprint(latest.payload or {}, extras, payload.exclude)
    row = GuidanceRecord(id=new_id(), user_id=user.id, kind="blueprint", payload=blueprint)
    db.add(row)
    db.commit()
    return {"id": row.id, **blueprint}


@router.get("/blueprint/{record_id}/pdf")
def blueprint_pdf(record_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from fastapi import Response

    row = db.get(GuidanceRecord, record_id)
    if not row or row.user_id != user.id or row.kind != "blueprint":
        raise HTTPException(status_code=404, detail="Not found")
    pdf = render_pdf(
        {
            "title": row.payload.get("title", "My Life Blueprint"),
            "archetype": {"name": row.payload.get("title"), "description": str(row.payload.get("disclaimer", ""))},
            "methodology": "Assembled from stored assessments and user-provided life-guidance inputs. Missing sections were omitted on purpose.",
            "limitations": row.payload.get("disclaimer"),
            "disclaimer": DISCLAIMER,
            "traits": {},
            "who": row.payload.get("who_you_are"),
            "sections": row.payload.get("sections"),
        }
    )
    return Response(content=pdf, media_type="application/pdf")


@router.get("/centers")
def centers():
    return {
        "centers": [
            {"slug": "self", "href": "/app/encyclopedia", "name": "Self Intelligence"},
            {"slug": "career", "href": "/app/guidance/career", "name": "Career Intelligence"},
            {"slug": "marriage", "href": "/app/guidance/marriage", "name": "Marriage Intelligence"},
            {"slug": "family", "href": "/app/guidance/family", "name": "Family Intelligence"},
            {"slug": "finance", "href": "/app/guidance/money", "name": "Financial Intelligence"},
            {"slug": "leadership", "href": "/app/leadership", "name": "Leadership Intelligence"},
            {"slug": "decisions", "href": "/app/guidance/decisions", "name": "Life Decision Intelligence"},
            {"slug": "growth", "href": "/app/growth", "name": "Personal Growth"},
        ]
    }
