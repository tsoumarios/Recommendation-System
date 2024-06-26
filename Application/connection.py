import pymongo
from pymongo.errors import ConnectionFailure, PyMongoError, ServerSelectionTimeoutError
from pymongo.collection import Collection

uri="mongodb://localhost:27017/"
db_name="bets_db"

def get_mongo_collection(collection_name)-> Collection:
    
    try:
        # Initialize the MongoClient
        mongo_client = pymongo.MongoClient(uri)
        
        # Ping the server to check the connection
        mongo_client.admin.command('ping')
        print("Ping successful. MongoDB connection is active.")
        
        # Select the database
        db = mongo_client[db_name]
        print(f"Selected Database: {db_name}")
        
        # Select the collection
        collection = db[collection_name]
        print(f"Selected Collection: {collection_name}")
        
        return collection  # Return the collection object
        
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
    except PyMongoError as e:
        print(f"PyMongo error: {e}")
    except ServerSelectionTimeoutError as e:
        print(f"Server selection error: {e}")
    return None  # Return None if connection failed
