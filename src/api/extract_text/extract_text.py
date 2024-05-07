import io
from docx import Document
from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from src.ocr.arabic_ocr import extract_text_from_image

router = APIRouter()

@router.post("/extract-text-pdf")
async def extract_text_endpoint(pdf_file: UploadFile = File(...)):
    """
    Extracts text from a PDF file using OCR configured for Arabic language.
    
    Args:
        pdf_file (UploadFile): The PDF file to extract text from.
        
    Returns:
        JSONResponse: A JSON response containing the extracted text.
    """
    
    if not pdf_file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, detail="Invalid file format. Please upload a PDF file.")

    try:
        extracted_texts = extract_text_from_image(await pdf_file.read())
        return JSONResponse(content={"extracted_texts": extracted_texts})
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))


@router.post("/extract-text-word")
async def upload_word_func(file: UploadFile = File(...)):
    """
    This function receives a .docx file, reads its content, and extracts the text from it.

    The function first checks if the uploaded file is a .docx file. If not, it raises an HTTPException with a status code of 400 and an error message. 
    If the file is a .docx file, it reads the content of the file into a bytes object and uses the Document 
    class from the docx module to load the Word file.

    It then iterates over all the paragraphs in the document, extracts the text from each paragraph, and 
    appends it to a list. The list of strings is then joined into a single string with a newline character 
    ("\n") as the separator.

    The function returns a JSONResponse containing a dictionary with the filename and the extracted text.

    Args:
        file (UploadFile): The .docx file to be processed.

    Returns:
        JSONResponse: A JSON response containing a dictionary with the filename and the extracted text.
    """
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="This service only supports .docx files.")

    try:
        content = await file.read()
        document = Document(io.BytesIO(content))

        extracted_texts = [{'page_number': i+1, 'text': para.text}
                           for i, para in enumerate(document.paragraphs) if para.text.strip()]
        return JSONResponse(content={"extracted_texts": extracted_texts})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
