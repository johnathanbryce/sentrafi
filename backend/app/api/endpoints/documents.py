from fastapi import APIRouter, HTTPException, Depends, UploadFile


# deps
from app.auth.dependencies import get_current_user
from app.database import get_db

# services
from app.services.pdf_extraction import extract_document

# schema

router = APIRouter()

# This PR — PDF → Markdown extraction (almost done)
# Next PR — Ledger schema (Transactions, SyncBatches tables)
# Next PR — Ollama transformation (Markdown → structured Pydantic JSON)
# Next PR — sentra sync CLI command (wires it all together: upload → extract → Ollama → store)
# Next PR - apply current_user api security constraints
# Next PR - finalize all error handling & security logic


@router.post("/documents/extract", status_code=200)
def extract_pdf_for_analysis(
    pdf_doc: UploadFile,
    # current_user: User = Depends(get_current_user), TODO: restrict api route
):

    # get the raw bytes from the pdf
    pdf_bytes = pdf_doc.file.read()

    # send to service for extraction
    extracted_pdf_details = extract_document(pdf_bytes)
    filename = pdf_doc.filename

    llm_pdf_context = {
        "filename": filename,
        **extracted_pdf_details,
    }
    return llm_pdf_context


# TODO: send to Ollama to parse into structured transactions

# TODO: send structured output from ollama to db
