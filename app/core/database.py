from app.core.config import settings
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

class MongoDBService:
    def __init__(self):
        try:
            # URI configuration
            self.uri = settings.mongodb_uri
            self.db_name = settings.mongodb_db_name
            self.collection_name = settings.mongodb_collection_name
            
            # client configuration with timeout
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            
            # test connection
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
        except ServerSelectionTimeoutError as e:
            raise ConnectionError(f" Error connecting to MongoDB: {e}")
    
    def get_collection(self, collection_name=None):
        collection_name = collection_name or self.collection_name
        return self.db[collection_name]
