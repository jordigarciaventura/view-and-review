from tmdbv3api import TMDb, Movie, Discover
from os import environ

# Crea una instancia de TMDb
tmdb = TMDb()
# Configura la API key de TMDb
movie = Movie()

tmdb.api_key = environ.get('API_KEY')

def latest(number=20):
    discover = Discover()
    movies = discover.discover_movies({
    'sort_by': 'popularity.desc'
    })[:number]
    return movies

def popular(number=20):
    return movie.popular(number)

def top_most_rated(number=20):
    return movie.top_rated()[:number]

def top_most_rated_includes(number=20, min_votes=300, max_pages=1000, includes="Batman"):
    movies = []    
    # Realiza la búsqueda en todas las páginas
    for i in range(1, max_pages):  # número máximo de páginas
        search_result = movie.search(includes, page=i)
        
        if not search_result:
            break
        
        for result in search_result: 
            if result.vote_count >= min_votes:
                movies.append(result)
        
    return sorted(movies, key=lambda x: x.vote_average, reverse=True)[:number]
        