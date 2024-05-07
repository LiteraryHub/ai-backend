from pydantic import BaseModel

class BookTextBody(BaseModel):
    text: str
    book_name: str
    

class ImageFiles(BaseModel):
    image_files: list