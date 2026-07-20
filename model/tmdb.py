"""
TMDB Utility Functions

Handles communication with the TMDB API
for movie details, posters and cast.
"""


import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def search_movie(movie_name):
    url = f"{BASE_URL}/search/movie"
    response = requests.get(url, params={
        "api_key": API_KEY,
        "query": movie_name
    })
    return response.json()


def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    response = requests.get(url, params={
        "api_key": API_KEY
    })
    return response.json()


def get_poster_url(path):
    if path is None:
        return None
    return "https://image.tmdb.org/t/p/w500" + path


def get_movie_cast(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"

    response = requests.get(url, params={
        "api_key": API_KEY
    })

    data = response.json()

    cast = []

    for actor in data["cast"][:5]:
        cast.append({
            "name": actor["name"],
            "character": actor["character"],
            "photo": get_poster_url(actor["profile_path"])
        })

    return cast


def fetch_complete_movie(movie_name):
    

    search = search_movie(movie_name)

    if not search["results"]:
        return None

    movie_id = search["results"][0]["id"]

    details = get_movie_details(movie_id)

    return {
        "id": details["id"],
        "title": details["title"],
        "poster": get_poster_url(details["poster_path"]),
        "rating": details["vote_average"],
        "overview": details["overview"],
        "release_year": details["release_date"][:4],
        "language": details["original_language"],
        "runtime": details["runtime"],
        "genres": [g["name"] for g in details["genres"]],
        "cast": get_movie_cast(movie_id)
    }