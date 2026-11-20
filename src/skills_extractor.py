
import re


# Skills recognized across different industries.
SKILL_KEYWORDS = [
    # IT and software development
    "python",
    "java",
    "javascript",
    "c#",
    "c++",
    "html",
    "css",
    "sql",
    "mysql",
    "postgresql",
    "django",
    "flask",
    "asp.net",
    "software development",
    "web development",
    "web design",
    "database management",
    "networking",
    "computer networking",
    "technical support",
    "it support",
    "troubleshooting",
    "hardware maintenance",
    "software installation",
    "cybersecurity",
    "machine learning",
    "artificial intelligence",
    "data analysis",
    "data collection",
    "data entry",

    # Office and administration
    "administration",
    "administrative support",
    "office administration",
    "record keeping",
    "filing",
    "document management",
    "microsoft office",
    "microsoft word",
    "microsoft excel",
    "microsoft powerpoint",
    "excel",
    "typing",
    "report writing",
    "email management",
    "scheduling",

    # Business and finance
    "accounting",
    "bookkeeping",
    "financial management",
    "budgeting",
    "invoicing",
    "payroll",
    "stock control",
    "inventory management",
    "sales",
    "marketing",
    "business management",
    "project management",
    "entrepreneurship",

    # Agriculture and animal production
    "animal production",
    "animal care",
    "animal husbandry",
    "livestock management",
    "crop production",
    "crop farming",
    "farming",
    "agriculture",
    "agricultural production",
    "farm management",
    "food production",
    "physical fitness",

    # Customer service and communication
    "customer service",
    "customer relations",
    "communication",
    "verbal communication",
    "written communication",
    "public speaking",
    "teamwork",
    "leadership",
    "problem solving",
    "conflict resolution",
    "interpersonal skills",
    "time management",
    "organisation",
    "organization",
    "attention to detail",
    "decision making",
    "critical thinking",
    "adaptability",
    "reliability",
    "responsibility",
    "punctuality",
    "working independently",
    "ability to learn",
    "following instructions",

    # Healthcare and care services
    "patient care",
    "first aid",
    "health and safety",
    "healthcare",
    "caregiving",
    "record management",
    "infection control",

    # General workplace skills
    "maintenance",
    "quality control",
    "safety procedures",
    "communication skills",
    "computer literacy",
    "multitasking",
    "training",
    "supervision",
]


def extract_skills(text):
    """
    Identify recognized skills from CV text.

    Returns a list of unique skill names.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    found_skills = []

    for skill in SKILL_KEYWORDS:
        # Match complete words and phrases, ignoring letter case.
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill.title())

    return found_skills
