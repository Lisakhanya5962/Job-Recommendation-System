
import re


QUALIFICATION_KEYWORDS = [
    "national senior certificate",
    "senior certificate",
    "grade 12",
    "matric",
    "national certificate",
    "higher certificate",
    "advanced certificate",
    "certificate",
    "diploma",
    "advanced diploma",
    "national diploma",
    "bachelor's degree",
    "bachelors degree",
    "bachelor degree",
    "honours degree",
    "honours",
    "master's degree",
    "masters degree",
    "master degree",
    "doctorate",
    "phd",
    "postgraduate diploma",
    "postgraduate certificate",
]


def extract_qualifications(text):
    """
    Identify education qualifications from CV text.

    Returns a list of unique qualifications.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    found_qualifications = []

    for qualification in QUALIFICATION_KEYWORDS:
        pattern = (
            r"(?<!\w)"
            + re.escape(qualification)
            + r"(?!\w)"
        )

        if re.search(pattern, text, re.IGNORECASE):
            formatted = qualification.title()

            if formatted not in found_qualifications:
                found_qualifications.append(formatted)

    return found_qualifications
