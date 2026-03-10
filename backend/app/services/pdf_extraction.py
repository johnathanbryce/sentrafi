import pymupdf4llm
import pymupdf
from fastapi import HTTPException

PDF_SIZE_CAP = 5 * 1024 * 1024  # 5 MB cap


# core pdf extraction module -- takes PDF bytes and returns markdown
def extract_document(pdf_bytes):

    if len(pdf_bytes) > PDF_SIZE_CAP:
        raise HTTPException(
            status_code=413,
            detail="This file is too large: file size exceeds PDF size cap. ",
        )

    if pdf_bytes[:4] != b"%PDF":
        raise HTTPException(
            status_code=400, detail="Invalid file: only PDF documents are supported."
        )

    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    markdown = pymupdf4llm.to_markdown(doc)

    return {
        "markdown": markdown,
        "page_count": doc.page_count,
        "length": len(pdf_bytes),
        "metadata": doc.metadata,
    }
