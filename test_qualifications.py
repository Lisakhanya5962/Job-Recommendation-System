
from src.cv_parser import extract_text_from_pdf
from src.qualifications_extractor import extract_qualifications


cv_path = input("Enter PDF CV path: ").strip().strip('"')

cv_text = extract_text_from_pdf(cv_path)

qualifications = extract_qualifications(cv_text)

print("\n========== EXTRACTED QUALIFICATIONS ==========")

if qualifications:
    for qualification in qualifications:
        print("-", qualification)
else:
    print("No qualifications identified.")

print("\nTotal qualifications identified:", len(qualifications))

