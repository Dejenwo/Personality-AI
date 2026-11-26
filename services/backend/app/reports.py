from __future__ import annotations

from io import BytesIO
from typing import Any

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def build_report_payload(user: dict[str, Any], result: dict[str, Any], report_type: str) -> dict[str, Any]:
    archetype = (result.get("payload") or result).get("archetype") or {}
    traits = (result.get("payload") or result).get("trait_scores") or {}
    return {
        "report_type": report_type,
        "version": "1.0.0",
        "title": {
            "comprehensive": "Comprehensive Personality Profile",
            "big-five": "Big Five Personality Traits",
            "career": "Career Exploration Report",
            "relationship": "Relationship Communication Report",
            "leadership": "Leadership Development Report",
        }.get(report_type, "PersonalityDNA Report"),
        "user": {"display_name": user.get("display_name"), "email": user.get("email")},
        "archetype": archetype,
        "secondary_archetype": (result.get("payload") or result).get("secondary_archetype"),
        "traits": traits,
        "strengths": (result.get("payload") or result).get("strengths", []),
        "growth_areas": (result.get("payload") or result).get("growth_areas", []),
        "methodology": (
            "Scores were produced by PersonalityDNA scoring algorithm v1 from the stored "
            "instrument version. They are reproducible from the response hash. 0–100 values "
            "are min-max scaled raw sums, not population percentiles."
        ),
        "limitations": (
            "Educational use only. Not a clinical diagnosis, not a hiring tool, and not a "
            "prediction of relationship success."
        ),
        "disclaimer": "Archetypes are descriptive product constructs, not validated scientific categories.",
        "response_hash": (result.get("payload") or result).get("response_hash"),
        "instrument_slug": (result.get("payload") or result).get("instrument_slug"),
        "instrument_version": (result.get("payload") or result).get("instrument_version"),
    }


def render_pdf(payload: dict[str, Any]) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=payload.get("title", "Report"))
    styles = getSampleStyleSheet()
    story = [
        Paragraph("PersonalityDNA AI", styles["Title"]),
        Paragraph(payload.get("title", "Report"), styles["Heading1"]),
        Spacer(1, 12),
        Paragraph(payload.get("archetype", {}).get("name", "Profile"), styles["Heading2"]),
        Paragraph(payload.get("archetype", {}).get("description", ""), styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Methodology", styles["Heading2"]),
        Paragraph(payload.get("methodology", ""), styles["BodyText"]),
        Spacer(1, 8),
        Paragraph("Limitations", styles["Heading2"]),
        Paragraph(payload.get("limitations", ""), styles["BodyText"]),
        Spacer(1, 8),
        Paragraph("Disclaimer", styles["Heading2"]),
        Paragraph(payload.get("disclaimer", ""), styles["BodyText"]),
    ]
    if payload.get("response_hash"):
        story += [Spacer(1, 8), Paragraph(f"Response hash: {payload['response_hash']}", styles["Code"])]
    for trait, score in (payload.get("traits") or {}).items():
        story += [
            Spacer(1, 6),
            Paragraph(f"{score.get('name', trait)} — mean {score.get('mean')}", styles["Heading3"]),
            Paragraph(score.get("explanation", ""), styles["BodyText"]),
        ]
    doc.build(story)
    return buffer.getvalue()
