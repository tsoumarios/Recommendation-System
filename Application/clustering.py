# Import necessary modules
import pandas as pd
import json
import numpy as np

# Import clustering and preprocessing classes
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from typing import List, Dict, Tuple
from datetime import datetime

# Preprocess the data
def preprocess_data(json_data):
    df = pd.json_normalize(json_data, 'bet', ['time', 'userid'])
    df['match_id'] = df['pick'].apply(lambda x: x[0]['match']['id'])
    df['match_dateofmatch'] = df['pick'].apply(lambda x: x[0]['match']['dateofmatch'])
    df['match_home'] = df['pick'].apply(lambda x: x[0]['match']['home'])
    df['match_homeId'] = df['pick'].apply(lambda x: x[0]['match']['homeId'])
    df['match_away'] = df['pick'].apply(lambda x: x[0]['match']['away'])
    df['match_awayId'] = df['pick'].apply(lambda x: x[0]['match']['awayId'])
    df['match_sport'] = df['pick'].apply(lambda x: x[0]['match']['sport'])
    df['match_category'] = df['pick'].apply(lambda x: x[0]['match']['category'])
    df['match_tournament'] = df['pick'].apply(lambda x: x[0]['match']['tournament'])
    df['match_sportId'] = df['pick'].apply(lambda x: x[0]['match']['sportId'])
    df['match_categoryId'] = df['pick'].apply(lambda x: x[0]['match']['categoryId'])
    df['match_tournamentId'] = df['pick'].apply(lambda x: x[0]['match']['tournamentId'])
    df['market_freetext'] = df['pick'].apply(lambda x: x[0]['market']['freetext'])
    df['market_specialoddsvalue'] = df['pick'].apply(lambda x: x[0]['market']['specialoddsvalue'])
    df['market_typeid'] = df['pick'].apply(lambda x: x[0]['market']['typeid'])
    df['oddField_oddTypeId'] = df['pick'].apply(lambda x: x[0]['oddField']['oddTypeId'])
    df['oddField_type'] = df['pick'].apply(lambda x: x[0]['oddField']['type'])
    df['oddField_value'] = df['pick'].apply(lambda x: x[0]['oddField']['value'])
    # Drop the 'pick' column
    df.drop(['pick'], axis=1, inplace=True)
    df['time'] = pd.to_datetime(df['time'])
    df['match_dateofmatch'] = pd.to_datetime(df['match_dateofmatch'])
    return df

# Clustering with Kmeans
def clustering(df):
    user_profiles = df.groupby('userid').agg({
        'stake': ['mean', 'sum', 'count'],
        'match_sport': lambda x: x.mode().iloc[0] if not x.mode().empty else 'unknown',
        'match_tournament': lambda x: x.mode().iloc[0] if not x.mode().empty else 'unknown',
        'oddField_type': lambda x: x.mode().iloc[0] if not x.mode().empty else 'unknown',
        'match_category': lambda x: x.mode().iloc[0] if not x.mode().empty else 'unknown'
    }).reset_index()

    user_profiles.columns = ['userid', 'avg_stake', 'total_stake', 'bet_count', 'favorite_sport', 'favorite_tournament', 'favorite_oddField_type', 'favorite_match_category']
    
    numerical_features = ['avg_stake', 'total_stake', 'bet_count']
    categorical_features = ['favorite_sport', 'favorite_tournament', 'favorite_oddField_type', 'favorite_match_category']
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ]
    )
    pipeline = Pipeline(steps=[('preprocessor', preprocessor)])
    user_profiles_transformed = pipeline.fit_transform(user_profiles)
    kmeans = KMeans(n_clusters=3, random_state=42)
    user_profiles['cluster'] = kmeans.fit_predict(user_profiles_transformed)
    return user_profiles

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
def delete_bets_in_period(data: List[Dict], start_date: str, end_date: str) -> List[Dict]:
    # Convert string dates to datetime objects for comparison
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    # Filter out bets outside the date range
    filtered_data = [
        entry for entry in data 
        if not start_dt <= datetime.fromisoformat(entry['time']) <= end_dt
    ]
    return filtered_data

# Count users
def count_unique_users(data: List[Dict]) -> int:
    unique_users = {entry['userid'] for entry in data if 'userid' in entry}
    return len(unique_users)

# Count bets
def count_bets(data: List[Dict]) -> int:
    total_bets = 0
    for entry in data:
        if 'bet' in entry and isinstance(entry['bet'], list):
            total_bets += len(entry['bet'])
    return total_bets

# Get date range of a dataset
def get_date_range(data: List[Dict]) -> Tuple[str, str]:
    dates = [entry['time'] for entry in data if 'time' in entry]
    if not dates:
        return None, None
    min_date = {"From": min(dates)}
    max_date = {"To": max(dates)}
    return min_date, max_date

