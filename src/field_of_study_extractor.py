
import re


FIELDS_OF_STUDY = [
    "information technology",
    "information systems",
    "software development",
    "computer science",
    "computer systems",
    "network engineering",
    "computer networking",
    "cybersecurity",
    "data science",
    "data analytics",
    "business information systems",
    "business management",
    "business administration",
    "financial management",
    "accounting",
    "finance",
    "marketing",
    "human resource management",
    "public management",
    "office administration",
    "agriculture",
    "agricultural management",
    "animal production",
    "animal science",
    "animal health",
    "crop production",
    "environmental science",
    "teaching",
    "nursing",
    "public health",
    "social work",
    "hospitality management",
    "tourism management",
    "logistics",
    "supply chain management",
    "electrical engineering",
    "mechanical engineering",
    "civil engineering",
]


EDUCATION_HEADINGS = {
    "education",
    "educational background",
    "academic background",
    "qualifications",
    "academic qualifications",
}

STOP_HEADINGS = {
    "work experience",
    "employment history",
    "professional experience",
    "work history",
    "professional profile",
    "core skills",
    "skills",
    "languages",
    "references",
    "certifications",
    "certificates",
    "projects",
    "personal information",
}


def extract_education_section(text):
    """Extract text between the education heading and the next major section."""

    lines = text.splitlines()
    education_lines = []
    inside_education = False

    for line in lines:
        cleaned = line.strip().strip(":").strip()
        normalized = re.sub(r"\s+", " ", cleaned).lower()

        if normalized in EDUCATION_HEADINGS:
            inside_education = True
            continue

        if inside_education and normalized in STOP_HEADINGS:
            break

        if inside_education and cleaned:
            education_lines.append(cleaned)

    return "\n".join(education_lines)


def extract_fields_of_study(text):
    """
    Identify fields of study only inside the education section.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    education_text = extract_education_section(text)

    if not education_text:
        return []

    found_fields = []

    for field in sorted(FIELDS_OF_STUDY, key=len, reverse=True):
        pattern = r"(?<!\w)" + re.escape(field) + r"(?!\w)"

        if re.search(pattern, education_text, re.IGNORECASE):
            found_fields.append(field.title())

    return found_fields
