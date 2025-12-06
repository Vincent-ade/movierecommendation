# recommender.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self):
        self.movies = pd.read_csv('movies.csv')
        self.tfidf = TfidfVectorizer(stop_words='english')
        
        # Create feature matrix from genres
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies['genres'])
        
        # Calculate similarity between all movies
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
    
    def get_recommendations(self, movie_title, n=10):
        # Find movie index
        idx = self.movies[self.movies['title'] == movie_title].index[0]
        
        # Get similarity scores for this movie
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort by similarity
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N (excluding the movie itself)
        sim_scores = sim_scores[1:n+1]
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Return movie titles
        return self.movies['title'].iloc[movie_indices].tolist()

# Test it
recommender = ContentBasedRecommender()
recommendations = recommender.get_recommendations('Toy Story (1995)', n=5)
print(recommendations)