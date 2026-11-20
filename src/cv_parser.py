
from io import BytesIO

import pymupdf
from docx import Document


def extract_text_from_pdf(file_source):
    """
    Extract text from a PDF file.

    Supports:
    - A file path
    - Uploaded PDF bytes
    """

    if isinstance(file_source, bytes):
        pdf = pymupdf.open(
            stream=file_source,
            filetype="pdf"
        )
    else:
        pdf = pymupdf.open(file_source)

    try:
        text = []

        for page in pdf:
            text.append(page.get_text())

        return "\n".join(text)

    finally:
        pdf.close()


def extract_text_from_docx(file_source):
    """
    Extract text from a Word document.

    Supports:
    - A file path
    - Uploaded DOCX bytes
    """

    if isinstance(file_source, bytes):
        document = Document(BytesIO(file_source))
    else:
        document = Document(file_source)

    text = []

    # Extract paragraphs.
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    # Extract table content.
    for table in document.tables:
        for row in table.rows:
            row_text = [
                cell.text.strip()
                for cell in row.cells
                if cell.text.strip()
            ]

            if row_text:
                text.append(" | ".join(row_text))

    return "\n".join(text)
