from clustering import clustering
from preprocessing import preprocess_data
from Controllers.bet_controller import upload_dataset, recommend_bets, recommend_bets_for_all_users, delete_bets_in_period
from data_statictics import count_unique_users, count_bets, get_date_range
from Controllers.user_profile_controller import upload_user_profiles

# Import database
from connection import get_mongo_collection, uri, db_name

# Import FastAPI classes
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

# Import necessary modules
import pandas as pd
import json
import os

# Initialize the API
app = FastAPI()


target_features = ['match_sportId', 'match_categoryId', 'match_tournamentId', 'oddField_oddTypeId']

# Fetch the collections
data = get_mongo_collection('bets') 
user_profiles = get_mongo_collection('user_profiles')

# Global variables to store the model and data
dataset = get_mongo_collection('bets')
data =  list(dataset.find({}, {'_id': 0}))
user_profiles_set = get_mongo_collection('user_profiles')
user_profiles =  list(user_profiles_set.find({}, {'_id': 0}))

# Route to upload a new dataset and rerun the model
@app.post("/upload_json/")
async def upload_json(file: UploadFile = File(...)):
    if file.content_type != 'application/json':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JSON file.")

    contents = await file.read()
    new_json_data = json.loads(contents)
    try:
        # Upload new dataset
        upload_dataset(new_json_data, uri, db_name, 'bets')

        totaldata =  list(dataset.find({}, {'_id': 0}))
        # Preproccesing
        processed_data = preprocess_data(totaldata)
        # Clustering
        new_user_profiles = clustering(processed_data)
        new_user_profiles_json = new_user_profiles.to_dict(orient='records')
        # Save user profiles
        upload_user_profiles(new_user_profiles_json, uri, db_name, 'user_profiles')
        
        # New data statistics
        new_users = count_unique_users(new_json_data)
        new_bets = count_bets(new_json_data)
        new_data_period = get_date_range(new_json_data)
        # Collection statistics
        total_users = count_unique_users(totaldata)
        total_bets = count_bets(totaldata)
        total_data_period = get_date_range(totaldata)
        
        return {"Message": "JSON file processed successfully", 
                "Descriptive statistics": [{
                    "users_to_import" : new_users,
                    "total_users": total_users,
                    "bets_to_import" : new_bets,
                    "total_bets": total_bets,
                    "new_data_date_range": new_data_period,
                    "total_date_range": total_data_period
                }],
                "data_preview": totaldata[:5]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing JSON file: {e}")

# Route to get all recommendations
@app.get("/recommend/all")
async def recommend_all():
    try:
        dataset = preprocess_data(data)

        user_profiles_df = pd.json_normalize(user_profiles)

        all_users_recommendations = recommend_bets_for_all_users(user_profiles_df, dataset, target_features)

        return JSONResponse(content=json.loads(all_users_recommendations))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations for all users: {e}")

# Route to get single recommendations for a {user_id}
@app.get("/recommend/{user_id}")
async def recommend(user_id: int):
    try:
        dataset = preprocess_data(data)

        user_profiles_df = pd.json_normalize(user_profiles)
        
        recommended_bets = recommend_bets(user_id, user_profiles_df, dataset, target_features)
        
        return JSONResponse(content=[recommended_bets])
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Probably user is not exists. Error generating recommendations: {e}")

# Route to delete bets in a date range
@app.delete("/delete_bets/")
async def delete_bets(start_date: str, end_date: str):
    try:
        deleted_bets_count = delete_bets_in_period('bets', start_date, end_date, uri, db_name)
        
        totaldata =  list(dataset.find({}, {'_id': 0}))
        total_bets = count_bets(totaldata)
        unique_users = count_unique_users(totaldata)
        total_data_period = get_date_range(totaldata)
        
        return {
            "message": "Bets within the specified period deleted successfully.",
            "total_bets": total_bets,
            "unique_users": unique_users,
            "deleted_dates": [
                {
                    "from": start_date
                }
                 ,{
                     "to": end_date
                 }
            ],
            "deleted_bets_count": deleted_bets_count,
            "total_date_range": total_data_period,
            "data_preview": data[:5]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting bets: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
