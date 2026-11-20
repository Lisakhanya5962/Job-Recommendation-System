
import re


# Recognised work experience headings
EXPERIENCE_HEADINGS = {
    "work experience",
    "working experience",
    "employment history",
    "employment experience",
    "professional experience",
    "career history",
    "career experience",
    "work history",
    "relevant experience",
    "working history",
    "internship experience",
    "volunteer experience",
    "experience",
}

# Headings that indicate the experience section has ended
STOP_HEADINGS = {
    "education",
    "educational background",
    "academic background",
    "qualifications",
    "academic qualifications",
    "skills",
    "core skills",
    "technical skills",
    "certifications",
    "certificates",
    "references",
    "personal information",
    "personal details",
    "projects",
    "languages",
    "interests",
    "hobbies",
}


def normalize_heading(line):
    """Clean a line before checking whether it is a section heading."""

    line = line.strip().lower()

    # Remove common bullet characters
    line = re.sub(r"^[\s•●▪■\-*]+", "", line)

    # Remove numbering, for example: 1. Work Experience
    line = re.sub(r"^\d+[\.)]\s*", "", line)

    # Remove punctuation around headings
    line = re.sub(r"[:\-\s]+$", "", line)
    line = re.sub(r"^[:\-\s]+", "", line)

    # Normalise whitespace
    line = re.sub(r"\s+", " ", line)

    return line.strip()


def is_experience_heading(line):
    """Check whether a line represents an experience heading."""

    normalized = normalize_heading(line)

    return normalized in EXPERIENCE_HEADINGS


def is_stop_heading(line):
    """Check whether a line represents the end of experience."""

    normalized = normalize_heading(line)

    return normalized in STOP_HEADINGS


def extract_experience_section(text):
    """
    Extract lines between a recognised work experience heading
    and the next major CV section.
    """

    lines = text.splitlines()

    experience_lines = []
    inside_experience = False

    for line in lines:

        cleaned = line.strip()

        if not cleaned:
            continue

        if is_experience_heading(cleaned):
            inside_experience = True
            continue

        if inside_experience and is_stop_heading(cleaned):
            break

        if inside_experience:
            experience_lines.append(cleaned)

    return experience_lines


def extract_experience(text):
    """
    Extract work experience information from CV text.

    Returns a list of non-empty lines from the recognised
    employment history section.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    return extract_experience_section(text)
