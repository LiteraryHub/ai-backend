from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from fastapi import UploadFile


class BookTextBody(BaseModel):
    text: str
    book_name: str
    
class ImageFiles(BaseModel):
    image_files: list

class Book(BaseModel):
    title: str
    book_summary: str
    file_path: str
    authors_ids: List[UUID]

    
class BookAuthorPipeline(BaseModel):
    file: UploadFile
    title: str = Field(default="")
    authors_ids: List[str] = Field(default=[])
    book_summary: str = Field(default="")
