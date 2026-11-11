import json
import os
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="CineMatch | Movie Recommender", page_icon="🎬", layout="wide")
DATA = Path(__file__).parent / "data"

st.markdown("""<style>
.stApp {background: #0d111b; color: #f6f7fb}
h1,h2,h3 {color:#f8f9fc !important}
[data-testid="stMetric"] {background:#1b2435; padding:15px; border-radius:12px}
div.stButton > button {background:#e63946; color:white; border:0; border-radius:9px}
</style>""", unsafe_allow_html=True)

def parse_names(value, limit=None):
    try:
        items = json.loads(value) if isinstance(value, str) else value
        if not isinstance(items, list):
            return []
        names = [x.get("name", "") for x in items if isinstance(x, dict) and x.get("name")]
        return names[:limit] if limit else names
    except (ValueError, TypeError):
        return []

def director(value):
    try:
        items = json.loads(value) if isinstance(value, str) else value
        return [x["name"] for x in items if isinstance(x, dict) and x.get("job") == "Director"]
    except (ValueError, TypeError):
        return []

def normalize(words):
    return [str(w).replace(" ", "").lower() for w in words]

@st.cache_data(show_spinner="Preparing movie catalog…")
def load_movies():
    movies_path = DATA / "tmdb_5000_movies.csv"
    credits_path = DATA / "tmdb_5000_credits.csv"
    if not movies_path.exists() or not credits_path.exists():
        return None
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)
    required_m = {"id", "title", "overview", "genres", "keywords", "vote_average", "release_date"}
    required_c = {"movie_id", "cast", "crew"}
    if not required_m.issubset(movies.columns) or not required_c.issubset(credits.columns):
        raise ValueError("CSV files are missing required TMDB columns.")
    movies = movies.merge(credits[["movie_id", "cast", "crew"]], left_on="id", right_on="movie_id", how="inner")
    movies = movies.drop_duplicates("id").dropna(subset=["title", "overview"]).reset_index(drop=True)
    movies["genres_list"] = movies["genres"].apply(parse_names)
    movies["cast_list"] = movies["cast"].apply(lambda x: parse_names(x, 3))
    movies["director_list"] = movies["crew"].apply(director)
    movies["keywords_list"] = movies["keywords"].apply(parse_names)
    movies["tags"] = movies.apply(lambda r: " ".join(
        str(r["overview"]).lower().split() + normalize(r["genres_list"]) * 2 +
        normalize(r["keywords_list"]) + normalize(r["cast_list"]) * 2 +
        normalize(r["director_list"]) * 3), axis=1)
    return movies

@st.cache_resource(show_spinner="Building recommendation engine…")
def build_engine(tags):
    vectorizer = CountVectorizer(max_features=5000, stop_words="english")
    return vectorizer.fit_transform(tags)

@st.cache_data(ttl=86400, show_spinner=False)
def poster(movie_id):
    try:
        key = st.secrets.get("TMDB_API_KEY", "")
    except Exception:
        key = ""
    key = key or os.getenv("TMDB_API_KEY", "")
    if not key:
        return None
    try:
        r = requests.get(f"https://api.themoviedb.org/3/movie/{int(movie_id)}",
                         params={"api_key": key}, timeout=5)
        r.raise_for_status()
        path = r.json().get("poster_path")
        return "https://image.tmdb.org/t/p/w500" + path if path else None
    except (requests.RequestException, ValueError):
        return None

st.title("🎬 CineMatch")
st.caption("Discover your next favorite movie · Content-based recommendations powered by TMDB metadata")
try:
    movies = load_movies()
except Exception as exc:
    st.error(f"Unable to load movie data: {exc}")
    st.stop()
if movies is None:
    st.warning("Movie data is not installed yet.")
    st.markdown("Download the **TMDB 5000 Movie Dataset** from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata), and put BOTH `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` inside the `data/` folder. Commit those files to GitHub and redeploy.")
    st.stop()

vectors = build_engine(tuple(movies["tags"]))
st.markdown("### Find movies like the ones you love")
selected = st.selectbox("Choose a movie", movies["title"].sort_values().tolist(), index=None, placeholder="Search for a movie…")
count = st.slider("Number of recommendations", 3, 10, 5)
if selected and st.button("✨ Recommend movies", type="primary", use_container_width=True):
    idx = movies.index[movies["title"] == selected][0]
    scores = cosine_similarity(vectors[idx], vectors).ravel()
    ranked = [i for i in scores.argsort()[::-1] if i != idx][:count]
    st.subheader(f"Because you liked {selected}")
    for start in range(0, len(ranked), 5):
        cols = st.columns(5)
        for col, i in zip(cols, ranked[start:start + 5]):
            row = movies.iloc[i]
            with col:
                pic = poster(row["id"])
                if pic:
                    st.image(pic, use_container_width=True)
                else:
                    st.markdown("🎞️ **Poster unavailable**")
                st.markdown(f"**{row['title']}**")
                year = str(row["release_date"])[:4] if pd.notna(row["release_date"]) else "N/A"
                st.caption(f"{year} · ⭐ {row['vote_average']:.1f}/10")
                st.caption(", ".join(row["genres_list"][:2]))
                with st.expander("Overview"):
                    st.write(row["overview"])
st.divider()
a, b, c = st.columns(3)
a.metric("Movies indexed", f"{len(movies):,}")
b.metric("Recommendation method", "Cosine similarity")
c.metric("Text features", "5,000 max")
st.caption("Movie information: TMDB dataset. This product uses the TMDB API but is not endorsed or certified by TMDB. Poster imagery © respective owners.")
