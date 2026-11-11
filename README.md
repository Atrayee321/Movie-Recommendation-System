# 🎬 CineMatch — Movie Recommendation System

<p align="center">
  <strong>Discover movies you'll love with content-based recommendations powered by natural language processing.</strong>
</p>

<p align="center">
  <a href="https://movie-recommendation-system-ycv3kiwgxp9tjjhxagbffk.streamlit.app/"><img alt="Live Demo" src="https://img.shields.io/badge/Live_Demo-Launch_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"></a>
  <a href="https://github.com/Atrayee321/Movie-Recommendation-System"><img alt="GitHub Repository" src="https://img.shields.io/badge/Source_Code-GitHub-181717?style=for-the-badge&logo=github"></a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?logo=streamlit&logoColor=white">
  <img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-NLP-F7931E?logo=scikitlearn&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-Not_Specified-lightgrey">
</p>

### 🚀 [Try the Live Application](https://movie-recommendation-system-ycv3kiwgxp9tjjhxagbffk.streamlit.app/)

---

## 📌 Overview

**CineMatch** is a content-based movie recommendation web application built with **Python**, **Streamlit**, **pandas**, and **scikit-learn**. Select a movie you enjoy, and the application recommends other movies with similar descriptions, genres, and keywords.

The recommendation engine analyzes movie metadata from the **TMDB 5000 Movie Metadata** dataset. Unlike collaborative filtering, this project does **not** require user ratings, viewing histories, or account creation.

## ✨ Features

- 🔎 **Movie search** — select a title from the available catalog.
- 🎯 **Personalized-by-selection suggestions** — discover movies similar to your chosen title.
- 🎛️ **Adjustable results** — choose between **3 and 10 recommendations**.
- 🧠 **NLP-based similarity** — bag-of-words text vectorization with cosine similarity.
- 🎭 **Metadata-aware matching** — uses overviews, genres, and keywords.
- 🖼️ **Movie posters** — retrieved from the TMDB API when a valid API key and poster are available.
- ⭐ **Movie details** — release year, average rating, genres, and expandable synopsis.
- 🌙 **Dark-themed interface** — responsive layout powered by Streamlit.
- ⚡ **Caching** — caches processed movie data, vectorized features, and poster lookups.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Application logic and data processing |
| **Streamlit** | Interactive web interface and deployment |
| **pandas** | Dataset loading, cleaning, and transformations |
| **scikit-learn** | CountVectorizer and cosine similarity |
| **Natural Language Processing** | Metadata tokenization and feature engineering |
| **TMDB API** | Optional movie poster retrieval |
| **Streamlit Community Cloud** | Web application hosting |

## 🧠 How the Recommendation Engine Works

```text
TMDB Movies CSV
       │
       ▼
Load and clean movie metadata
       │
       ▼
Extract overview + genres + keywords
       │
       ▼
Combine into weighted text tags
       │
       ▼
CountVectorizer (up to 5,000 features)
       │
       ▼
Compute cosine similarity for selected movie
       │
       ▼
Rank similar movies and exclude the selected title
       │
       ▼
Display top 3–10 recommendations
       │
       └──► Optional poster lookup via TMDB API
```

### Recommendation approach

1. **Preprocessing:** Read the movie CSV, remove duplicate IDs, and exclude records without a title or overview.
2. **Feature extraction:** Parse JSON-formatted genre and keyword fields and normalize multiword labels.
3. **Weighted tags:** Combine overview terms with repeated genre and keyword tokens to give metadata additional influence.
4. **Vectorization:** Convert text into a sparse bag-of-words representation using `CountVectorizer(max_features=5000, stop_words="english")`.
5. **Similarity:** Compute cosine similarity between the selected movie vector and the catalog.
6. **Ranking:** Exclude the selected movie and return the highest-scoring alternatives.

> **Model type:** Content-based recommendation, not collaborative filtering or a trained deep-learning model. The current version does not use actor or director metadata, and does not report formal recommendation-accuracy metrics.

## 📂 Project Structure

```text
Movie-Recommendation-System/
├── app.py                       # Streamlit UI and recommendation engine
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── .gitignore                   # Ignored local and secret files
├── .streamlit/
│   ├── config.toml              # App theme configuration
│   └── secrets.toml.example     # Example API-key configuration
└── data/
    ├── tmdb_5000_movies.csv     # Required TMDB movie dataset (add locally)
    └── README.md                # Dataset instructions
```

## 📊 Dataset

**Source:** [TMDB 5000 Movie Metadata — Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

The application requires **only** `tmdb_5000_movies.csv`. The larger `tmdb_5000_credits.csv` file is **not needed**.

The required CSV columns are `id`, `title`, `overview`, `genres`, `keywords`, `vote_average`, and `release_date`.

> Download the dataset from its source and review its usage terms before redistributing it.

## 💻 Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/Atrayee321/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

**2. Create and activate a virtual environment**

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Add the dataset**

Download `tmdb_5000_movies.csv` from Kaggle and place it in the `data/` folder.

**5. Start the app**

```bash
streamlit run app.py
```

Streamlit will show the local address in your terminal (typically `http://localhost:8501`).

## 🖼️ Enable Movie Posters (Optional)

The application can retrieve movie poster images from **The Movie Database (TMDB)**.

1. Create an account at [TMDB](https://www.themoviedb.org/).
2. Request an API key under [TMDB API Settings](https://www.themoviedb.org/settings/api).
3. For local use, create `.streamlit/secrets.toml`:

```toml
TMDB_API_KEY = "your_actual_tmdb_v3_api_key"
```

For Streamlit Community Cloud, add the same line under **App settings → Secrets** and save.

**Security:** Never commit `.streamlit/secrets.toml` or a real API key to GitHub. If an API key is missing, invalid, or the API is unavailable, the app may show **Poster unavailable**.

## ☁️ Deployment

The project is designed for **Streamlit Community Cloud**.

1. Push the project code and required dataset to a GitHub repository, subject to the dataset's redistribution terms.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Choose **Create app** and connect the repository.
4. Set the branch to `main` and the entry-point file to `app.py`.
5. Configure `TMDB_API_KEY` under **Secrets** if you want posters.
6. Deploy the app.

**🌐 Live website:** https://movie-recommendation-system-ycv3kiwgxp9tjjhxagbffk.streamlit.app/

## ⚠️ Limitations and Future Improvements

**Current limitations**
- Recommendations depend on descriptive metadata, not individual viewing preferences.
- Similarity scores reflect text overlap and do not guarantee movie quality or user satisfaction.
- Recommendations are restricted to the titles present in the dataset.
- Poster availability depends on TMDB API access and poster metadata.

**Potential improvements**
- Incorporate cast and director features when credits data is available.
- Add semantic embeddings for richer description-based similarity.
- Evaluate recommendation relevance using curated examples or user feedback.
- Add filters for genre, release year, and rating.
- Expand coverage beyond the TMDB 5000 catalog.

## 🙏 Acknowledgements

- [TMDB 5000 Movie Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) — movie metadata.
- [The Movie Database (TMDB)](https://www.themoviedb.org/) — movie information and optional poster API.
- [CampusX Movie Recommender](https://github.com/campusx-official/movie-recommender-system-tmdb-dataset) — project inspiration.
- [Streamlit](https://streamlit.io/) and [scikit-learn](https://scikit-learn.org/) — core technologies.

*This product uses the TMDB API but is not endorsed or certified by TMDB.*

---

<p align="center">
  <strong>Made with Python, NLP, and Streamlit.</strong><br>
  <a href="https://movie-recommendation-system-ycv3kiwgxp9tjjhxagbffk.streamlit.app/">Live Demo</a> ·
  <a href="https://github.com/Atrayee321/Movie-Recommendation-System">GitHub Repository</a>
</p>
