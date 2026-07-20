"""
Flask Application

Entry point for the Movie Recommendation System.
"""
from flask import Flask, render_template, request
from model.recommender import recommend
from model.tmdb import fetch_complete_movie

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    selected_movie = None
    recommendations = []
    error = None
    movie_name = request.args.get("movie")


    if movie_name:

        matched_title, recommendations = recommend(movie_name)

        if matched_title is None:

            error = "Movie not found. Please try another movie."

        else:

            selected_movie = fetch_complete_movie(matched_title)


    return render_template(

    "index.html",

    recommendations=recommendations,

    selected_movie=selected_movie,

    error=error

    )

if __name__ == "__main__":
    app.run(debug=True)