from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import os 
from src.nlp.plagiarism_checker.builder import add_embeddings
from src.db.insert_book import insert_document_with_file
from src.model.pydantic_model import BookAuthorPipeline
from src.ocr.arabic_ocr import extract_text_from_image
from src.nlp.restricted_topic_detection.JAIS_detection import get_restricted_content_prediction
import io
from docx import Document
import shutil
from tempfile import NamedTemporaryFile
from typing import List


router = APIRouter()


def extract_text_from_pdf(file_path: str):
    """
    Extracts text from a PDF file located at the given path using OCR configured for Arabic language.
    """
    file_path = file_path.replace("%2F", "\\")

    try:
        with open(file_path, "rb") as file:
            extracted_texts = extract_text_from_image(file.read())
        return {"extracted_texts": extracted_texts}
    except ValueError as ve:
        return None

def extract_text_from_word(file_path: str):
    """
    Extracts text from a Word (.docx) file located at the given path.
    """
    file_path = file_path.replace("%2F", "\\")
    
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

        return {"extracted_texts": extracted_texts}
    except Exception as e:
        return None

def add_restricted_topics_flag(text_objects: dict):
    """
    Adds a 'is_safe' flag to each paragraph in the 'extracted_texts' list of the given 'text_objects' dictionary.
    The 'is_safe' flag indicates whether the paragraph contains restricted content or not.

    Parameters:
    - text_objects (dict): A dictionary containing text objects.

    Returns:
    - None
    """
    for paragraph in text_objects["extracted_texts"]:
        if get_restricted_content_prediction(paragraph["text"]) == 1:
            paragraph["is_safe"] = False
        else:
            paragraph["is_safe"] = True
        
    return text_objects


@router.post("/author-pipeline")
async def author_pipeline(book: BookAuthorPipeline):
    """
    Endpoint for processing a book file and inserting it into the database.

    Args:
        book (Book): The book data.

    Returns:
        JSONResponse: The response containing the book ID if successful, or an error message if unsuccessful.

    Raises:
        400: If the file format is not supported. Only PDF and Word files are supported.
        500: If an error occurs while processing the file.

    Notes:
        - This endpoint expects a POST request with multipart/form-data containing the file and metadata about the book.
    """
    # Check file type
    valid_extensions = ('.pdf', '.docx')
    file_extension = os.path.splitext(book.file.filename)[1]
    if file_extension not in valid_extensions:
        raise HTTPException(
            status_code=400, detail="Unsupported file format. Please upload a PDF or Word file.")

    # Create a temporary file
    with NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        shutil.copyfileobj(book.file.file, temp_file)
        temp_file_path = temp_file.name

    # Process the file based on its type
    try:
        if file_extension == '.pdf':
            text_objects = extract_text_from_pdf(file_path=temp_file_path)
        elif file_extension == '.docx':
            text_objects = extract_text_from_word(file_path=temp_file_path)

        plaintext = "".join(paragraph["text"]
                            for paragraph in text_objects["extracted_texts"])

        # Add restricted topics flag and embeddings
        text_objects = add_restricted_topics_flag(text_objects)
        document_semantic_info = add_embeddings(text_objects)

        # Insert into the database
        book_id = insert_document_with_file(file_path=temp_file_path, file_type=file_extension[1:], title=book.title, authors_ids=book.authors_ids,
                                            plaintext=plaintext, book_summary=book.book_summary, is_published=False, document_semantic_info=document_semantic_info)

        # Clean up the temporary file
        os.remove(temp_file_path)

        return JSONResponse(content={"book_id": str(book_id)}, status_code=200)
    except Exception as e:
        # Ensure the temporary file is cleaned up in case of failure
        os.remove(temp_file_path)
        raise HTTPException(
            status_code=500, detail=f"An error occurred while processing the file: {str(e)}")
