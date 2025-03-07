import re
import socket
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, url_for
from urllib.parse import quote

app = Flask(__name__)


def clean_movie_title(title):
    """Remove numbers and trailing parentheses from movie titles."""
    return re.sub(r'^\d+\)?\s*', '', title).strip()


# Scrape the movie list from the website
response = requests.get(
    "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
)
soup = BeautifulSoup(response.text, "html.parser")
all_movies = soup.find_all(name="h3", class_="title")

# Extract and reverse the list
movies = [clean_movie_title(movie.get_text()) for movie in all_movies[::-1]]

# Save movies to a file
with open("movie.txt", mode="w", encoding="utf-8") as file:
    file.writelines(f"{movie}\n" for movie in movies)


@app.route('/')
def home():
    try:
        with open("movie.txt", mode="r", encoding="utf-8") as file:
            movies = [clean_movie_title(movie.strip()) for movie in file.readlines() if movie.strip()]
    except FileNotFoundError:
        movies = []

    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Top 100 Movies</title>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body>
        <div class="container">
            <h1>Top 100 Movies of All Time 🎬</h1>
            {% if movies %}
                <ul>
                    {% for movie in movies %}
                        <li>
                            <a href="https://www.google.com/search?q={{ movie | urlencode }}" target="_blank">
                                {{ movie }}
                            </a>
                        </li>
                    {% endfor %}
                </ul>
            {% else %}
                <p>No movies found. Please add some to <code>movie.txt</code>.</p>
            {% endif %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_template, movies=movies, urlencode=quote)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000

    # Check if port 5000 is in use
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', port)) == 0:
            print(f"Port {port} is in use. Trying port 5001...")
            port = 5001  # Use fallback port

    app.run(host=host, port=port, debug=True)
