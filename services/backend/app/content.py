"""Educational programs, careers, insights, and help content."""

from __future__ import annotations

PROGRAMS = [
    {
        "slug": "seven-day-self-awareness",
        "name": "7-Day Self-Awareness Sprint",
        "days": 7,
        "category": "self-awareness",
        "summary": "A short practice of noticing patterns without trying to overhaul your personality.",
        "objectives": [
            "Name one recurring pattern without judging it",
            "Connect a trait score to a real situation",
            "Leave with one sustainable next experiment",
        ],
        "days_content": [
            {"day": 1, "title": "Observe without fixing", "exercise": "Write three moments today when you felt most like yourself.", "reflection": "What did those moments have in common?"},
            {"day": 2, "title": "Trait in the wild", "exercise": "Pick one Big Five domain and catch it twice in real life.", "reflection": "When did the trait help, and when did it cost you?"},
            {"day": 3, "title": "The story you tell", "exercise": "Write the nickname you give yourself under stress.", "reflection": "Is that nickname a measurement or a verdict?"},
            {"day": 4, "title": "One conversation", "exercise": "Ask someone what they experience when you are at your best.", "reflection": "What surprised you?"},
            {"day": 5, "title": "Friction map", "exercise": "List two recurring frictions and the need underneath each.", "reflection": "Which friction is actually a values clash?"},
            {"day": 6, "title": "Tiny redesign", "exercise": "Change one environmental cue (calendar, desk, phone, doorway).", "reflection": "Did the cue make the desired action easier?"},
            {"day": 7, "title": "Keep one thing", "exercise": "Choose a single practice to keep for 30 more days.", "reflection": "How will you notice if it is working without shaming yourself?"},
        ],
    },
    {
        "slug": "thirty-day-communication",
        "name": "30-Day Communication Practice",
        "days": 30,
        "category": "communication",
        "summary": "Daily micro-practices for clearer, kinder, more specific conversations.",
        "objectives": ["Speak needs in one sentence", "Ask better questions", "Repair small ruptures faster"],
        "weekly_milestones": [
            "Week 1: Notice default style",
            "Week 2: Practice requests",
            "Week 3: Practice disagreement",
            "Week 4: Practice repair",
        ],
    },
    {
        "slug": "thirty-day-leadership",
        "name": "30-Day Leadership Practice",
        "days": 30,
        "category": "leadership",
        "summary": "Educational leadership habits — not a competency certification.",
        "objectives": ["Clarify decisions", "Delegate one real ownership", "Give one specific piece of feedback weekly"],
    },
    {
        "slug": "sixty-day-organization",
        "name": "60-Day Organization Foundations",
        "days": 60,
        "category": "organization",
        "summary": "Light systems for people who either over-plan or under-plan.",
        "objectives": ["A trusted capture habit", "A weekly review", "A shutdown ritual"],
    },
    {
        "slug": "sixty-day-confidence",
        "name": "60-Day Confidence in Action",
        "days": 60,
        "category": "confidence",
        "summary": "Confidence as kept promises and recovered attempts, not as a feeling you wait for.",
        "objectives": ["One visible attempt per week", "A recovery script after awkwardness"],
    },
    {
        "slug": "ninety-day-productivity",
        "name": "90-Day Sustainable Productivity",
        "days": 90,
        "category": "productivity",
        "summary": "Output without contempt for rest. No streak-shaming.",
        "objectives": ["Priority list", "Focus blocks", "Recovery scheduled like work"],
    },
    {
        "slug": "ninety-day-career",
        "name": "90-Day Career Exploration",
        "days": 90,
        "category": "career",
        "summary": "Experiments, informational conversations, and skill evidence — not a personality-based job assignment.",
        "objectives": ["A shortlist of interest themes", "Five conversations", "One portfolio-sized experiment"],
    },
    {
        "slug": "annual-development",
        "name": "Annual Personal Development Compass",
        "days": 365,
        "category": "self-awareness",
        "summary": "Four seasonal reviews of goals, relationships, work, and health-adjacent habits (non-clinical).",
        "objectives": ["Four reviews", "One word for the year", "A discard list"],
    },
]


CAREERS = [
    {
        "slug": "research-analyst",
        "title": "Research Analyst",
        "riasec": ["investigative", "conventional"],
        "summary": "Turns questions into structured evidence. Interest is not the same as statistical skill.",
        "skills_to_explore": ["Research design", "Writing for decision-makers", "Data literacy"],
        "learning": ["A methods primer", "A public dataset project", "A critique of a published claim"],
    },
    {
        "slug": "product-designer",
        "title": "Product Designer",
        "riasec": ["artistic", "investigative"],
        "summary": "Shapes how people experience a tool. Requires both taste and constraint.",
        "skills_to_explore": ["User research", "Interaction design", "Visual hierarchy"],
        "learning": ["Redesign a flow you use daily", "Sit in on a usability session"],
    },
    {
        "slug": "software-engineer",
        "title": "Software Engineer",
        "riasec": ["investigative", "realistic"],
        "summary": "Builds reliable systems. Personality does not determine whether someone can learn this craft.",
        "skills_to_explore": ["Problem decomposition", "Testing", "Collaboration in code review"],
        "learning": ["Ship a tiny tool that solves one of your own frictions"],
    },
    {
        "slug": "teacher-facilitator",
        "title": "Teacher / Facilitator",
        "riasec": ["social", "artistic"],
        "summary": "Helps other people learn. Warmth helps; design of learning matters more.",
        "skills_to_explore": ["Lesson design", "Feedback", "Classroom or workshop presence"],
        "learning": ["Teach a 20-minute session and collect three pieces of feedback"],
    },
    {
        "slug": "operations-lead",
        "title": "Operations Lead",
        "riasec": ["conventional", "enterprising"],
        "summary": "Makes the machine of work actually run. Invisible when excellent.",
        "skills_to_explore": ["Process design", "Vendor coordination", "Quality checks"],
        "learning": ["Map a broken process from request to done"],
    },
    {
        "slug": "founder-operator",
        "title": "Founder / Operator",
        "riasec": ["enterprising", "investigative"],
        "summary": "Holds uncertainty and still ships. Romanticizing personality as destiny is a risk here.",
        "skills_to_explore": ["Customer conversations", "Cash awareness", "Hiring judgment"],
        "learning": ["Talk to ten people with the problem you want to solve"],
    },
    {
        "slug": "counselor-coach-adjacent",
        "title": "Coach or Educator (non-clinical)",
        "riasec": ["social", "investigative"],
        "summary": "Supports development. This career path requires training, ethics, and supervision — PersonalityDNA is not that training.",
        "skills_to_explore": ["Listening", "Contracting", "Referral to licensed care"],
        "learning": ["Read a professional ethics code in the field you are considering"],
    },
    {
        "slug": "skilled-trade",
        "title": "Skilled Trade Specialist",
        "riasec": ["realistic", "conventional"],
        "summary": "Hands, tools, and standards. Often undervalued in personality-test career lists.",
        "skills_to_explore": ["Apprenticeship paths", "Safety", "Estimating"],
        "learning": ["Visit a training program or talk to someone currently in the trade"],
    },
]


HELP_ARTICLES = [
    {"slug": "how-scoring-works", "title": "How scoring works", "body": "PersonalityDNA uses a deterministic scoring engine. Reverse-keyed items are inverted, domain scores are means on a 1–5 scale, and 0–100 displays are min-max scaled raw sums — not percentiles."},
    {"slug": "not-therapy", "title": "This is not therapy", "body": "The coach and assessments are educational. They do not diagnose, treat, or replace licensed mental health care."},
    {"slug": "privacy", "title": "Privacy basics", "body": "Journals and coaching transcripts are private by default. Relationship comparison requires consent from every participant. Employers cannot see individual results without revocable consent."},
    {"slug": "archetypes", "title": "What archetypes are (and are not)", "body": "The 16 archetypes are original descriptive product constructs mapped from Big Five domain means. They are not MBTI types and are not independently validated categories."},
    {"slug": "crisis", "title": "If you are in crisis", "body": "Call local emergency services. In the US, call or text 988. International resources: https://www.iasp.info/suicidalthoughts/"},
    {"slug": "subscriptions", "title": "Plans and cancellation", "body": "Free includes Quick Discovery, Big Five, a basic dashboard, limited coaching, and a shareable card. Premium is a pricing hypothesis ($9.99/mo or $69.99/yr) and must be validated. Cancel anytime from Subscription settings. Store purchases follow Apple and Google rules."},
]


LEGAL_PAGES = {
    "privacy": "PersonalityDNA AI treats assessments, journals, and coaching as sensitive personal information. We do not sell personality data. Full legal review is required before commercial launch. This page is a product statement, not legal advice.",
    "terms": "The service is for adults 18+ for personal development education. Not a medical device. Not for automated hiring, firing, or eligibility decisions.",
    "cookies": "Local development uses essential session cookies only. Privacy-preserving analytics will be introduced with an opt-in model.",
    "ai": "The coach uses authorized context only. Private journals are excluded unless you enable journal AI analysis. We do not train foundation models on your private data without separate informed consent.",
}


INSIGHTS_LIBRARY = [
    "A trait score is a tendency, not a verdict about your worth.",
    "If a result feels wrong, treat it as a hypothesis and look for behavior in the last two weeks.",
    "Reverse-scored items exist because agreeing with everything would flatten a profile.",
    "Growth is usually a smaller version of a strength used more flexibly, not the opposite personality.",
    "You can decline an AI interpretation of any journal entry.",
    "Mixed profiles are expected. Mid-range scores are information, not indecision.",
    "Do not use these results to rank people on a team.",
    "Rest is part of conscientiousness too — it is how a system stays reliable.",
]


def program_by_slug(slug: str) -> dict | None:
    return next((item for item in PROGRAMS if item["slug"] == slug), None)


def career_by_slug(slug: str) -> dict | None:
    return next((item for item in CAREERS if item["slug"] == slug), None)


def daily_insight(seed: int) -> str:
    return INSIGHTS_LIBRARY[seed % len(INSIGHTS_LIBRARY)]
