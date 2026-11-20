
from src.cv_parser import extract_text_from_pdf
from src.field_of_study_extractor import extract_fields_of_study


cv_path = input("Enter PDF CV path: ").strip().strip('"')

cv_text = extract_text_from_pdf(cv_path)

fields = extract_fields_of_study(cv_text)

print("\n========== EXTRACTED FIELDS OF STUDY ==========")

if fields:
    for field in fields:
        print("-", field)
else:
    print("No fields of study identified.")

print("\nTotal fields identified:", len(fields))
