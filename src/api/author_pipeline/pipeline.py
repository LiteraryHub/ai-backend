from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os 
from src.nlp.plagiarism_checker.builder import add_embeddings
from src.db.insert_book import insert_document_with_file
from src.model.pydantic_model import Book
from src.ocr.arabic_ocr import extract_text_from_image
import io
from docx import Document

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


@router.post("/author-pipeline")
async def author_pipeline(payload: Book):
    """
    Endpoint for processing a book file and inserting it into the database.

    Args:
        payload (Book): The payload containing information about the book. It should be an instance of the `Book` class.

    Returns:
        JSONResponse: The response containing the book ID if successful, or an error message if unsuccessful.

    Raises:
        404: If the file specified in the payload does not exist.
        400: If the file format is not supported. Only PDF and Word files are supported.
        500: If an error occurs while processing the file.

    Notes:
        - This endpoint expects a POST request with a JSON payload containing information about the book.
        - The payload should include the following fields:
            - `file_path` (str): The path to the book file.
            - `title` (str): The title of the book.
            - `authors_ids` (List[int]): The IDs of the authors of the book.
            - `book_summary` (str): A summary of the book.

    Example Usage:
        ```
        import requests

        payload = {
            "file_path": "/path/to/book.pdf",
            "title": "My Book",
            "authors_ids": [1, 2],
            "book_summary": "This is a book about..."
        }

        response = requests.post("http://localhost:8000/author-pipeline", json=payload)
        print(response.json())
        ```

    """
    file_path = payload.file_path.replace("%2F", "\\")
    print(file_path)
    # Check file existence and validate format
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content="File not found. Please provide a valid file path.")

    file_type = None
    
    if file_path.endswith('.pdf'):
        file_type = "pdf"
        text_objects = extract_text_from_pdf(file_path=file_path)
    elif file_path.endswith('.docx'):
        file_type = "docx"
        text_objects = extract_text_from_word(file_path=file_path)
    else:
        return JSONResponse(status_code=400, content="Unsupported file format. Please provide a PDF or Word file.")


    try:
        plaintext = ""
        for paragraph in text_objects["extracted_texts"]:
            plaintext += paragraph["text"]
            
        # Add embeddings to the extracted text (to use in the plagiarism checker) and return the result
        # TODO: Implement add the restricted topics boolean flag for each paragraph in the response.
        document_semantic_info = add_embeddings(text_objects)
        
        book_id = insert_document_with_file(file_path=payload.file_path, file_type=file_type, title=payload.title, authors_ids=payload.authors_ids,
                                            plaintext=plaintext, book_summary=payload.book_summary, is_published=False, document_semantic_info=document_semantic_info)
        
        return JSONResponse(content={"book_id": book_id}, status_code=200)
    except Exception as e:
        return JSONResponse(status_code=500, content=f"An error occurred while processing the file: {str(e)}")