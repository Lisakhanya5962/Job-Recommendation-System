
from src.cv_parser import extract_text_from_pdf
from src.skills_extractor import extract_skills

cv_path = input("Enter PDF CV path: ").strip('"')

cv_text = extract_text_from_pdf(cv_path)

skills = extract_skills(cv_text)

print("\n========== EXTRACTED SKILLS ==========")

for skill in skills:
    print("-", skill)

print(f"\nTotal skills identified: {len(skills)}")
