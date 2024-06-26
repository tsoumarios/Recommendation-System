# Betting Recommendation System
## Project requirements
Python version: 3.12

## Database
MongoDB
- **db_name**: bets_db
- **collections**:
    - bets
    - user_profiles   

### Project files
- main.py - API
- connection.py - Connect with MongoDB
- clustering.py - Clustering model
- data_statistics.py - Culculate statistics for the dataset
- preprocessing.py - Perform preprossecing to the dataset
- Controllers
    - bet_controller.py - handles all functionality to interact with the bets like: 
        - upload_dataset(bets)
        - recommend_bets (for a userid)
        - recommend_bets_for_all_users
        - delete_bets_in_period
    - user_profile_controller.py
        - upload_user_profiles (the result of the clustering)
- requirements.txt - All the dependencies that are necesary for the project
- readme.txt - Documendation of the project
- uploaded_data.json - Sample file for demonstration (Contains user profiles, created from clustering and used for generate recommendations)

### Dependencies in the requirements.txt 
- fastapi
- uvicorn
- pandas
- matplotlib
- seaborn
- numpy
- typing
- scikit-learn
- datetime
- pymongo

### Commands to execute
- pip install -r requirements.txt
- python -m uvicorn main:app --reload

### API 
- /upload_json - Post route to upload new dataset. Supports only .json format.
    If there is not dataset (uploaded_data.json), after uploading the new one it will saved in a file named uploaded_data.json.
    Otherwise, it will merge the old and the new dataset and it will save the merged one in the uploaded_data.json file. 
- /recommend/all - Get route that returns recommendations for all users.
- /recommend/{userid} - Get route that returns recommendations for a userid.
- /delete_bets/ - Delete route to delete bet in a specific date range (ISO 8601 format, e.g., 2024-04-01T00:00:00)
Example of parameters:
    - start_date: Start date of the period (ISO 8601 format, e.g., 2024-04-01T00:00:00)
    - end_date: End date of the period (ISO 8601 format, e.g., 2024-04-15T23:59:59)
