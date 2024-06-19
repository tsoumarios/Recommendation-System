# Import clustering file
from clustering import preprocess_data, clustering, recommend_bets, recommend_bets_for_all_users, count_unique_users, count_bets, get_date_range, delete_bets_in_period

# Import json merging functions
from merge_json import merge_json_data

# Import FastAPI classes
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

# Import necessary modules
import pandas as pd
import json
import os

# Initialize the API
app = FastAPI()

# Global variables to store the model and data
data = None
user_profiles = None
target_features = ['match_sportId', 'match_categoryId', 'match_tournamentId', 'oddField_oddTypeId']

# Route to upload a new dataset and rerun the model
@app.post("/upload_json/")
async def upload_json(file: UploadFile = File(...)):
    if file.content_type != 'application/json':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JSON file.")

    contents = await file.read()
    new_json_data = json.loads(contents)
    try:

        if os.path.exists('uploaded_data.json'): # if uploaded_data.json is found
            with open('uploaded_data.json', 'r') as f: # open it
                existing_json_data = json.load(f)   
            data = merge_json_data(existing_json_data, new_json_data, 'uploaded_data.json')
            
        else:
            # Save new JSON data to a uploaded_data.json file if old one doesn't exist
            with open('uploaded_data.json', 'w') as json_file:
                json.dump(new_json_data, json_file, ensure_ascii=False, indent=2)
            data = new_json_data    
            
        # Clustering
        # Preproccesing
        clustering_data = preprocess_data(data)
        # Clustering
        user_profiles = clustering(clustering_data)

        # ALS

        # Preproccesing
        
        # Als model

        # Save user profiles
        user_profiles_json = user_profiles.to_json(orient='records', indent=2)
        with open('user_profiles.json', 'w') as json_file:
            json_file.write(user_profiles_json)
        
        new_users = count_unique_users(new_json_data)
        total_users = count_unique_users(data)
        new_bets = count_bets(new_json_data)
        total_bets = count_bets(data)
        new_data_period = get_date_range(new_json_data)
        total_data_period = get_date_range(data)
        
        return {"Message": "JSON file processed successfully", 
                "Descriptive statistics": [{
                    "users_imported" : new_users,
                    "total_users": total_users,
                    "bets_imported" : new_bets,
                    "total_bets": total_bets,
                    "new_data_date_range": new_data_period,
                    "total_date_range": total_data_period
                }],
                "data_preview": data[:5]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing JSON file: {e}")

# Route to get all recommendations
@app.get("/recommend/all")
async def recommend_all():
    try:
        with open('uploaded_data.json', 'r') as f:
            json_data = json.load(f)
        data = preprocess_data(json_data)

        with open('user_profiles.json', 'r') as f:
            json_data = json.load(f)
        user_profiles = pd.json_normalize(json_data)

        all_users_recommendations = recommend_bets_for_all_users(user_profiles, data, target_features)

        # all_users_recommendations = als_recommendation_all()

        return JSONResponse(content=json.loads(all_users_recommendations))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations for all users: {e}")

# Route to get single recommendations for a {user_id}
@app.get("/recommend/{user_id}")
async def recommend(user_id: int):
    try:
        with open('uploaded_data.json', 'r') as f:
            json_data = json.load(f)
        
        data = preprocess_data(json_data)

        with open('user_profiles.json', 'r') as f:
            json_data = json.load(f)
        
        user_profiles = pd.json_normalize(json_data)
        
        recommended_bets = recommend_bets(user_id, user_profiles, data, target_features)
        return JSONResponse(content=[recommended_bets])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Probably user is not exists. Error generating recommendations: {e}")

# Route to delete bets in a date range
@app.delete("/delete_bets/")
async def delete_bets(start_date: str, end_date: str):
    try:
        if os.path.exists('uploaded_data.json'):
            with open('uploaded_data.json', 'r') as f:
                json_data = json.load(f)
        else:
            return {"message": "No data available to delete from."}

        updated_data = delete_bets_in_period(json_data, start_date, end_date)

        # Save the updated data back to the JSON file
        with open('uploaded_data.json', 'w') as json_file:
            json.dump(updated_data, json_file, ensure_ascii=False, indent=2)

        old_total_bets = count_bets(json_data)
        total_bets = count_bets(updated_data)
        deleted_bets_count = old_total_bets - total_bets
        unique_users = count_unique_users(updated_data)
        total_data_period = get_date_range(updated_data)
        return {
            "message": "Bets within the specified period deleted successfully.",
            "total_bets": total_bets,
            "unique_users": unique_users,
            "deleted_bets": deleted_bets_count,
            "total_date_range": total_data_period,
            "data_preview": updated_data[:5]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting bets: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
