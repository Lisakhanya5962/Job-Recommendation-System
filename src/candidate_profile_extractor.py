
from src.skills_extractor import extract_skills
from src.qualifications_extractor import extract_qualifications
from src.field_of_study_extractor import extract_fields_of_study
from src.institution_extractor import extract_institutions
from src.experience_extractor import extract_experience


def extract_candidate_profile(cv_text):
    """
    Extract a structured candidate profile from CV text.

    Extracts:
    - Skills
    - Qualifications
    - Fields of study
    - Educational institutions
    - Work experience
    """

    if not isinstance(cv_text, str) or not cv_text.strip():
        raise ValueError("CV text cannot be empty.")

    profile = {
        "skills": extract_skills(cv_text),
        "qualifications": extract_qualifications(cv_text),
        "fields_of_study": extract_fields_of_study(cv_text),
        "institutions": extract_institutions(cv_text),
        "experience": extract_experience(cv_text),
    }

    return profile
