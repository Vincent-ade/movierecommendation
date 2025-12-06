import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')

# Create user-item matrix
user_movie_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)

# Perform SVD
U, sigma, Vt = svds(csr_matrix(user_movie_matrix.values), k=50)

# Reconstruct predictions
sigma = np.diag(sigma)
predicted_ratings = np.dot(np.dot(U, sigma), Vt)

def get_svd_recommendations(user_id, n=10):
    user_idx = user_movie_matrix.index.get_loc(user_id)
    user_predictions = predicted_ratings[user_idx, :]
    
    # Get movies user hasn't rated
    rated_movies = ratings[ratings['userId'] == user_id]['movieId'].values
    
    # Create recommendations
    movie_ids = user_movie_matrix.columns
    recommendations = []
    
    for i, movie_id in enumerate(movie_ids):
        if movie_id not in rated_movies:
            recommendations.append((movie_id, user_predictions[i]))
    
    # Sort and get top N
    recommendations.sort(key=lambda x: x[1], reverse=True)
    top_movie_ids = [rec[0] for rec in recommendations[:n]]
    
    return movies[movies['movieId'].isin(top_movie_ids)]['title'].tolist()