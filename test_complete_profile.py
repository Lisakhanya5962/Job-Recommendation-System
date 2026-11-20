
from src.candidate_profile_extractor import extract_candidate_profile


sample_cv = """
PERSONAL INFORMATION

WORK EXPERIENCE

IT Intern
Frontier Hospital
January 2025 - December 2025

- Provided technical user support.
- Troubleshot hardware and software problems.
- Assisted with computer maintenance.
- Logged technical incidents.

EDUCATION

Diploma in Information Technology
Nelson Mandela University

SKILLS

Python
Networking
Communication
Teamwork
"""

profile = extract_candidate_profile(sample_cv)

for category, values in profile.items():

    print(f"\n{category.upper()}")

    for value in values:
        print("-", value)

print("\nCOMPLETE PROFILE EXTRACTION SUCCESSFUL!")
