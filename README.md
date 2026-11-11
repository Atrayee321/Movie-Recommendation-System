# 🎬 CineMatch — Movie Recommendation System

A content-based movie recommender built with Python, natural language processing, scikit-learn and Streamlit using the **TMDB 5000 Movie Metadata** dataset.

## Features
- Search for movies by title
- Get 3–10 similar movie recommendations
- Recommendations from movie overviews, genres, keywords, cast and directors
- Cosine similarity over bag-of-words features
- Poster images when a TMDB API key is configured
- Dark-themed Streamlit dashboard

## Dataset
Download the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) from Kaggle. Both files are required:

```text
data/
  tmdb_5000_movies.csv
  tmdb_5000_credits.csv
```

**Note:** The dataset is not included in this repository. Download it from Kaggle and check its license/terms before redistribution.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud deployment
1. Add the two dataset CSVs to the `data/` directory and commit them to GitHub (subject to dataset licensing).
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Choose this repository and branch `main`, with entry point `app.py`.
4. Optionally add `TMDB_API_KEY = "your_key"` in the app's **Secrets** settings for posters.
5. Deploy.

Never commit a real API key to the repository.

## How it works
The app merges movies with credits on TMDB movie ID, parses JSON metadata, combines descriptive fields into weighted text tags, builds a 5,000-feature bag-of-words representation, and uses cosine similarity to rank related movies.

The recommendation engine is **content-based**, not collaborative filtering: it does not learn from user ratings or browsing history.

## Project layout
```text
Movie-Recommendation-System/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
└── data/
    └── README.md
```

## Credits
Inspired by [CampusX's movie recommender](https://github.com/campusx-official/movie-recommender-system-tmdb-dataset). Dataset sourced from Kaggle/TMDB. This product uses the TMDB API but is not endorsed or certified by TMDB.
