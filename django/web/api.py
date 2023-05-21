from tmdbv3api import TMDb, Movie, Discover
from os import environ
import requests

# Crea una instancia de TMDb
tmdb = TMDb()
# Configura la API key de TMDb
movie = Movie()

tmdb.api_key = environ.get('API_KEY')

endpoint="https://api.themoviedb.org/3/"
image_endpoint="https://image.tmdb.org/t/p/"
api_key = environ.get('TMDB_BEARER_TOKEN', "")
headers = {"Authorization": f"Bearer {api_key}"}

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


def movie(movie_id):
    return requests.get(f"{endpoint}/movie/{movie_id}", headers=headers).json()


def search(query):
    params = {"query": query}
    return requests.get(f"{endpoint}/search/movie", headers=headers, params=params).json()


def popular():
    return requests.get(f"{endpoint}/movie/popular", headers=headers).json()


def top_rated():
    return requests.get(f"{endpoint}/movie/top_rated", headers=headers).json()


def upcoming():
    return requests.get(f"{endpoint}/movie/upcoming", headers=headers).json()


def now_playing():
    return requests.get(f"{endpoint}/movie/now_playing", headers=headers).json()


def get_image_url(path, type="poster", size="w92"):
    assert type in ["poster", "backdrop", "logo", "profile", "still"]
    
    if type == "poster":
        assert size in ["w92", "w154", "w185", "w342", "w500", "w780", "original"]
    elif type == "backdrop":
        assert size in ["w300", "w780", "w1280", "original"]
    elif type == "logo":
        assert size in ["w45", "w92", "w154", "w185", "w300", "w500", "original"]
    elif type == "profile":
        assert size in ["w45", "w185", "h632", "original"]
    elif type == "still":
        assert size in ["w92", "w185", "w300", "original"]
    
    return f"{image_endpoint}{size}{path}"


def get_genre_name(id):
    genre_names_by_id = { 
        "28": "Action",
        "12": "Adventure",
        "16": "Animation",
        "35": "Comedy",
        "80": "Crime",
        "99": "Documentary",
        "18": "Drama",
        "10751": "Family",
        "14": "Fantasy",
        "36": "History",
        "27": "Horror",
        "10402": "Music",
        "9648": "Mystery",
        "10749": "Romance",
        "878": "Sci-Fi",
        "10770": "TV Movie",
        "53": "Thriller",
        "10752": "War",
        "37": "Western"
    }
    assert str(id) in genre_names_by_id
    return genre_names_by_id[str(id)]

def get_genre_id(genre_slug):
    genre_ids_by_slug = {
        "action": 28,
        "adventure": 12,
        "animation": 16,
        "comedy": 35,
        "crime": 80,
        "documentary": 99,
        "drama": 18,
        "family": 10751,
        "fantasy": 14,
        "history": 36,
        "horror": 27,
        "music": 10402,
        "mystery": 9648,
        "romance": 10749,
        "sci-fi": 878,
        "tv-movie": 10770,
        "thriller": 53,
        "war": 10752,
        "western": 37
    }
    assert genre_slug in genre_ids_by_slug
    return genre_ids_by_slug[genre_slug]

def get_movie_trailer(movie_id):
    response = requests.get(f"{endpoint}/movie/{movie_id}/videos", headers=headers).json()
    for result in response["results"]:
        if result["type"] == "Trailer" and result["site"] == "YouTube":
            return result["key"]
        
        
def get_movie_credits(movie_id):
    result = requests.get(f"{endpoint}/movie/{movie_id}/credits", headers=headers).json()
    return result['cast'] + result['crew']

def get_directors(movie_cast):
    return [member for member in movie_cast if member.get("job","") == "Director"]

def get_writers(movie_cast):
    return [member for member in movie_cast if member.get("job", "") == "Writer"]
    
def get_actors(movie_cast):
    return [member for member in movie_cast if member.get("known_for_department", "") == "Acting"]

def get_similar(movie_id):
    return requests.get(f"{endpoint}/movie/{movie_id}/similar", headers=headers).json()

def get_movies_by_genre(genre):
    genre_id = get_genre_id(genre)
    return requests.get(f"{endpoint}/discover/movie", headers=headers, params={"with_genres": genre_id}).json()

def get_movies_by_year(year):
    return requests.get(f"{endpoint}/discover/movie", headers=headers, params={"primary_release_year": year}).json()