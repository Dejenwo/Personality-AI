"""Occupation explorer.

Wage, demand, and outlook figures are not stored. Each record points to
O*NET OnLine. Do not invent salary statistics.
"""

from __future__ import annotations

from typing import Any

ONET = "https://www.onetonline.org/link/summary/{soc}"
BLS = "https://www.bls.gov/oes/"

# Public O*NET-SOC titles. Interest letters are typical O*NET first-letter
# themes where commonly published; they are exploration tags, not scores.
OCCUPATIONS: list[dict[str, Any]] = [
    {"slug": "software-developers", "title": "Software Developers", "soc": "15-1252.00", "riasec": ["I", "C", "R"], "summary": "Design and build software systems.", "education": "Often a bachelor's in computing or equivalent experience.", "environment": "Office, remote, or hybrid; long focus blocks."},
    {"slug": "data-scientists", "title": "Data Scientists", "soc": "15-2051.00", "riasec": ["I", "C"], "summary": "Turn questions into models and evidence.", "education": "Often quantitative graduate study or equivalent portfolio.", "environment": "Analytical teams; mixed coding and communication."},
    {"slug": "computer-systems-analysts", "title": "Computer Systems Analysts", "soc": "15-1211.00", "riasec": ["I", "C"], "summary": "Bridge business problems and technical systems.", "education": "Often a bachelor's plus domain knowledge.", "environment": "Meetings plus analysis."},
    {"slug": "information-security-analysts", "title": "Information Security Analysts", "soc": "15-1212.00", "riasec": ["I", "C", "R"], "summary": "Protect systems and respond to incidents.", "education": "Computing background plus security credentials are common.", "environment": "On-call and documentation-heavy."},
    {"slug": "web-and-digital-interface-designers", "title": "Web and Digital Interface Designers", "soc": "15-1255.00", "riasec": ["A", "I"], "summary": "Design usable digital interfaces.", "education": "Portfolio often matters as much as a degree.", "environment": "Collaborative product teams."},
    {"slug": "computer-user-support-specialists", "title": "Computer User Support Specialists", "soc": "15-1232.00", "riasec": ["S", "C", "R"], "summary": "Help people use technology under pressure.", "education": "Certificates and experience pathways are common.", "environment": "Tickets, phones, deskside."},
    {"slug": "civil-engineers", "title": "Civil Engineers", "soc": "17-2051.00", "riasec": ["R", "I", "C"], "summary": "Plan and oversee civil infrastructure.", "education": "Bachelor's in engineering; licensure for many roles.", "environment": "Office plus field sites."},
    {"slug": "mechanical-engineers", "title": "Mechanical Engineers", "soc": "17-2141.00", "riasec": ["R", "I"], "summary": "Design mechanical systems and products.", "education": "Bachelor's in mechanical engineering is typical.", "environment": "Labs, plants, CAD."},
    {"slug": "electrical-engineers", "title": "Electrical Engineers", "soc": "17-2071.00", "riasec": ["I", "R"], "summary": "Design electrical and electronic systems.", "education": "Bachelor's in electrical engineering is typical.", "environment": "Labs and project teams."},
    {"slug": "industrial-engineers", "title": "Industrial Engineers", "soc": "17-2112.00", "riasec": ["I", "C", "E"], "summary": "Improve processes, quality, and flow.", "education": "Bachelor's in industrial engineering or related.", "environment": "Plants and operations centers."},
    {"slug": "architects", "title": "Architects, Except Landscape and Naval", "soc": "17-1011.00", "riasec": ["A", "I", "R"], "summary": "Design buildings and coordinate construction intent.", "education": "Professional degree plus licensure in many jurisdictions.", "environment": "Studios and sites."},
    {"slug": "registered-nurses", "title": "Registered Nurses", "soc": "29-1141.00", "riasec": ["S", "I"], "summary": "Provide and coordinate patient care.", "education": "Nursing degree and license required.", "environment": "Hospitals, clinics, community; shift work common."},
    {"slug": "nurse-practitioners", "title": "Nurse Practitioners", "soc": "29-1171.00", "riasec": ["S", "I"], "summary": "Advanced nursing practice with assessment and treatment within scope.", "education": "Graduate nursing plus license.", "environment": "Clinics and hospitals."},
    {"slug": "physicians-assistants", "title": "Physician Assistants", "soc": "29-1071.00", "riasec": ["S", "I"], "summary": "Practice medicine with physician supervision as defined by law.", "education": "Master's PA program plus license.", "environment": "Clinics, hospitals."},
    {"slug": "physical-therapists", "title": "Physical Therapists", "soc": "29-1123.00", "riasec": ["S", "I", "R"], "summary": "Help people restore movement and function.", "education": "Doctor of physical therapy plus license.", "environment": "Clinics, hospitals, sports settings."},
    {"slug": "pharmacists", "title": "Pharmacists", "soc": "29-1051.00", "riasec": ["I", "C"], "summary": "Dispense medications and advise on their use.", "education": "Pharm.D. plus license.", "environment": "Pharmacies, hospitals."},
    {"slug": "pharmacy-technicians", "title": "Pharmacy Technicians", "soc": "29-2052.00", "riasec": ["C", "R"], "summary": "Support pharmacists with dispensing and operations.", "education": "On-the-job, certificate, or license by state.", "environment": "Retail and hospital pharmacies."},
    {"slug": "medical-assistants", "title": "Medical Assistants", "soc": "31-9092.00", "riasec": ["S", "C"], "summary": "Clinical and administrative support in care settings.", "education": "Certificate programs are common.", "environment": "Clinics."},
    {"slug": "emts", "title": "Emergency Medical Technicians", "soc": "29-2042.00", "riasec": ["R", "S"], "summary": "Provide emergency medical response.", "education": "State-approved EMT training and certification.", "environment": "Ambulances, shift work, high arousal."},
    {"slug": "home-health-aides", "title": "Home Health and Personal Care Aides", "soc": "31-1120.00", "riasec": ["S", "R"], "summary": "Support people in daily living at home.", "education": "Short training; requirements vary.", "environment": "Homes; physical and relational work."},
    {"slug": "elementary-teachers", "title": "Elementary School Teachers, Except Special Education", "soc": "25-2021.00", "riasec": ["S", "A"], "summary": "Teach young students across subjects.", "education": "Bachelor's plus state certification typical.", "environment": "Classrooms, high social load."},
    {"slug": "instructional-coordinators", "title": "Instructional Coordinators", "soc": "25-9031.00", "riasec": ["S", "I", "A"], "summary": "Develop curricula and support teachers.", "education": "Often a master's in education.", "environment": "District offices and schools."},
    {"slug": "librarians", "title": "Librarians and Media Collections Specialists", "soc": "25-4022.00", "riasec": ["C", "S", "A"], "summary": "Organize information and help people find it.", "education": "Often an MLIS.", "environment": "Libraries, quiet-to-busy public spaces."},
    {"slug": "career-counselors", "title": "Educational, Guidance, and Career Counselors and Advisors", "soc": "21-1012.00", "riasec": ["S", "A"], "summary": "Help people plan education and work. This is not a substitute for licensed therapy.", "education": "Often a master's plus credential.", "environment": "Schools and career centers."},
    {"slug": "child-family-social-workers", "title": "Child, Family, and School Social Workers", "soc": "21-1021.00", "riasec": ["S", "A"], "summary": "Support families and children in systems of care.", "education": "Bachelor's or master's in social work; license for many roles.", "environment": "Agencies, schools, homes."},
    {"slug": "mental-health-counselors", "title": "Mental Health Counselors", "soc": "21-1014.00", "riasec": ["S", "A"], "summary": "Licensed counseling practice. PersonalityDNA is not this job and does not diagnose.", "education": "Graduate degree plus license.", "environment": "Clinics, private practice."},
    {"slug": "community-service-managers", "title": "Social and Community Service Managers", "soc": "11-9151.00", "riasec": ["E", "S"], "summary": "Run programs that serve communities.", "education": "Often a bachelor's plus experience.", "environment": "Nonprofits and public agencies."},
    {"slug": "general-managers", "title": "General and Operations Managers", "soc": "11-1021.00", "riasec": ["E", "C"], "summary": "Direct operations and people toward results.", "education": "Varies widely; experience is common.", "environment": "Offices, sites, hybrid."},
    {"slug": "marketing-managers", "title": "Marketing Managers", "soc": "11-2021.00", "riasec": ["E", "A"], "summary": "Set marketing strategy and spend.", "education": "Often a bachelor's plus experience.", "environment": "Offices, agencies, remote."},
    {"slug": "sales-managers", "title": "Sales Managers", "soc": "11-2022.00", "riasec": ["E", "S"], "summary": "Lead sales teams and pipelines.", "education": "Experience often outweighs a specific degree.", "environment": "Field and office."},
    {"slug": "hr-managers", "title": "Human Resources Managers", "soc": "11-3121.00", "riasec": ["E", "S", "C"], "summary": "Design people systems. Not a license to use personality tests for hiring here.", "education": "Often a bachelor's plus HR experience.", "environment": "Offices."},
    {"slug": "hr-specialists", "title": "Human Resources Specialists", "soc": "13-1071.00", "riasec": ["S", "C", "E"], "summary": "Recruiting, benefits, and employee relations support.", "education": "Bachelor's common, not always required.", "environment": "Offices."},
    {"slug": "management-analysts", "title": "Management Analysts", "soc": "13-1111.00", "riasec": ["I", "E", "C"], "summary": "Advise organizations on process and strategy.", "education": "Bachelor's plus domain experience.", "environment": "Consulting travel or internal strategy teams."},
    {"slug": "market-research-analysts", "title": "Market Research Analysts and Marketing Specialists", "soc": "13-1161.00", "riasec": ["I", "E"], "summary": "Study markets and customer evidence.", "education": "Often a bachelor's in a quantitative or social field.", "environment": "Offices, mixed analysis and stakeholder work."},
    {"slug": "project-management-specialists", "title": "Project Management Specialists", "soc": "13-1082.00", "riasec": ["E", "C"], "summary": "Plan, track, and close projects.", "education": "Experience plus optional PMP or similar.", "environment": "Cross-functional teams."},
    {"slug": "accountants", "title": "Accountants and Auditors", "soc": "13-2011.00", "riasec": ["C", "E"], "summary": "Prepare and examine financial records.", "education": "Bachelor's in accounting; CPA for many roles.", "environment": "Offices; busy seasons."},
    {"slug": "bookkeeping", "title": "Bookkeeping, Accounting, and Auditing Clerks", "soc": "43-3031.00", "riasec": ["C"], "summary": "Record financial transactions.", "education": "Certificate or associate common.", "environment": "Offices, remote possible."},
    {"slug": "financial-managers", "title": "Financial Managers", "soc": "11-3031.00", "riasec": ["E", "C"], "summary": "Direct financial operations. This app does not give investment advice.", "education": "Bachelor's plus experience; MBA sometimes.", "environment": "Offices."},
    {"slug": "financial-analysts", "title": "Financial and Investment Analysts", "soc": "13-2051.00", "riasec": ["I", "C", "E"], "summary": "Analyze financial information. Not personalized investing advice.", "education": "Bachelor's in finance or related.", "environment": "Offices, markets hours."},
    {"slug": "lawyers", "title": "Lawyers", "soc": "23-1011.00", "riasec": ["E", "I"], "summary": "Advise and represent clients on legal matters.", "education": "Law degree plus bar admission.", "environment": "Offices, courts."},
    {"slug": "paralegals", "title": "Paralegals and Legal Assistants", "soc": "23-2011.00", "riasec": ["C", "I"], "summary": "Support lawyers with research and documents.", "education": "Certificate or bachelor's; varies.", "environment": "Law offices."},
    {"slug": "writers", "title": "Writers and Authors", "soc": "27-3043.00", "riasec": ["A"], "summary": "Create written content.", "education": "Portfolio-driven; degrees vary.", "environment": "Often independent or newsrooms."},
    {"slug": "graphic-designers", "title": "Graphic Designers", "soc": "27-1024.00", "riasec": ["A", "R"], "summary": "Create visual communications.", "education": "Portfolio plus often a design degree.", "environment": "Studios, agencies, in-house."},
    {"slug": "public-relations-specialists", "title": "Public Relations Specialists", "soc": "27-3031.00", "riasec": ["E", "A"], "summary": "Shape public communication.", "education": "Communications-related bachelor's common.", "environment": "Agencies, in-house, on-call news."},
    {"slug": "producers-directors", "title": "Producers and Directors", "soc": "27-2012.00", "riasec": ["E", "A"], "summary": "Coordinate creative productions.", "education": "Experience-heavy; degrees vary.", "environment": "Sets, studios, irregular hours."},
    {"slug": "interpreters", "title": "Interpreters and Translators", "soc": "27-3091.00", "riasec": ["A", "S"], "summary": "Convert language in speech or writing.", "education": "Fluency plus credentials in many settings.", "environment": "Courts, hospitals, remote."},
    {"slug": "urban-planners", "title": "Urban and Regional Planners", "soc": "19-3051.00", "riasec": ["I", "E"], "summary": "Plan land use and community development.", "education": "Often a master's in planning.", "environment": "Government and consulting."},
    {"slug": "environmental-scientists", "title": "Environmental Scientists and Specialists, Including Health", "soc": "19-2041.00", "riasec": ["I", "R"], "summary": "Study and advise on environmental problems.", "education": "Bachelor's in environmental science or related.", "environment": "Field plus office."},
    {"slug": "medical-scientists", "title": "Medical Scientists, Except Epidemiologists", "soc": "19-1042.00", "riasec": ["I"], "summary": "Research human health.", "education": "Often a doctorate.", "environment": "Labs and universities."},
    {"slug": "statisticians", "title": "Statisticians", "soc": "15-2041.00", "riasec": ["I", "C"], "summary": "Collect and analyze data using statistical methods.", "education": "Usually a master's or doctorate.", "environment": "Government, research, industry."},
    {"slug": "construction-managers", "title": "Construction Managers", "soc": "11-9021.00", "riasec": ["E", "R", "C"], "summary": "Coordinate construction projects.", "education": "Experience plus often a construction or engineering degree.", "environment": "Job sites."},
    {"slug": "electricians", "title": "Electricians", "soc": "47-2111.00", "riasec": ["R", "C"], "summary": "Install and maintain electrical systems.", "education": "Apprenticeship and license typical.", "environment": "Sites, physical work."},
    {"slug": "carpenters", "title": "Carpenters", "soc": "47-2031.00", "riasec": ["R", "C"], "summary": "Build and repair structures from wood and related materials.", "education": "Apprenticeship or on-the-job.", "environment": "Sites, weather, physical work."},
    {"slug": "hvac", "title": "Heating, Air Conditioning, and Refrigeration Mechanics and Installers", "soc": "49-9021.00", "riasec": ["R", "C"], "summary": "Install and repair HVAC systems.", "education": "Technical training plus license in many states.", "environment": "Homes, commercial buildings."},
    {"slug": "auto-techs", "title": "Automotive Service Technicians and Mechanics", "soc": "49-3023.00", "riasec": ["R", "C"], "summary": "Diagnose and repair vehicles.", "education": "Technical training common.", "environment": "Shops."},
    {"slug": "maintenance-workers", "title": "Maintenance and Repair Workers, General", "soc": "49-9071.00", "riasec": ["R", "C"], "summary": "Keep buildings and equipment working.", "education": "On-the-job plus some technical training.", "environment": "Facilities."},
    {"slug": "truck-drivers", "title": "Heavy and Tractor-Trailer Truck Drivers", "soc": "53-3032.00", "riasec": ["R", "C"], "summary": "Transport goods over roads.", "education": "CDL required.", "environment": "Long hours, independence, regulations."},
    {"slug": "cooks", "title": "Cooks, Restaurant", "soc": "35-2014.00", "riasec": ["R", "A", "E"], "summary": "Prepare meals in restaurants.", "education": "On-the-job; culinary school optional.", "environment": "Kitchens, nights, weekends."},
    {"slug": "food-supervisors", "title": "First-Line Supervisors of Food Preparation and Serving Workers", "soc": "35-1012.00", "riasec": ["E", "C", "R"], "summary": "Supervise restaurant and kitchen staff.", "education": "Experience typical.", "environment": "Food service, peak hours."},
    {"slug": "retail-supervisors", "title": "First-Line Supervisors of Retail Sales Workers", "soc": "41-1011.00", "riasec": ["E", "C", "S"], "summary": "Run a retail team and floor.", "education": "Experience typical.", "environment": "Stores, weekends."},
    {"slug": "retail-salespersons", "title": "Retail Salespersons", "soc": "41-2031.00", "riasec": ["E", "S"], "summary": "Help customers buy goods.", "education": "Short training.", "environment": "Stores."},
    {"slug": "sales-reps", "title": "Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products", "soc": "41-4012.00", "riasec": ["E", "C"], "summary": "Sell goods to businesses.", "education": "Experience plus product knowledge.", "environment": "Field and phone."},
    {"slug": "customer-service", "title": "Customer Service Representatives", "soc": "43-4051.00", "riasec": ["S", "C", "E"], "summary": "Handle customer questions and problems.", "education": "Short training.", "environment": "Call centers, retail, remote."},
    {"slug": "office-supervisors", "title": "First-Line Supervisors of Office and Administrative Support Workers", "soc": "43-1011.00", "riasec": ["C", "E"], "summary": "Supervise office staff and workflows.", "education": "Experience typical.", "environment": "Offices."},
    {"slug": "health-services-managers", "title": "Medical and Health Services Managers", "soc": "11-9111.00", "riasec": ["E", "C", "S"], "summary": "Run healthcare units and clinics.", "education": "Often a bachelor's or master's in health admin.", "environment": "Hospitals and clinics."},
    {"slug": "exercise-trainers", "title": "Exercise Trainers and Group Fitness Instructors", "soc": "39-9031.00", "riasec": ["S", "R"], "summary": "Lead fitness activities. Not a medical treatment.", "education": "Certification common.", "environment": "Gyms, irregular hours."},
    {"slug": "interior-designers", "title": "Interior Designers", "soc": "27-1025.00", "riasec": ["A", "E"], "summary": "Plan interior spaces.", "education": "Design degree plus portfolio; license in some states.", "environment": "Studios and client sites."},
    {"slug": "construction-supervisors", "title": "First-Line Supervisors of Construction Trades and Extraction Workers", "soc": "47-1011.00", "riasec": ["R", "E", "C"], "summary": "Supervise trade crews.", "education": "Experience in the trade.", "environment": "Job sites."},
    {"slug": "claims-adjusters", "title": "Claims Adjusters, Examiners, and Investigators", "soc": "13-1031.00", "riasec": ["C", "E"], "summary": "Investigate insurance claims.", "education": "Bachelor's or experience; licenses vary.", "environment": "Offices and field."},
    {"slug": "human-service-assistants", "title": "Social and Human Service Assistants", "soc": "21-1093.00", "riasec": ["S"], "summary": "Support clients in social service programs.", "education": "Certificate or associate common.", "environment": "Agencies."},
    {"slug": "speech-pathologists", "title": "Speech-Language Pathologists", "soc": "29-1127.00", "riasec": ["S", "I"], "summary": "Assess and treat communication disorders. This app does not diagnose.", "education": "Master's plus license.", "environment": "Schools, clinics, hospitals."},
]

RIASEC_NAMES = {
    "R": "Realistic",
    "I": "Investigative",
    "A": "Artistic",
    "S": "Social",
    "E": "Enterprising",
    "C": "Conventional",
}


def _public(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "riasec_labels": [RIASEC_NAMES[letter] for letter in row["riasec"]],
        "source": "O*NET OnLine",
        "source_url": ONET.format(soc=row["soc"]),
        "bls_oes_url": BLS,
        "salary": None,
        "outlook": None,
        "salary_note": "Wage and outlook figures are not stored here. Use BLS Occupational Employment and Wage Statistics and O*NET for current numbers. Do not treat this app as a labor-market forecast.",
        "last_reviewed": "2026-11-26",
        "limitations": "Titles and SOC codes are public occupational labels. Fit is not determined by personality type. Interests, skills, constraints, and training still have to be checked by the user.",
    }


def list_occupations(riasec: str | None = None, q: str | None = None) -> list[dict[str, Any]]:
    rows = [_public(row) for row in OCCUPATIONS]
    if riasec:
        letter = riasec[0].upper()
        rows = [row for row in rows if letter in row["riasec"]]
    if q:
        needle = q.lower()
        rows = [row for row in rows if needle in row["title"].lower() or needle in row["summary"].lower()]
    return rows


def get_occupation(slug: str) -> dict[str, Any] | None:
    for row in OCCUPATIONS:
        if row["slug"] == slug:
            return _public(row)
    return None


def explore_for_interests(letters: list[str], skills: list[str] | None = None) -> dict[str, Any]:
    wanted = {letter[0].upper() for letter in letters if letter}
    ranked = []
    for row in list_occupations():
        overlap = len(wanted.intersection(row["riasec"]))
        skill_hit = 0
        if skills:
            blob = f"{row['title']} {row['summary']}".lower()
            skill_hit = sum(1 for skill in skills if skill.lower() in blob)
        ranked.append({**row, "interest_overlap": overlap, "skill_mention": skill_hit})
    ranked.sort(key=lambda item: (item["interest_overlap"], item["skill_mention"]), reverse=True)
    return {
        "why": "Occupations are ranked by overlap with user-stated RIASEC letters and optional skill keywords. Personality type is not used to exclude careers.",
        "primary": ranked[:20],
        "alternatives": ranked[20:30],
        "limitations": "This is an exploration list, not a hiring recommendation or a forecast of success.",
    }
