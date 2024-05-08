from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
import requests 
from src.nlp.plagiarism_checker.builder import add_embeddings
from src.db.insert_book import insert_document_with_file
from src.model.pydantic_model import Book

router = APIRouter()

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
    # Check file existence and validate format
    if not os.path.exists(payload.file_path):
        return JSONResponse(status_code=404, detail="File not found. Please provide a valid file path.")

    file_type = None
    
    if payload.file_path.endswith('.pdf'):
        file_type = "pdf"
        response = requests.get(f"http://127.0.0.1/extractor/extract-text-pdf?file_path={payload.file_path}")
    elif payload.file_path.endswith('.docx'):
        file_type = "docx"
        response = requests.get(f"http://127.0.0.1/extractor/extract-text-word?file_path={payload.file_path}")
    else:
        return JSONResponse(status_code=400, detail="Unsupported file format. Please provide a PDF or Word file.")


    try:
        plaintext = ""
        for paragraph in response.json()["extracted_texts"]:
            plaintext += paragraph["text"]
            
        # Add embeddings to the extracted text (to use in the plagiarism checker) and return the result
        # TODO: Implement add the restricted topics boolean flag for each paragraph in the response.
        document_semantic_info = add_embeddings(response.json())
        
        book_id = insert_document_with_file(file_path=payload.file_path, file_type=file_type, title=payload.title, authors_ids=payload.authors_ids,
                                            plaintext=plaintext, book_summary=payload.book_summary, is_published=False, document_semantic_info=document_semantic_info)
        
        return JSONResponse(content={"book_id": book_id}, status_code=200)
    except Exception as e:
        return JSONResponse(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")