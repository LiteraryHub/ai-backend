from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.nlp.restricted_topic_detection.JAIS_detection import get_restricted_content_prediction

router = APIRouter()

router.post('/v2/detect', tags=['Restricted Topic Detection'])
async def detect_restricted_content(payload: dict):
    """
    Endpoint for detecting restricted content in a list of extracted texts.

    Args:
        payload (dict): The JSON input containing the extracted texts.

    Returns:
        JSONResponse: The updated JSON input with the restricted content detection results.
    
    Raises:
        HTTPException: If the extracted_texts field is empty.
        
    Examples:
        JSON input:
        {
            "extracted_texts": [
                {"page_number": 1, "paragraph_index": 1, "text": "This is a sample text."},
                {"page_number": 1, "paragraph_index": 2, "text": "This is another sample text."}
            ]
        }

        JSON output:
        {
            "extracted_texts": [
                {"page_number": 1, "paragraph_index": 1, "text": "This is a sample text.", "is_safe": true},
                {"page_number": 1, "paragraph_index": 2, "text": "This is another sample text.", "is_safe": true}
            ]
        }
    """
    # Get the extracted texts from the payload
    extracted_texts = payload.get('extracted_texts', [])

    # Check if the extracted_texts field is empty
    if not extracted_texts:
        raise HTTPException(status_code=400, detail='No extracted texts provided')

    # Get the restricted content prediction for each extracted text
    for text in extracted_texts:
        if get_restricted_content_prediction(text['text']) == 1:
            text['is_safe'] = False
        else:
            text['is_safe'] = True
    
    # Return the updated JSON input
    return JSONResponse(content={'extracted_texts': extracted_texts})