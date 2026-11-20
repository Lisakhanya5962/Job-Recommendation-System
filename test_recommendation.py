
from src.cv_parser import extract_text_from_pdf
from src.skills_extractor import extract_skills
from src.recommendation_engine import generate_recommendations


# Candidate CV
cv_path = input("Enter candidate CV path: ").strip('"')

# Extract CV text
cv_text = extract_text_from_pdf(cv_path)

# Extract candidate skills
candidate_skills = extract_skills(cv_text)

print("\n========== CANDIDATE SKILLS ==========")

for skill in candidate_skills:
    print("-", skill)

# Generate recommendations
recommendations = generate_recommendations(candidate_skills)

print("\n========== JOB RECOMMENDATIONS ==========")

if not recommendations:
    print("No vacancies currently available.")

for job in recommendations:

    print("\nJob:", job["job_title"])
    print("Company:", job["company"])
    print("Location:", job["location"])
    print("Match:", str(job["match_percentage"]) + "%")
    print("Matched skills:", job["matched_skills"])
    print("Missing skills:", job["missing_skills"])
