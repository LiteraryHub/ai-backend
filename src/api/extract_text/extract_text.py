import os
import io
from docx import Document
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from src.ocr.arabic_ocr import extract_text_from_image

router = APIRouter()

@router.get("/extract-text-pdf")
async def extract_text_from_pdf(file_path: str = Query(..., description="The path to the PDF file")):
    """
    Extracts text from a PDF file located at the given path using OCR configured for Arabic language.
    """
    if not file_path.endswith('.pdf') or not os.path.exists(file_path):
        raise HTTPException(
            status_code=400, detail="Invalid file format or file does not exist. Please provide a valid PDF file path.")

    try:
        with open(file_path, "rb") as file:
            extracted_texts = extract_text_from_image(file.read())
        return JSONResponse(content={"extracted_texts": extracted_texts})
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))


@router.get("/extract-text-word")
async def extract_text_from_word(file_path: str = Query(..., description="The path to the Word file")):
    """
    Extracts text from a Word (.docx) file located at the given path.
    """
    # Validate file path and extension
    if not file_path.endswith(".docx") or not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Invalid file format or file does not exist. Please provide a valid Word file path.")

    try:
        # Open and read the Word file
        with open(file_path, "rb") as file:
            content = file.read()
            document = Document(io.BytesIO(content))

        # Extract texts with paragraph index and page numbers
        extracted_texts = []
        paragraph_index = 0
        for para in document.paragraphs:
            if para.text.strip():  # Ensure the paragraph contains text
                extracted_texts.append({
                    'paragraph_index': paragraph_index,
                    # Page numbers are not directly available in .docx
                    'page_number': 'Not directly available',
                    'text': para.text
                })
                paragraph_index += 1

        return JSONResponse(content={"extracted_texts": extracted_texts})
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
