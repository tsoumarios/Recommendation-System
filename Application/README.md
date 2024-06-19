# Project requirements
Python version: 3.12

# Project files
- main.py - API
- clustering.py - Clustering code
- merge_json.py - Functions to merge json datasets
- uploaded_data.json - Dataset
- user_profiles.json - Contains user profiles, created from clustering and will used for generate recommendations
- requirements.txt - All the dependencies that are necesary for the project
- readme.txt - Documendation of the project

# Dependencies in the requirements.txt 
- fastapi
- uvicorn
- pandas
- matplotlib
- seaborn
- numpy
- typing
- scikit-learn
- datetime

# Commands to execute
- pip install -r requirements.txt
- python -m uvicorn main:app --reload

# API 
- /upload_json - Post route to upload new dataset. Supports only .json format.
    If there is not dataset (uploaded_data.json), after uploading the new one it will saved in a file named uploaded_data.json.
    Otherwise, it will merge the old and the new dataset and it will save the merged one in the uploaded_data.json file. 
- /recommend/all - Get route that returns recommendations for all users.
- /recommend/{userid} - Get route that returns recommendations for a userid.
- /delete_bets/ - Delete route to delete bet in a specific date range (ISO 8601 format, e.g., 2024-04-01T00:00:00)
Example of parameters:
    - start_date: Start date of the period (ISO 8601 format, e.g., 2024-04-01T00:00:00)
    - end_date: End date of the period (ISO 8601 format, e.g., 2024-04-15T23:59:59)