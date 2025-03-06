import re
from flask import Flask, render_template_string, url_for
from urllib.parse import quote
import socket
app = Flask(__name__)

def clean_movie_title(title):
    """Remove numbers and trailing parentheses from movie titles."""
    return re.sub(r'^\d+\)?\s*', '', title).strip()

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

                    {% for movie in movies %}
                        <li>
                            <a href="https://www.google.com/search?q={{ movie | urlencode }}" target="_blank">
                                {{ movie }}
                            </a>
                        </li>
                    {% endfor %}

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
    app.run(host=host, port=port)

    # Check if port 5000 is in use
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', port)) == 0:
            print(f"Port {port} is in use. Trying port 5001...")
            port = 5001  # Use fallback port

    app.run(host=host, port=port, debug=True)
