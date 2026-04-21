from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🔥 OFFLINE POSTER FUNCTION
def fetch_poster(movie_title):
    filename = movie_title.lower().replace(" ", "") + ".jpg"
    
    full_path = os.path.join("static", "posters", filename)

    if os.path.exists(full_path):
        return f"/static/posters/{filename}"   # 👈 VERY IMPORTANT CHANGE
    else:
        return f"/static/posters/default.jpg"


# 🎬 RECOMMEND FUNCTION
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(list(enumerate(distances)),
                        reverse=True, key=lambda x: x[1])[1:6]

    names = []
    posters = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        names.append(title)

        poster_path = fetch_poster(title)
        posters.append(poster_path)

    return names, posters


# 🌐 ROUTE
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        movie = request.form["movie"]
        names, posters = recommend(movie)
        return render_template("index.html", movies=names, posters=posters)

    return render_template("index.html", movies=None)


# ▶️ RUN APP
if __name__ == "__main__":
    app.run(debug=True)
