const API_BASE = 'http://localhost:5000/api';

async function searchMovies() {
    const query = document.getElementById('searchInput').value;
    const response = await fetch(`${API_BASE}/movies/search?q=${query}`);
    const movies = await response.json();
    displayResults(movies);
}

async function displayResults(movies) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<p style="color: white;">Loading...</p>';
    
    resultsDiv.innerHTML = '';
    
    for (const movie of movies.slice(0, 6)) {
        const details = await fetch(`${API_BASE}/movie-details/${movie.movieId}`).then(r => r.json());
        
        const movieCard = document.createElement('div');
        movieCard.className = 'movie-card';
        movieCard.innerHTML = `
            ${details.poster ? `<img src="${details.poster}" alt="${movie.title}">` : ''}
            <h3>${movie.title}</h3>
            <p>${movie.genres}</p>
            ${details.trailer ? `<a href="${details.trailer}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>` : ''}
            <button onclick="getRecommendations('${movie.title.replace(/'/g, "\\'")}')">Get Similar Movies</button>
        `;
        resultsDiv.appendChild(movieCard);
    }
}

async function getRecommendations(movieTitle) {
    const response = await fetch(`${API_BASE}/recommend/content`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({movie_title: movieTitle, n: 10})
    });
    const data = await response.json();
    displayRecommendations(data.recommendations);
}

async function displayRecommendations(recommendations) {
    const recDiv = document.getElementById('recommendations');
    recDiv.innerHTML = '<p style="color: white;">Loading recommendations...</p>';
    
    recDiv.innerHTML = '';
    
    for (const title of recommendations.slice(0, 8)) {
        const card = document.createElement('div');
        card.className = 'movie-card';
        card.innerHTML = `
            <h3>${title}</h3>
            <button onclick="getRecommendations('${title.replace(/'/g, "\\'")}')">Get Similar Movies</button>
        `;
        recDiv.appendChild(card);
    }
}