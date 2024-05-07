import requests
import os

def test_arabic_pdf_ocr():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "example.pdf")
    url = f"http://localhost:8001/ocr/arabic-pdf-ocr?input_file_path={file_path}"
    
    response = requests.get(url)

    if response.status_code == 200:
        print("OCR successful. Extracted text:")
        print(response.json())
    else:
        print("OCR failed. Error message:")


if __name__ == "__main__":
    test_arabic_pdf_ocr()
