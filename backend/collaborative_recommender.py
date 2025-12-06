# collaborative_recommender.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeRecommender:
    def __init__(self):
        self.ratings = pd.read_csv('ratings.csv')
        self.movies = pd.read_csv('movies.csv')
        
        # Create user-item matrix
        self.user_movie_matrix = self.ratings.pivot_table(
            index='userId',
            columns='movieId',
            values='rating'
        ).fillna(0)
        
        # Calculate user similarity
        self.user_similarity = cosine_similarity(self.user_movie_matrix)
        self.user_similarity_df = pd.DataFrame(
            self.user_similarity,
            index=self.user_movie_matrix.index,
            columns=self.user_movie_matrix.index
        )
    
    def get_recommendations(self, user_id, n=10):
        # Find similar users
        similar_users = self.user_similarity_df[user_id].sort_values(ascending=False)[1:11]
        
        # Get movies rated by similar users
        similar_user_ids = similar_users.index
        
        # Find movies user hasn't seen
        user_movies = self.ratings[self.ratings['userId'] == user_id]['movieId'].values
        
        # Get recommendations from similar users
        recommendations = self.ratings[
            (self.ratings['userId'].isin(similar_user_ids)) &
            (~self.ratings['movieId'].isin(user_movies))
        ]
        
        # Calculate weighted average rating
        top_movies = recommendations.groupby('movieId')['rating'].mean().sort_values(ascending=False)
        
        # Get top N movie IDs
        top_movie_ids = top_movies.head(n).index
        
        # Return movie titles
        return self.movies[self.movies['movieId'].isin(top_movie_ids)]['title'].tolist()

# Test it
collab_recommender = CollaborativeRecommender()
recommendations = collab_recommender.get_recommendations(user_id=1, n=5)
print(recommendations)