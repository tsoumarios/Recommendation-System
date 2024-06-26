# Import necessary modules
import pandas as pd

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