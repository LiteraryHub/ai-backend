from src.db.mongodb_connection import DBConnection
import gridfs
import bson
import datetime


def insert_document_with_file(file_path, file_type, title: str, authors_ids: list, plaintext: str, book_summary: str, is_published: bool, document_semantic_info: list):
    mongodb_connection = DBConnection()
    db = mongodb_connection.get_db()
    collection = mongodb_connection.get_collection("book")
    fs = gridfs.GridFS(db)

    # Read the file
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Store the file in GridFS
    file_id = fs.put(file_data, filename=file_path.split('/')[-1], contentType=file_type)

    book_object = {
        "file_id": bson.ObjectId(file_id),
        "title": title,
        "authors_ids": authors_ids,
        "timestamp": datetime.datetime.now(),
        "plaintext": plaintext,
        "book_summary": book_summary,
        "is_published": is_published,
        "document_semantic_info": document_semantic_info,
        "uploaded_file_type": file_type,
        "audiobook": None,
        "book_cover": None,
        "publishers_ids": None,
        "price": None,
        "rate": None,
        "publishing_timestamp": None
    }
    

    try:
        # Insert the JSON document with the file reference
        book_id = collection.insert_one(book_object).inserted_id
        return book_id
    except:
        return None