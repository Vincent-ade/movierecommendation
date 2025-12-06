# app.py
import sqlite3
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from recommender import ContentBasedRecommender
from collaborative_recommender import CollaborativeRecommender
from tmdb_service import search_movie_tmdb, get_movie_trailer, get_movie_poster

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Initialize recommenders
content_recommender = ContentBasedRecommender()
collab_recommender = CollaborativeRecommender()

# Load movies
movies = pd.read_csv('movies.csv')

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """Get all movies"""
    return jsonify(movies.to_dict('records'))

@app.route('/api/movies/search', methods=['GET'])
def search_movies():
    """Search movies by title"""
    query = request.args.get('q', '')
    results = movies[movies['title'].str.contains(query, case=False)]
    return jsonify(results.to_dict('records'))

@app.route('/api/recommend/content', methods=['POST'])
def recommend_content():
    """Get content-based recommendations"""
    data = request.json
    movie_title = data.get('movie_title')
    n = data.get('n', 10)
    
    recommendations = content_recommender.get_recommendations(movie_title, n)
    return jsonify({'recommendations': recommendations})

@app.route('/api/recommend/collaborative', methods=['POST'])
def recommend_collaborative():
    """Get collaborative filtering recommendations"""
    data = request.json
    user_id = data.get('user_id')
    n = data.get('n', 10)
    
    recommendations = collab_recommender.get_recommendations(user_id, n)
    return jsonify({'recommendations': recommendations})

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get single movie details"""
    movie = movies[movies['movieId'] == movie_id].to_dict('records')
    if movie:
        return jsonify(movie[0])
    return jsonify({'error': 'Movie not found'}), 404

# Add to app.py
@app.route('/api/rate', methods=['POST'])
def rate_movie():
    """User rates a movie"""
    data = request.json
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    rating = data.get('rating')
    
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO ratings (user_id, movie_id, rating, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (user_id, movie_id, rating, int(time.time())))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# Add this import
from tmdb_service import search_movie_tmdb, get_movie_trailer, get_movie_poster

# Add new endpoint
@app.route('/api/movie-details/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    """Get movie details with trailer"""
    movie = movies[movies['movieId'] == movie_id].iloc[0]
    
    # Search TMDb
    tmdb_data = search_movie_tmdb(movie['title'])
    
    if tmdb_data:
        tmdb_id = tmdb_data['id']
        trailer_url = get_movie_trailer(tmdb_id)
        poster_url = get_movie_poster(tmdb_id)
        
        return jsonify({
            'movieId': int(movie_id),
            'title': movie['title'],
            'genres': movie['genres'],
            'trailer': trailer_url,
            'poster': poster_url,
            'overview': tmdb_data.get('overview', '')
        })
    
    return jsonify({
        'movieId': int(movie_id),
        'title': movie['title'],
        'genres': movie['genres'],
        'trailer': None,
        'poster': None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
