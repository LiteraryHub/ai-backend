from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import PlainTextResponse
from docx import Document
import io

router = APIRouter()

@router.post("/upload-word")
async def upload_word_func(file: UploadFile = File(...)):
    """
    This function receives a .docx file, reads its content, and extracts the text from it.

    The function first checks if the uploaded file is a .docx file. If not, it returns an error message. 
    If the file is a .docx file, it reads the content of the file into a bytes object and uses the Document 
    class from the docx module to load the Word file.

    It then iterates over all the paragraphs in the document, extracts the text from each paragraph, and 
    appends it to a list. The list of strings is then joined into a single string with a newline character 
    ("\n") as the separator.

    The function returns a dictionary containing the filename and the extracted text.

    Parameters:
    file (UploadFile): The .docx file to be processed.

    Returns:
    dict: A dictionary with the filename and the extracted text.
    """
    if not file.filename.endswith(".docx"):
        return {"error": "This service only supports .docx files."}

    # Access the file name
    filename = file.filename

    # Load the Word file
    content = await file.read()
    document = Document(io.BytesIO(content))

    # Extract text
    full_text = []
    for para in document.paragraphs:
        full_text.append(para.text)

    # Join the list of strings into a single string
    result_text = "\n".join(full_text)

    # Return both the file name and the extracted text
    return {"filename": filename, "text": result_text}
