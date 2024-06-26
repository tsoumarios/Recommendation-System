# Import clustering and preprocessing classes
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

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
