
def calculate_match(candidate_skills, required_skills):
    """
    Calculate the percentage match between
    candidate skills and job requirements.
    """

    candidate_skills = {
        skill.strip().lower()
        for skill in candidate_skills
    }

    required_skills = {
        skill.strip().lower()
        for skill in required_skills
    }

    if not required_skills:
        return {
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": []
        }

    matched_skills = candidate_skills.intersection(
        required_skills
    )

    missing_skills = required_skills - candidate_skills

    percentage = (
        len(matched_skills) / len(required_skills)
    ) * 100

    return {
        "match_percentage": round(percentage, 2),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }


def recommend_jobs(candidate_skills, jobs):
    """
    Compare candidate skills against multiple jobs
    and rank jobs from highest to lowest match.
    """

    recommendations = []

    for job in jobs:

        result = calculate_match(
            candidate_skills,
            job["required_skills"]
        )

        recommendations.append({
            "job_title": job["title"],
            "company": job["company"],
            **result
        })

    recommendations.sort(
        key=lambda job: job["match_percentage"],
        reverse=True
    )

    return recommendations
