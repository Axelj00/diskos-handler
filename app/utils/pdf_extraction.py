# pdf_extraction.py
import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file) -> str:
    """Extract full text from a PDF file."""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text
