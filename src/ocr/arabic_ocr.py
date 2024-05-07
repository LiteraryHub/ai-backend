import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

# Set the default path for local development and use the environment variable for production
# Default path on local Windows machines
default_tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD', default_tesseract_path)
TESSERACT_CONFIG = '--oem 3 --psm 6 -l ara'


def extract_text_from_image(pdf_bytes):
    """
    Extracts text from PDF bytes using OCR configured for Arabic language.

    Args:
        pdf_bytes (bytes): The byte content of a PDF file.

    Returns:
        list[dict]: A list of dictionaries containing the page number and extracted text.
    """
    try:
        doc = fitz.open("pdf", pdf_bytes)
        extracted_texts = []

        for page_number, page in enumerate(doc, start=1):
            # Render the page as an image
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("ppm")  # Convert the pixmap to bytes

            # Load it to PIL
            image = Image.open(io.BytesIO(img_bytes))
            text = pytesseract.image_to_string(image, config=TESSERACT_CONFIG)

            # Add extracted text from the page to the list
            extracted_texts.append({
                'page_number': page_number,
                'text': text
            })

        return extracted_texts

    except Exception as e:
        raise ValueError(f"Failed to extract text due to: {e}")