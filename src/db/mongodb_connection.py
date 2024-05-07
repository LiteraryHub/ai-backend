from pymongo import MongoClient

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
    
    def get_db(self):
        return self.db
