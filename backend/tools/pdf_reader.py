import PyPDF2
import os
from docx import Document   

def read_pdf_with_pages(pdf_path: str) -> list:
    """
    Returns list of dicts with text and page number
    instead of one big string
    """
    print(f"📖 Reading PDF: {pdf_path}")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append({
                    "text"    : text,
                    "page_num": page_num + 1
                })

    print(f"✅ PDF read — {len(pages)} pages extracted")
    return pages




def read_docx_with_pages(docx_path: str) -> list:
    """
    Reads DOCX and returns list of dicts
    (page_num is approximated since DOCX has no real pages)
    """
    print(f"📖 Reading DOCX: {docx_path}")

    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"DOCX not found: {docx_path}")

    doc = Document(docx_path)

    pages = []
    current_text = ""
    page_num = 1
    approx_page_size = 800  # characters per "page"

    for para in doc.paragraphs:
        text = para.text.strip()

        if not text:
            continue

        current_text += text + "\n"

        # simulate page break
        if len(current_text) >= approx_page_size:
            pages.append({
                "text": current_text.strip(),
                "page_num": page_num
            })
            current_text = ""
            page_num += 1

    # last page
    if current_text.strip():
        pages.append({
            "text": current_text.strip(),
            "page_num": page_num
        })

    print(f"✅ DOCX read — {len(pages)} pages (approx)")
    return pages




def read_document(file_path: str) -> list:
    """
    Single unified function.
    Automatically detects PDF or DOCX from extension.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return read_pdf_with_pages(file_path)
    elif ext in [".docx", ".doc"]:
        return read_docx_with_pages(file_path)
    else:
        raise ValueError(
            f"Unsupported file type: {ext}. "
            f"Only PDF and DOCX are supported."
        )