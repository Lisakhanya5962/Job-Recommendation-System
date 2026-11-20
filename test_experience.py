
from src.experience_extractor import extract_experience


sample_cv = """
PERSONAL INFORMATION

Name: Test Candidate

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
"""

experience = extract_experience(sample_cv)

print("\nEXTRACTED EXPERIENCE")

for item in experience:
    print("-", item)

print("\nTotal extracted lines:", len(experience))
