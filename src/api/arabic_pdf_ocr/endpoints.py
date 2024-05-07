# from fastapi import APIRouter
# from fastapi import File, UploadFile, Path
# from src.ocr.arabic_pdf_ocr import arabic_pdf_ocr


# router = APIRouter()

# @router.get("/arabic-pdf-ocr")
# async def upload_pdf(input_file_path: str):
#     """
#     Uploads a PDF file and performs Arabic OCR on it.

#     Args:
#         input_file_path (str): The path to the input PDF file.

#     Returns:
#         str: The result of the Arabic OCR process.
#     """
#     input_file_path = input_file_path.replace("%5C", "\\")

#     result = arabic_pdf_ocr(input_file_path)
    

#     return result

