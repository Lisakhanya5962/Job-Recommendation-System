from src.cv_parser import extract_text_from_pdf, extract_text_from_docx

pdf_path = input("Enter the path to a PDF CV: ").strip('"')
docx_path = input("Enter the path to a DOCX CV: ").strip('"')

print("\n========== PDF CV TEXT ==========")

try:
    pdf_text = extract_text_from_pdf(pdf_path)
    print(pdf_text[:1000])
    print("\nPDF extraction successful!")
except Exception as e:
    print(f"PDF extraction failed: {e}")

print("\n========== DOCX CV TEXT ==========")

try:
    docx_text = extract_text_from_docx(docx_path)
    print(docx_text[:1000])
    print("\nDOCX extraction successful!")
except Exception as e:
    print(f"DOCX extraction failed: {e}")