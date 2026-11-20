
from src.job_matcher import recommend_jobs

# Skills extracted from the candidate's CV
candidate_skills = [
    "Communication",
    "Teamwork",
    "Time Management",
    "Animal Production",
    "Animal Care",
    "Reliability",
    "Punctuality"
]

# Sample job vacancies
jobs = [
    {
        "title": "Animal Production Assistant",
        "company": "Green Farms",
        "required_skills": [
            "Animal Production",
            "Animal Care",
            "Teamwork",
            "Communication"
        ]
    },
    {
        "title": "Administrative Assistant",
        "company": "Office Solutions",
        "required_skills": [
            "Communication",
            "Microsoft Office",
            "Time Management",
            "Data Entry"
        ]
    },
    {
        "title": "Farm Worker",
        "company": "Fresh Harvest",
        "required_skills": [
            "Animal Care",
            "Reliability",
            "Teamwork",
            "Punctuality"
        ]
    }
]

recommendations = recommend_jobs(
    candidate_skills,
    jobs
)

print("\n========== JOB RECOMMENDATIONS ==========")

for job in recommendations:
    print("\nJob:", job["job_title"])
    print("Company:", job["company"])
    print("Match:", str(job["match_percentage"]) + "%")
    print("Matched skills:", job["matched_skills"])
    print("Missing skills:", job["missing_skills"])
