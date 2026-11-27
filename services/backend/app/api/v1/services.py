from __future__ import annotations

import secrets
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.coaching import coach_reply
from app.config import get_settings
from app.content import CAREERS, HELP_ARTICLES, LEGAL_PAGES, PROGRAMS, career_by_slug, daily_insight, program_by_slug
from app.database import get_db
from app.deps import get_current_user, get_optional_user, require_roles
from app.models import (
    AccountDeletionRequest,
    AIUsage,
    AssessmentResponse,
    AssessmentResult,
    AssessmentSession,
    AuditEvent,
    ConsentRecord,
    Conversation,
    DataExportRequest,
    DevelopmentEnrollment,
    DevelopmentProgress,
    Entitlement,
    FeatureFlag,
    Feedback,
    Goal,
    Habit,
    HabitLog,
    JournalEntry,
    Membership,
    Message,
    Notification,
    Organization,
    Referral,
    RelationshipInvitation,
    ReportRecord,
    Subscription,
    User,
    UserPreference,
    UserProfile,
    utcnow,
)
from app.reports import build_report_payload, render_pdf
from app.life.codes import CODE_BY_SLUG
from app.scoring.archetypes import ARCHETYPES
from app.scoring.engine import ScoringEngine, ScoringError

router = APIRouter()
engine = ScoringEngine()


def _is_premium(db: Session, user: User) -> bool:
    if user.role in {"admin", "superadmin", "staff"}:
        return True
    sub = db.get(Subscription, user.id)
    if sub and sub.plan in {"premium", "staff", "enterprise"} and sub.status == "active":
        return True
    ent = (
        db.query(Entitlement)
        .filter(Entitlement.user_id == user.id, Entitlement.code == "premium", Entitlement.active.is_(True))
        .first()
    )
    return bool(ent)


def _require_instrument_access(db: Session, user: User, slug: str) -> dict:
    instrument = engine.get_instrument(slug)
    if instrument["is_free"] or _is_premium(db, user):
        return instrument
    raise HTTPException(status_code=402, detail="Premium entitlement required for this assessment")


class ProfileIn(BaseModel):
    display_name: str | None = None
    headline: str | None = None
    bio: str | None = None
    country: str | None = None
    timezone: str | None = None
    occupation: str | None = None
    share_profile_public: bool | None = None


class PreferencesIn(BaseModel):
    theme: str | None = None
    reduced_motion: bool | None = None
    text_scale: str | None = None
    email_notifications: bool | None = None
    daily_insights: bool | None = None
    coaching_reminders: bool | None = None
    journal_ai_analysis: bool | None = None
    coach_may_use_assessments: bool | None = None
    coach_may_use_goals: bool | None = None
    coach_may_use_journal: bool | None = None
    locale: str | None = None


class ConsentIn(BaseModel):
    kind: str
    granted: bool = True


class ResponseIn(BaseModel):
    item_id: str
    value: int = Field(ge=1, le=5)


class BulkResponsesIn(BaseModel):
    responses: list[ResponseIn]
    complete: bool = False


class CoachIn(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: str | None = None


class JournalIn(BaseModel):
    title: str = ""
    body: str
    entry_type: str = "reflection"
    mood: int | None = Field(default=None, ge=1, le=5)
    tags: list[str] = []
    allow_ai: bool = False


class GoalIn(BaseModel):
    title: str
    description: str = ""
    category: str = "personal"
    target_date: str | None = None
    progress: int | None = Field(default=None, ge=0, le=100)


class HabitIn(BaseModel):
    name: str
    cadence: str = "daily"
    reminder: str | None = None


class InviteIn(BaseModel):
    email: EmailStr
    relationship_type: str = "partner"


class OrgIn(BaseModel):
    name: str
    slug: str


class FeedbackIn(BaseModel):
    category: str = "general"
    message: str


# --- Users ---
@router.get("/users/me")
def me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.get(UserProfile, user.id)
    prefs = db.get(UserPreference, user.id)
    sub = db.get(Subscription, user.id)
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "locale": user.locale,
        "email_verified": user.email_verified,
        "profile": {
            "display_name": profile.display_name if profile else "",
            "headline": profile.headline if profile else "",
            "bio": profile.bio if profile else "",
            "country": profile.country if profile else "",
            "timezone": profile.timezone if profile else "UTC",
            "occupation": profile.occupation if profile else "",
            "share_profile_public": profile.share_profile_public if profile else False,
        },
        "preferences": {
            "theme": prefs.theme if prefs else "system",
            "reduced_motion": prefs.reduced_motion if prefs else False,
            "text_scale": prefs.text_scale if prefs else "medium",
            "email_notifications": prefs.email_notifications if prefs else True,
            "daily_insights": prefs.daily_insights if prefs else True,
            "journal_ai_analysis": prefs.journal_ai_analysis if prefs else False,
            "coach_may_use_assessments": prefs.coach_may_use_assessments if prefs else True,
            "coach_may_use_goals": prefs.coach_may_use_goals if prefs else True,
            "coach_may_use_journal": prefs.coach_may_use_journal if prefs else False,
        },
        "subscription": {"plan": sub.plan if sub else "free", "status": sub.status if sub else "active"},
        "premium": _is_premium(db, user),
    }


@router.patch("/users/me/profile")
def update_profile(payload: ProfileIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.get(UserProfile, user.id)
    if not profile:
        profile = UserProfile(user_id=user.id)
        db.add(profile)
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(profile, key, value)
    db.commit()
    return {"ok": True}


@router.patch("/users/me/preferences")
def update_prefs(payload: PreferencesIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    prefs = db.get(UserPreference, user.id) or UserPreference(user_id=user.id)
    db.add(prefs)
    data = payload.model_dump(exclude_none=True)
    locale = data.pop("locale", None)
    for key, value in data.items():
        setattr(prefs, key, value)
    if locale:
        user.locale = locale
    db.commit()
    return {"ok": True}


@router.post("/users/me/consent")
def consent(payload: ConsentIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = ConsentRecord(user_id=user.id, kind=payload.kind, granted=payload.granted, version="1.0")
    if not payload.granted:
        record.revoked_at = utcnow()
    db.add(record)
    db.commit()
    return {"ok": True, "id": record.id}


@router.get("/users/me/consent")
def list_consent(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(ConsentRecord).filter(ConsentRecord.user_id == user.id).order_by(ConsentRecord.created_at.desc()).all()
    return [
        {"id": r.id, "kind": r.kind, "granted": r.granted, "version": r.version, "created_at": r.created_at.isoformat()}
        for r in rows
    ]


# --- Assessments ---
@router.get("/assessments")
def list_assessments(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    premium = _is_premium(db, user)
    items = []
    for instrument in engine.list_instruments():
        items.append({**instrument, "locked": (not instrument["is_free"]) and not premium})
    return items


@router.get("/assessments/{slug}")
def get_assessment(slug: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    instrument = _require_instrument_access(db, user, slug)
    return engine.public_instrument(instrument, include_items=True)


@router.post("/assessments/{slug}/sessions", status_code=201)
def start_session(slug: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    instrument = _require_instrument_access(db, user, slug)
    existing = (
        db.query(AssessmentSession)
        .filter(
            AssessmentSession.user_id == user.id,
            AssessmentSession.instrument_slug == slug,
            AssessmentSession.status == "in_progress",
        )
        .first()
    )
    if existing:
        return _session_out(existing, instrument, db)
    session = AssessmentSession(
        user_id=user.id,
        instrument_slug=slug,
        instrument_version=instrument["version"],
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return _session_out(session, instrument, db)


@router.get("/sessions/{session_id}")
def get_session(session_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = _owned_session(db, user, session_id)
    instrument = engine.get_instrument(session.instrument_slug)
    return _session_out(session, instrument, db)


@router.post("/sessions/{session_id}/responses")
def save_responses(session_id: str, payload: BulkResponsesIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = _owned_session(db, user, session_id)
    if session.status != "in_progress":
        raise HTTPException(status_code=409, detail="Session is not in progress")
    instrument = engine.get_instrument(session.instrument_slug)
    valid_ids = {item["id"] for item in instrument["items"]}
    for item in payload.responses:
        if item.item_id not in valid_ids:
            raise HTTPException(status_code=400, detail=f"Unknown item {item.item_id}")
        row = (
            db.query(AssessmentResponse)
            .filter(AssessmentResponse.session_id == session.id, AssessmentResponse.item_id == item.item_id)
            .first()
        )
        if row:
            row.value = item.value
            row.answered_at = utcnow()
        else:
            db.add(AssessmentResponse(session_id=session.id, item_id=item.item_id, value=item.value))
    answered = db.query(AssessmentResponse).filter(AssessmentResponse.session_id == session.id).count()
    session.current_index = min(answered, instrument["item_count"] - 1)
    db.commit()
    if payload.complete:
        return complete_session(session_id, user, db)
    return _session_out(session, instrument, db)


@router.post("/sessions/{session_id}/complete")
def complete_session(session_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = _owned_session(db, user, session_id)
    instrument = engine.get_instrument(session.instrument_slug)
    rows = db.query(AssessmentResponse).filter(AssessmentResponse.session_id == session.id).all()
    responses = {row.item_id: row.value for row in rows}
    try:
        scored = engine.score(session.instrument_slug, responses, session.instrument_version)
    except ScoringError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    result = AssessmentResult(
        user_id=user.id,
        session_id=session.id,
        instrument_slug=session.instrument_slug,
        instrument_version=session.instrument_version,
        scoring_algorithm=scored.scoring_algorithm,
        response_hash=scored.response_hash,
        payload=scored.to_dict(),
    )
    db.add(result)
    db.flush()
    session.status = "completed"
    session.completed_at = utcnow()
    session.result_id = result.id
    db.add(AuditEvent(actor_id=user.id, action="assessment.complete", resource="result", resource_id=result.id))
    db.commit()
    db.refresh(result)
    return {"session": _session_out(session, instrument, db), "result": _result_out(result)}


def _owned_session(db: Session, user: User, session_id: str) -> AssessmentSession:
    session = db.get(AssessmentSession, session_id)
    if not session or session.user_id != user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


def _session_out(session: AssessmentSession, instrument: dict, db: Session) -> dict:
    rows = db.query(AssessmentResponse).filter(AssessmentResponse.session_id == session.id).all()
    return {
        "id": session.id,
        "instrument_slug": session.instrument_slug,
        "instrument_version": session.instrument_version,
        "status": session.status,
        "current_index": session.current_index,
        "answered": len(rows),
        "item_count": instrument["item_count"],
        "responses": {row.item_id: row.value for row in rows},
        "result_id": session.result_id,
        "started_at": session.started_at.isoformat() if session.started_at else None,
        "completed_at": session.completed_at.isoformat() if session.completed_at else None,
    }


def _result_out(result: AssessmentResult) -> dict:
    return {
        "id": result.id,
        "session_id": result.session_id,
        "instrument_slug": result.instrument_slug,
        "instrument_version": result.instrument_version,
        "scoring_algorithm": result.scoring_algorithm,
        "response_hash": result.response_hash,
        "created_at": result.created_at.isoformat() if result.created_at else None,
        "payload": result.payload,
    }


@router.get("/results")
def list_results(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(AssessmentResult)
        .filter(AssessmentResult.user_id == user.id)
        .order_by(AssessmentResult.created_at.desc())
        .all()
    )
    return [_result_out(row) for row in rows]


@router.get("/results/{result_id}")
def get_result(result_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = db.get(AssessmentResult, result_id)
    if not result or result.user_id != user.id:
        raise HTTPException(status_code=404, detail="Result not found")
    return _result_out(result)


@router.get("/personality/dashboard")
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest = (
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
    history = (
        db.query(AssessmentResult)
        .filter(AssessmentResult.user_id == user.id)
        .order_by(AssessmentResult.created_at.desc())
        .limit(20)
        .all()
    )
    insight = daily_insight(abs(hash(user.id + date.today().isoformat())) % 1000)
    return {
        "has_profile": bool(latest),
        "latest": _result_out(latest) if latest else None,
        "history": [
            {
                "id": row.id,
                "instrument_slug": row.instrument_slug,
                "created_at": row.created_at.isoformat(),
                "archetype": (row.payload or {}).get("archetype", {}).get("name") if row.payload else None,
            }
            for row in history
        ],
        "insight": insight,
        "premium": _is_premium(db, user),
    }


@router.get("/personality/archetypes")
def list_archetypes():
    return [
        {
            "slug": item["slug"],
            "name": item["name"],
            "tagline": item["tagline"],
            "palette": item["palette"],
            "symbol": item["symbol"],
            "description": item["description"],
            "preference_code": CODE_BY_SLUG[item["slug"]]["code"],
            "preference_title": CODE_BY_SLUG[item["slug"]]["title"],
        }
        for item in ARCHETYPES.values()
    ]


@router.get("/personality/archetypes/{slug}")
def get_archetype(slug: str):
    item = ARCHETYPES.get(slug)
    if not item:
        raise HTTPException(status_code=404, detail="Unknown archetype")
    return item


# --- Coach ---
def _coach_context(db: Session, user: User) -> dict:
    prefs = db.get(UserPreference, user.id)
    latest = (
        db.query(AssessmentResult)
        .filter(AssessmentResult.user_id == user.id)
        .order_by(AssessmentResult.created_at.desc())
        .first()
    )
    goals = db.query(Goal).filter(Goal.user_id == user.id, Goal.status == "active").all()
    context: dict = {"goals": [], "trait_summaries": [], "archetype": None}
    if prefs and prefs.coach_may_use_assessments and latest and latest.payload:
        payload = latest.payload
        context["archetype"] = payload.get("archetype")
        context["trait_summaries"] = [
            f"{score['name']}: mean {score['mean']}"
            for score in (payload.get("trait_scores") or {}).values()
        ]
        context["exercises"] = (payload.get("archetype") or {}).get("exercises") or []
        context["growth_areas"] = payload.get("growth_areas") or []
        context["measured_only"] = True
    if prefs and prefs.coach_may_use_goals:
        context["goals"] = [{"title": g.title, "progress": g.progress} for g in goals]
    if prefs and prefs.coach_may_use_journal:
        context["journal_authorized"] = True
    else:
        context["journal_authorized"] = False
    return context


@router.post("/coach/conversations", status_code=201)
def new_conversation(payload: CoachIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _coach_turn(payload, user, db)


@router.get("/coach/conversations")
def list_conversations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Conversation).filter(Conversation.user_id == user.id).order_by(Conversation.updated_at.desc()).all()
    return [{"id": c.id, "title": c.title, "agent": c.agent, "updated_at": c.updated_at.isoformat() if c.updated_at else None} for c in rows]


@router.get("/coach/conversations/{conversation_id}")
def get_conversation(conversation_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    convo = db.get(Conversation, conversation_id)
    if not convo or convo.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = db.query(Message).filter(Message.conversation_id == convo.id).order_by(Message.created_at.asc()).all()
    return {
        "id": convo.id,
        "title": convo.title,
        "agent": convo.agent,
        "messages": [
            {"id": m.id, "role": m.role, "content": m.content, "grounding": m.grounding, "safety": m.safety, "created_at": m.created_at.isoformat()}
            for m in messages
        ],
    }


@router.post("/coach/conversations/{conversation_id}/messages")
def continue_conversation(conversation_id: str, payload: CoachIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    payload.conversation_id = conversation_id
    return _coach_turn(payload, user, db)


def _coach_turn(payload: CoachIn, user: User, db: Session) -> dict:
    settings = get_settings()
    day = date.today().isoformat()
    usage = db.query(AIUsage).filter(AIUsage.user_id == user.id, AIUsage.day == day).first()
    if not usage:
        usage = AIUsage(user_id=user.id, day=day)
        db.add(usage)
        db.flush()
    limit = settings.ai_daily_message_limit_premium if _is_premium(db, user) else settings.ai_daily_message_limit_free
    if usage.messages >= limit:
        raise HTTPException(status_code=429, detail="Daily coaching limit reached")
    convo = None
    if payload.conversation_id:
        convo = db.get(Conversation, payload.conversation_id)
        if not convo or convo.user_id != user.id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    context = _coach_context(db, user)
    result = coach_reply(payload.message, context)
    if not convo:
        title = payload.message.strip()[:80] or "Coaching conversation"
        convo = Conversation(user_id=user.id, title=title, agent=result.get("agent", "insight"))
        db.add(convo)
        db.flush()
    db.add(Message(conversation_id=convo.id, role="user", content=payload.message))
    db.add(
        Message(
            conversation_id=convo.id,
            role="assistant",
            content=result["content"],
            grounding=result.get("grounding"),
            safety=result.get("safety"),
        )
    )
    usage.messages += 1
    convo.agent = result.get("agent", convo.agent)
    db.commit()
    return {"conversation_id": convo.id, **result, "usage": {"messages_today": usage.messages, "limit": limit}}


# --- Growth / journal / habits ---
@router.get("/growth/programs")
def list_programs():
    return PROGRAMS


@router.get("/growth/programs/{slug}")
def get_program(slug: str):
    program = program_by_slug(slug)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program


@router.post("/growth/programs/{slug}/enroll", status_code=201)
def enroll(slug: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not program_by_slug(slug):
        raise HTTPException(status_code=404, detail="Program not found")
    row = DevelopmentEnrollment(user_id=user.id, program_slug=slug)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "program_slug": slug, "current_day": 1, "status": row.status}


@router.get("/growth/enrollments")
def enrollments(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(DevelopmentEnrollment).filter(DevelopmentEnrollment.user_id == user.id).all()
    return [{"id": r.id, "program_slug": r.program_slug, "status": r.status, "current_day": r.current_day} for r in rows]


@router.post("/growth/enrollments/{enrollment_id}/days/{day}")
def complete_day(enrollment_id: str, day: int, reflection: dict | None = None, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    enrollment = db.get(DevelopmentEnrollment, enrollment_id)
    if not enrollment or enrollment.user_id != user.id:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    text = (reflection or {}).get("reflection", "")
    row = DevelopmentProgress(enrollment_id=enrollment.id, day=day, completed=True, reflection=text, completed_at=utcnow())
    db.add(row)
    enrollment.current_day = max(enrollment.current_day, day + 1)
    db.commit()
    return {"ok": True, "current_day": enrollment.current_day}


@router.get("/journals")
def list_journals(q: str | None = None, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(JournalEntry).filter(JournalEntry.user_id == user.id)
    if q:
        like = f"%{q}%"
        query = query.filter(JournalEntry.body.like(like) | JournalEntry.title.like(like))
    rows = query.order_by(JournalEntry.created_at.desc()).all()
    return [_journal_out(r) for r in rows]


@router.post("/journals", status_code=201)
def create_journal(payload: JournalIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = JournalEntry(user_id=user.id, **payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return _journal_out(row)


@router.delete("/journals/{entry_id}")
def delete_journal(entry_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.get(JournalEntry, entry_id)
    if not row or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(row)
    db.commit()
    return {"ok": True}


def _journal_out(row: JournalEntry) -> dict:
    return {
        "id": row.id,
        "title": row.title,
        "body": row.body,
        "entry_type": row.entry_type,
        "mood": row.mood,
        "tags": row.tags,
        "allow_ai": row.allow_ai,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


@router.get("/goals")
def list_goals(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Goal).filter(Goal.user_id == user.id).all()
    return [{"id": g.id, "title": g.title, "description": g.description, "category": g.category, "status": g.status, "progress": g.progress, "target_date": g.target_date} for g in rows]


@router.post("/goals", status_code=201)
def create_goal(payload: GoalIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = Goal(user_id=user.id, title=payload.title, description=payload.description, category=payload.category, target_date=payload.target_date, progress=payload.progress or 0)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id}


@router.patch("/goals/{goal_id}")
def update_goal(goal_id: str, payload: GoalIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.get(Goal, goal_id)
    if not row or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Goal not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(row, key, value)
    db.commit()
    return {"ok": True}


@router.get("/habits")
def list_habits(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Habit).filter(Habit.user_id == user.id).all()
    today = date.today().isoformat()
    out = []
    for habit in rows:
        log = db.query(HabitLog).filter(HabitLog.habit_id == habit.id, HabitLog.day == today).first()
        out.append({"id": habit.id, "name": habit.name, "cadence": habit.cadence, "reminder": habit.reminder, "completed_today": bool(log and log.completed)})
    return out


@router.post("/habits", status_code=201)
def create_habit(payload: HabitIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = Habit(user_id=user.id, name=payload.name, cadence=payload.cadence, reminder=payload.reminder)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id}


@router.post("/habits/{habit_id}/log")
def log_habit(habit_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    habit = db.get(Habit, habit_id)
    if not habit or habit.user_id != user.id:
        raise HTTPException(status_code=404, detail="Habit not found")
    today = date.today().isoformat()
    row = db.query(HabitLog).filter(HabitLog.habit_id == habit.id, HabitLog.day == today).first()
    if not row:
        row = HabitLog(habit_id=habit.id, user_id=user.id, day=today, completed=True)
        db.add(row)
    else:
        row.completed = not row.completed
    db.commit()
    return {"completed": row.completed}


# --- Career / leadership / relationships ---
@router.get("/careers")
def list_careers():
    return CAREERS


@router.get("/careers/{slug}")
def get_career(slug: str):
    item = career_by_slug(slug)
    if not item:
        raise HTTPException(status_code=404, detail="Career not found")
    return item


@router.get("/leadership/insights")
def leadership_insights(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest = (
        db.query(AssessmentResult)
        .filter(AssessmentResult.user_id == user.id, AssessmentResult.instrument_slug.in_(["leadership", "big-five"]))
        .order_by(AssessmentResult.created_at.desc())
        .first()
    )
    return {
        "disclaimer": "Leadership preferences are educational and must not be used for employment decisions.",
        "result": _result_out(latest) if latest else None,
        "practices": [
            "Name the decision, the owner, and the review date.",
            "Delegate one complete outcome, not a fragment.",
            "Give feedback on one observable behavior this week.",
        ],
    }


@router.get("/emotions/activities")
def emotion_activities():
    return {
        "disclaimer": "Educational emotional awareness activities. Not a clinical assessment or EQ score.",
        "activities": [
            {"slug": "name-the-feeling", "title": "Name the feeling", "minutes": 5, "prompt": "Write three body sensations and the feeling word that fits best."},
            {"slug": "listen-back", "title": "Reflective listening", "minutes": 10, "prompt": "In your next conversation, reflect one sentence before you add your view."},
            {"slug": "stress-weather", "title": "Everyday stress weather", "minutes": 5, "prompt": "Rate today's stress 1–5 and write one request that would help."},
        ],
    }


@router.post("/relationships/invitations", status_code=201)
def invite(payload: InviteIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if payload.email.lower() == user.email.lower():
        raise HTTPException(status_code=400, detail="You cannot invite yourself")
    invitee = db.query(User).filter(User.email == payload.email.lower()).first()
    row = RelationshipInvitation(
        inviter_id=user.id,
        invitee_email=payload.email.lower(),
        invitee_id=invitee.id if invitee else None,
        relationship_type=payload.relationship_type,
        token=secrets.token_urlsafe(24),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "status": row.status, "token": row.token}


@router.get("/relationships/invitations")
def list_invites(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sent = db.query(RelationshipInvitation).filter(RelationshipInvitation.inviter_id == user.id).all()
    received = db.query(RelationshipInvitation).filter(RelationshipInvitation.invitee_email == user.email).all()
    def out(row: RelationshipInvitation) -> dict:
        return {
            "id": row.id,
            "invitee_email": row.invitee_email,
            "relationship_type": row.relationship_type,
            "status": row.status,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }
    return {"sent": [out(r) for r in sent], "received": [out(r) for r in received]}


@router.post("/relationships/invitations/{invite_id}/accept")
def accept_invite(invite_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.get(RelationshipInvitation, invite_id)
    if not row or row.invitee_email != user.email:
        raise HTTPException(status_code=404, detail="Invitation not found")
    row.status = "accepted"
    row.invitee_id = user.id
    row.accepted_at = utcnow()
    db.commit()
    return {"ok": True}


@router.post("/relationships/invitations/{invite_id}/revoke")
def revoke_invite(invite_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.get(RelationshipInvitation, invite_id)
    if not row or (row.inviter_id != user.id and row.invitee_email != user.email):
        raise HTTPException(status_code=404, detail="Invitation not found")
    row.status = "revoked"
    row.revoked_at = utcnow()
    db.commit()
    return {"ok": True}


@router.get("/relationships/{invite_id}/comparison")
def compare(invite_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.get(RelationshipInvitation, invite_id)
    if not row or row.status != "accepted":
        raise HTTPException(status_code=404, detail="Accepted invitation not found")
    if user.id not in {row.inviter_id, row.invitee_id}:
        raise HTTPException(status_code=403, detail="Not a participant")
    other_id = row.invitee_id if user.id == row.inviter_id else row.inviter_id
    mine = (
        db.query(AssessmentResult)
        .filter(AssessmentResult.user_id == user.id, AssessmentResult.instrument_slug.in_(["big-five", "relationship-communication"]))
        .order_by(AssessmentResult.created_at.desc())
        .first()
    )
    theirs = (
        db.query(AssessmentResult)
        .filter(AssessmentResult.user_id == other_id, AssessmentResult.instrument_slug.in_(["big-five", "relationship-communication"]))
        .order_by(AssessmentResult.created_at.desc())
        .first()
    )
    return {
        "disclaimer": "This comparison is educational. It does not predict relationship success or recommend staying or leaving.",
        "relationship_type": row.relationship_type,
        "me": _result_out(mine) if mine else None,
        "other": _result_out(theirs) if theirs else None,
        "prompts": [
            "Where do we prefer different amounts of talking after a long day?",
            "What would a repair look like after a misunderstanding this week?",
            "Which strength in the other person do I under-use?",
        ],
        "private_journals_excluded": True,
        "coaching_history_excluded": True,
    }


# --- Reports / subscriptions / referrals ---
@router.get("/reports")
def list_reports(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(ReportRecord).filter(ReportRecord.user_id == user.id).order_by(ReportRecord.created_at.desc()).all()
    return [{"id": r.id, "title": r.title, "report_type": r.report_type, "version": r.version, "created_at": r.created_at.isoformat()} for r in rows]


@router.post("/reports", status_code=201)
def create_report(payload: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report_type = payload.get("report_type", "comprehensive")
    if report_type != "comprehensive" and not _is_premium(db, user):
        raise HTTPException(status_code=402, detail="Premium required")
    result = (
        db.query(AssessmentResult)
        .filter(AssessmentResult.user_id == user.id)
        .order_by(AssessmentResult.created_at.desc())
        .first()
    )
    if not result:
        raise HTTPException(status_code=400, detail="Complete an assessment first")
    profile = db.get(UserProfile, user.id)
    body = build_report_payload(
        {"display_name": profile.display_name if profile else "", "email": user.email},
        {"payload": result.payload},
        report_type,
    )
    row = ReportRecord(user_id=user.id, result_id=result.id, report_type=report_type, title=body["title"], payload=body)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "title": row.title, "payload": body}


@router.get("/reports/{report_id}")
def get_report(report_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.get(ReportRecord, report_id)
    if not row or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"id": row.id, "title": row.title, "report_type": row.report_type, "payload": row.payload}


@router.get("/reports/{report_id}/pdf")
def get_report_pdf(report_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.get(ReportRecord, report_id)
    if not row or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Report not found")
    pdf = render_pdf(row.payload)
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{row.id}.pdf"'})


@router.get("/personality/card")
def personality_card(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest = (
        db.query(AssessmentResult)
        .filter(AssessmentResult.user_id == user.id)
        .order_by(AssessmentResult.created_at.desc())
        .first()
    )
    profile = db.get(UserProfile, user.id)
    archetype = (latest.payload or {}).get("archetype") if latest else None
    return {
        "display_name": profile.display_name if profile else "",
        "archetype": archetype,
        "share_url": f"{get_settings().app_base_url}/card/{user.id[:8]}",
        "disclaimer": "Shared cards never include journals, scores-as-percentiles, or coaching transcripts.",
    }


@router.get("/subscriptions")
def get_sub(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sub = db.get(Subscription, user.id)
    return {
        "plan": sub.plan if sub else "free",
        "status": sub.status if sub else "active",
        "cancel_at_period_end": sub.cancel_at_period_end if sub else False,
        "pricing_hypothesis": {
            "monthly": 12.99,
            "annual": 79.99,
            "currency": "USD",
            "reports": {
                "personality": 9.99,
                "career": 19.99,
                "marriage": 19.99,
                "relationship": 19.99,
                "leadership": 19.99,
                "development": 14.99,
                "blueprint": 39.99,
            },
            "note": "Prices are configurable hypotheses requiring customer validation. Not a sales forecast.",
        },
        "providers": {"stripe": "not_configured", "revenuecat": "not_configured", "apple": "not_configured", "google": "not_configured"},
    }


@router.post("/subscriptions/premium-dev")
def grant_premium_dev(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not get_settings().app_debug:
        raise HTTPException(status_code=403, detail="Development entitlement grant is disabled")
    sub = db.get(Subscription, user.id)
    if not sub:
        sub = Subscription(user_id=user.id)
        db.add(sub)
    sub.plan = "premium"
    sub.status = "active"
    db.add(Entitlement(user_id=user.id, code="premium", active=True, source="dev"))
    db.commit()
    return {"ok": True, "plan": "premium"}


@router.post("/subscriptions/cancel")
def cancel_sub(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sub = db.get(Subscription, user.id)
    if sub:
        sub.cancel_at_period_end = True
        db.commit()
    return {"ok": True}


@router.get("/referrals")
def referrals(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Referral).filter(Referral.referrer_id == user.id).all()
    if not rows:
        row = Referral(referrer_id=user.id, code=user.id[:8].upper(), status="issued")
        db.add(row)
        db.commit()
        rows = [row]
    return {
        "code": rows[0].code,
        "url": f"{get_settings().app_base_url}/register?ref={rows[0].code}",
        "items": [{"id": r.id, "status": r.status, "referred_email": r.referred_email} for r in rows],
    }


@router.get("/notifications")
def notifications(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Notification).filter(Notification.user_id == user.id).order_by(Notification.created_at.desc()).all()
    return [{"id": n.id, "title": n.title, "body": n.body, "category": n.category, "read": n.read, "created_at": n.created_at.isoformat()} for n in rows]


@router.get("/insights/today")
def insight_today(user: User = Depends(get_current_user)):
    return {"insight": daily_insight(abs(hash(user.id + date.today().isoformat())) % 1000), "date": date.today().isoformat()}


# --- Privacy ---
@router.get("/privacy/export")
def export_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.add(DataExportRequest(user_id=user.id, status="ready"))
    journals = db.query(JournalEntry).filter(JournalEntry.user_id == user.id).all()
    results = db.query(AssessmentResult).filter(AssessmentResult.user_id == user.id).all()
    db.commit()
    return {
        "user": {"id": user.id, "email": user.email, "locale": user.locale},
        "results": [_result_out(r) for r in results],
        "journals": [_journal_out(j) for j in journals],
        "note": "Coaching transcripts are included only in a full export on request; this payload includes assessments and journals you own.",
    }


@router.post("/privacy/delete")
def request_delete(payload: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.add(AccountDeletionRequest(user_id=user.id, reason=payload.get("reason", ""), status="pending"))
    user.status = "pending_deletion"
    db.commit()
    return {"ok": True, "status": "pending_deletion"}


@router.post("/feedback")
def feedback(payload: FeedbackIn, user: User | None = Depends(get_optional_user), db: Session = Depends(get_db)):
    db.add(Feedback(user_id=user.id if user else None, category=payload.category, message=payload.message))
    db.commit()
    return {"ok": True}


@router.get("/help")
def help_center():
    return HELP_ARTICLES


@router.get("/legal/{slug}")
def legal(slug: str):
    if slug not in LEGAL_PAGES:
        raise HTTPException(status_code=404, detail="Unknown legal page")
    return {"slug": slug, "body": LEGAL_PAGES[slug]}


# --- Organizations / admin ---
@router.post("/organizations", status_code=201)
def create_org(payload: OrgIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(Organization).filter(Organization.slug == payload.slug).first():
        raise HTTPException(status_code=409, detail="Slug in use")
    org = Organization(name=payload.name, slug=payload.slug)
    db.add(org)
    db.flush()
    db.add(Membership(organization_id=org.id, user_id=user.id, role="owner", results_consent=False))
    db.commit()
    db.refresh(org)
    return {"id": org.id, "name": org.name, "slug": org.slug}


@router.get("/organizations")
def list_orgs(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    memberships = db.query(Membership).filter(Membership.user_id == user.id).all()
    out = []
    for member in memberships:
        org = db.get(Organization, member.organization_id)
        if org:
            out.append({"id": org.id, "name": org.name, "slug": org.slug, "role": member.role, "results_consent": member.results_consent})
    return out


@router.get("/admin/overview")
def admin_overview(user: User = Depends(require_roles("admin", "superadmin")), db: Session = Depends(get_db)):
    return {
        "users": db.query(User).count(),
        "results": db.query(AssessmentResult).count(),
        "conversations": db.query(Conversation).count(),
        "flags": [{"key": f.key, "enabled": f.enabled} for f in db.query(FeatureFlag).all()],
        "plans": {
            "free": db.query(Subscription).filter(Subscription.plan == "free").count(),
            "premium": db.query(Subscription).filter(Subscription.plan == "premium").count(),
        },
    }


@router.get("/admin/users")
def admin_users(user: User = Depends(require_roles("admin", "superadmin")), db: Session = Depends(get_db)):
    rows = db.query(User).order_by(User.created_at.desc()).limit(200).all()
    return [{"id": u.id, "email": u.email, "role": u.role, "status": u.status} for u in rows]
