# tmdb_service.py
import requests
import os

TMDB_API_KEY = 'b10886df3217561d7e0af42e880d43dc    '
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def get_movie_details(tmdb_id):
    """Get movie details from TMDb"""
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    params = {'api_key': TMDB_API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def get_movie_poster(tmdb_id):
    """Get movie poster URL"""
    details = get_movie_details(tmdb_id)
    poster_path = details.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

def search_movies_tmdb(query):
    """Search movies on TMDb"""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': query
    }
    response = requests.get(url, params=params)
    return response.json()['results']

def search_movie_tmdb(title):
    """Search for movie on TMDb"""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': title
    }
    response = requests.get(url, params=params)
    results = response.json().get('results', [])
    return results[0] if results else None

def get_movie_trailer(tmdb_id):
    """Get YouTube trailer URL"""
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}/videos"
    params = {'api_key': TMDB_API_KEY}
    response = requests.get(url, params=params)
    videos = response.json().get('results', [])
    
    # Find YouTube trailer
    for video in videos:
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return f"https://www.youtube.com/watch?v={video['key']}"
    
    return None

def get_movie_poster(tmdb_id):
    """Get poster image URL"""
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    params = {'api_key': TMDB_API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    poster_path = data.get('poster_path')
    
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None