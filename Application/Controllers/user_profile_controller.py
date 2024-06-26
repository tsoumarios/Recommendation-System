from typing import List, Dict
from pymongo import MongoClient, errors


# Function to insert new user profiles and skip existing ones
def upload_user_profiles(new_profiles: List[Dict], db_uri: str, db_name: str, collection_name: str) -> int:
    try:
        # Connect to MongoDB
        client = MongoClient(db_uri)
        db = client[db_name]
        collection = db[collection_name]
        
        # Track number of documents inserted
        documents_inserted = 0
        
        # Iterate through new_profiles and insert if not already exists
        for profile in new_profiles:
            # Ensure profile is a dictionary
            if not isinstance(profile, dict):
                raise ValueError("Each profile should be a dictionary")

            # Define query to check existence based on userid
            query = {'userid': profile['userid']}
            
            # Check if document already exists
            existing_profile = collection.find_one(query)
            
            if existing_profile:
                # Document already exists, skip insertion
                print(f"User profile already exists, skipping: {profile['userid']}")
            else:
                # Insert new profile
                collection.insert_one(profile)
                documents_inserted += 1
                print(f"Inserted new user profile: {profile['userid']}")
        
        print(f"Total user profiles inserted: {documents_inserted}")
    
    except errors.ConnectionFailure as e:
        print(f"Connection error: {e}")
    except errors.OperationFailure as e:
        print(f"Operation failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
    
    return documents_inserted
