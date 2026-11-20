
from src.cv_parser import extract_text_from_pdf
from src.institution_extractor import extract_institutions


cv_path = input("Enter PDF CV path: ").strip().strip('"')

cv_text = extract_text_from_pdf(cv_path)

institutions = extract_institutions(cv_text)

print("\n========== EXTRACTED INSTITUTIONS ==========")

if institutions:
    for institution in institutions:
        print("-", institution)
else:
    print("No known institutions identified.")

print("\nTotal institutions identified:", len(institutions))
