from pymongo import MongoClient
from dotenv import load_dotenv
import os
from src.model.idea import Idea

load_dotenv()


class DataAction:
    """
    Enum for the type of data action that was performed on the database.
    
    Attributes:
        INSERT (str): Insert a new record into the database.
        UPDATE (str): Update an existing record in the database.
        DELETE (str): Delete an existing record from the database.
        FAILED (str): The action failed.
        NOOP (str): No operation was performed.
    """
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    FAILED = "failed"
    NOOP = "noop"

class DBConnection:
    # Connection URI for Cosmos DB MongoDB API
    # MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_URI = "mongodb+srv://khaledbahaa2012:a0RycYZtfXQnRfqB@cluster0.oli8qgt.mongodb.net/"
    DB_NAME = "Grad"

    def __init__(self, uri: str = None):
        if uri == None:
            uri = self.MONGODB_URI

        # Connect to the Cosmos DB MongoDB API
        self.client = MongoClient(uri)

        # Access the database
        self.db = self.client[self.DB_NAME]

        if not DBConnection.indexed:
            self.reindex()
            DBConnection.indexed = True

    def get_collection(self, collection_name: str):
        db_collection = self.db.get_collection(collection_name)
        return db_collection
