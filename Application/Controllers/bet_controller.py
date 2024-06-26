from typing import List, Dict
from pymongo import MongoClient, errors
import json
import numpy as np

# Function to merge or skip documents based on uniqueness
def upload_dataset(new_data: List[Dict], db_uri: str, db_name: str, collection_name: str) -> int:
    try:
        # Connect to MongoDB
        client = MongoClient(db_uri)
        db = client[db_name]
        collection = db[collection_name]
        
        # Track number of documents inserted
        documents_inserted = 0
        
        # Iterate through new_data and insert/update if not already exists
        for entry in new_data:
            # Define query to check existence based on unique fields
            query = {'userid': entry['userid'], 'time': entry['time']}
            if 'match_id' in entry:
                query['match_id'] = entry['match_id']
            
            # Check if document already exists
            existing_doc = collection.find_one(query)
            
            if existing_doc:
                # Document already exists, skip insertion/update
                print(f"Document already exists, skipping: {entry}")
            else:
                # Insert new document
                collection.insert_one(entry)
                documents_inserted += 1
                print(f"Inserted new document: {entry}")
        
        print(f"Total documents inserted: {documents_inserted}")
        return collection
    
    except errors.ConnectionFailure as e:
        print(f"Connection error: {e}")
    except errors.OperationFailure as e:
        print(f"Operation failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()


# Single user recommendations
def recommend_bets(user_id, user_profiles, df, target_features):
    user_cluster = user_profiles[user_profiles['userid'] == user_id]['cluster'].values[0]
    similar_users = user_profiles[user_profiles['cluster'] == user_cluster]['userid'].values
    user_bets = df[df['userid'] == user_id]['match_id'].unique()
    similar_users_bets = df[df['userid'].isin(similar_users) & ~df['match_id'].isin(user_bets)]
    recommendations = {}
    for feature in target_features:
        recommended_bets = similar_users_bets[feature].value_counts().head(3).index.tolist()
        recommendations[feature] = recommended_bets
    return recommendations

# Recommendations for all users
def recommend_bets_for_all_users(user_profiles, df, target_features):
    all_users_results = []
    user_ids = user_profiles['userid'].unique()
    for user_id in user_ids:
        try:
            user_cluster = user_profiles[user_profiles['userid'] == user_id]['cluster'].values[0]
            similar_users = user_profiles[user_profiles['cluster'] == user_cluster]['userid'].values
            user_bets = df[df['userid'] == user_id]['match_id'].unique()
            similar_users_bets = df[df['userid'].isin(similar_users) & ~df['match_id'].isin(user_bets)]
            
            recommendations = {'userid': int(user_id)}  # Ensure user_id is a native int
            for feature in target_features:
                recommended_bets = similar_users_bets[feature].value_counts().head(3).index.tolist()
                recommendations[feature] = [int(x) if isinstance(x, np.integer) else x for x in recommended_bets]
            
            all_users_results.append(recommendations)
        except Exception as e:
            print(f"Error processing user_id {user_id}: {e}")
    all_users_results_json = json.dumps(all_users_results, ensure_ascii=False)
    return all_users_results_json

# Delete bets of a dataset for a date range 
def delete_bets_in_period(collection_name: str, start_date: str, end_date: str, db_uri: str, db_name: str) -> int:
    try:
        # Connect to MongoDB
        client = MongoClient(db_uri)
        db = client[db_name]
        collection = db[collection_name]
        
        # # Convert string dates to datetime objects
        # start_dt = datetime.fromisoformat(start_date)
        # end_dt = datetime.fromisoformat(end_date)
        
        # Define query to match documents within the date range
        query = {
            'time': {
                '$gte': start_date,
                '$lte': end_date
            }
        }
        
        # Delete matching documents
        result = collection.delete_many(query)

        deleted_count = result.deleted_count
        
        print(f"Deleted {deleted_count} documents from {collection_name} collection.")
    
    except errors.ConnectionFailure as e:
        print(f"Connection error: {e}")
    except errors.OperationFailure as e:
        print(f"Operation failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

    return deleted_count

