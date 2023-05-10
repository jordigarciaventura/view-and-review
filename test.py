import requests

endpoint="https://api.themoviedb.org/3"
image_endpoint="https://image.tmdb.org/t/p"
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MzFkODkyODc2OGIzZTgwNTI2ZGQ4ZjMxM2IyNTJlYyIsInN1YiI6IjY0M2QxMzU1NDFhZDhkMTFjMTJjOTk3YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.M9mmY6uYQnxzWEvasfuApAC8kTVEfGvmcS681NDWlSg"
headers = {"Authorization": f"Bearer {api_key}"}

payload={"query": "tita"}

res = requests.get(endpoint + "/search/movie", headers=headers, params=payload)
print(res.url)
results = res.json()["results"]
top_results = [k["title"] for k in results[:5]]
print(top_results)