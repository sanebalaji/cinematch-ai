"""
Recommendation Engine

This module implements a content-based movie
recommendation system using cosine similarity.
"""

import re
import pickle
from rapidfuzz import process
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from model.tmdb import fetch_complete_movie

BASE_DIR = Path(__file__).resolve().parent.parent

# Load processed movie data
movies = pickle.load(
    open(BASE_DIR / "artifacts" / "movies.pkl", "rb")
)

# Generate similarity matrix dynamically
cv = CountVectorizer(
    max_features=5000,
    stop_words="english"
)

vectors = cv.fit_transform(
    movies["tags"].fillna("")
)

similarity = cosine_similarity(vectors)


def normalize_title(title):
    """
    Normalize movie titles for fuzzy matching.

    Example:
    Iron Man    -> ironman
    Spider-Man  -> spiderman
    Spider Man  -> spiderman
    """

    return re.sub(r'[^a-z0-9]', '', str(title).lower())


def recommend(movie):

    titles = movies["title"].tolist()

    normalized_titles = [
        normalize_title(title)
        for title in titles
    ]

    normalized_movie = normalize_title(movie)

    match = process.extractOne(
        normalized_movie,
        normalized_titles,
        score_cutoff=80
    )

    if match is None:
        return None, []

    matched_index = match[2]

    matched_title = titles[matched_index]

    movie_index = movies[
        movies["title"] == matched_title
    ].index[0]

    distance = list(
        enumerate(similarity[movie_index])
    )

    distance = sorted(
        distance,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    TOP_K = 5

    for i in distance[1:TOP_K + 1]:

        movie_title = movies.iloc[i[0]].title

        movie_data = fetch_complete_movie(movie_title)

        if movie_data is not None:
            recommendations.append(movie_data)

    return matched_title, recommendations


