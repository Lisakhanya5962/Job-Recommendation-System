
from src.database import get_all_jobs
from src.job_matcher import calculate_match


def generate_recommendations(candidate_skills):
    """
    Retrieve jobs from the database,
    compare candidate skills and rank vacancies.
    """

    jobs = get_all_jobs()

    recommendations = []

    for job in jobs:

        result = calculate_match(
            candidate_skills,
            job["required_skills"]
        )

        recommendations.append({
            "job_id": job["id"],
            "job_title": job["title"],
            "company": job["company"],
            "location": job["location"],
            **result
        })

    recommendations.sort(
        key=lambda job: job["match_percentage"],
        reverse=True
    )

    return recommendations
