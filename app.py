import streamlit as st
import pickle
import requests
import pandas as pd

st.set_page_config(layout="wide", page_title="CineVerse", page_icon="🎬")

# 🎨 Custom CSS with Vector Icons and Refined Blue Theme
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');
        
        html, body, [class*="st-emotion-cache"] {
            font-family: 'Poppins', sans-serif;
            color: #d8d8d8;
        }

        .stApp {
            background: #0a0a0a;
            overflow-y: hidden; /* This line prevents vertical scrolling */
        }
        
        /* Specific rules to remove top space and align */
        .st-emotion-cache-z5fcl4 { 
            padding-top: 0rem; /* Ensures no padding at the very top of the main content area */
            
        }
        h1 { 
             font-size: 1em;
            margin-top: 0rem; /* Removes default top margin from the main title */
            padding-top: 0rem; /* Ensures no padding at the top of the main title */
        }
        /* Further adjustments for potential container spacing */
        .block-container {
            padding-top: 0rem;
            padding-left: 1rem; /* Adjust as needed */
            padding-right: 1rem; /* Adjust as needed */
            padding-bottom: 0rem;
        }
        


        h1, h2, h3, h4, h5, h6 {
            color: #f0f0f0;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0, 123, 255, 0.2);
        }
        
        h1::before {
            content: '\\f008'; /* Font Awesome film icon */
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            color: #4dc2ff;
            margin-right: 15px;
            font-size: 1em;
            vertical-align: middle;
        }

        .icon-movie::before { content: '\\f03d'; font-family: 'Font Awesome 6 Free'; font-weight: 900; color: #4dc2ff; margin-right: 8px; }
        .icon-overview::before { content: '\\f02d'; font-family: 'Font Awesome 6 Free'; font-weight: 900; color: #4dc2ff; margin-right: 8px; }
        .icon-crew::before { content: '\\f500'; font-family: 'Font Awesome 6 Free'; font-weight: 900; color: #4dc2ff; margin-right: 8px; }
        .icon-cast::before { content: '\\f0c0'; font-family: 'Font Awesome 6 Free'; font-weight: 900; color: #4dc2ff; margin-right: 8px; }
        .icon-trailer::before { content: '\\f144'; font-family: 'Font Awesome 6 Free'; font-weight: 900; color: #4dc2ff; margin-right: 8px; }
        .icon-search::before { content: '\\f002'; font-family: 'Font Awesome 6 Free'; font-weight: 900; color: #4dc2ff; position: absolute; left: 0.8rem; top: 50%; transform: translateY(-50%); z-index: 10; }
        .icon-trending::before { content: '\\f06d'; font-family: 'Font Awesome 6 Free'; font-weight: 900; color: #4dc2ff; margin-right: 8px; }
        .icon-info::before { content: '\\f05a'; font-family: 'Font Awesome 6 Free'; font-weight: 900; color: #4dc2ff; }

        /* General button styling */
        .stButton>button {
            background-color: rgba(0, 150, 255, 0.1);
            color: #4dc2ff;
            border: 1px solid rgba(0, 150, 255, 0.4);
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: 600;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 4px 15px rgba(0, 150, 255, 0.2);
            backdrop-filter: blur(5px);
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: rgba(0, 150, 255, 0.3);
            color: #ffffff;
            transform: scale(1.05);
            border: 1px solid rgba(0, 150, 255, 0.8);
            box-shadow: 0px 0px 20px rgba(0, 150, 255, 0.8), inset 0px 0px 10px rgba(0, 150, 255, 0.5);
        }
        
        /* New styling for the info box under the poster */
        .info-button-container {
            background-color: rgba(0, 150, 255, 0.1);
            border: 1px solid rgba(0, 150, 255, 0.4);
            border-radius: 10px;
            padding: 5px;
            margin-top: 10px;
            text-align: center;
            width: 100%;
        }

        .info-button-container .stButton > button {
            background-color: transparent;
            border: none;
            box-shadow: none;
            padding: 5px 10px;
            width: 100%;
            color: #4dc2ff;
            font-weight: 600;
            font-size: 14px;
        }

        .info-button-container .stButton > button:hover {
            background-color: rgba(0, 150, 255, 0.2);
            transform: scale(1.02);
            color: #ffffff;
            box-shadow: none;
        }

        /* Movie Card for Recommendations and Trending */
        .movie-card {
            position: relative;
            border-radius: 15px;
            overflow: hidden;
            transition: transform 0.4s ease-in-out, box-shadow 0.4s ease-in-out;
            cursor: pointer;
            border: 2px solid transparent;
            width: 100%;
            aspect-ratio: 2/3; 
        }
        .movie-card:hover {
            transform: translateY(-8px) scale(1.08);
            box-shadow: 0 15px 40px rgba(0, 150, 255, 0.6);
            border: 2px solid #0096ff;
        }
        .movie-card img {
            width: 100%;
            height: 100%; 
            object-fit: cover; 
            border-radius: 12px;
            display: block;
            transition: filter 0.3s ease;
        }
        .movie-card:hover img {
            filter: brightness(0.7);
        }
        .movie-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 22px 18px; 
            background: linear-gradient(to top, rgba(0,0,0,0.95), rgba(0,0,0,0));
            color: white;
            transition: opacity 0.4s ease;
            opacity: 1; 
        }
        .movie-title-overlay {
            font-weight: 700;
            font-size: 17px;
            text-shadow: 1px 1px 5px rgba(0,0,0,0.8);
        }
        .movie-rating-overlay {
            font-size: 12px; 
            color: #66b3ff;
            font-weight: 600;
            margin-top: 5px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        }

        .genre-badge {
            display: inline-block;
            background: rgba(0,150,255,0.25);
            color: #80d4ff;
            padding: 3px 8px; 
            margin: 3px 3px 0 0;
            border-radius: 8px;
            font-size: 10px; 
            font-weight: 500;
            border: 1px solid rgba(0,150,255,0.4);
        }
    </style>
""", unsafe_allow_html=True)


# --- GLOBAL VARIABLES & CACHING ---
try:
    movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files not found. Please ensure 'artifacts/movie_list.pkl' and 'artifacts/similarity.pkl' are in the correct directory.")
    st.stop()

API_KEY = "88f53bd0012ece4f356be2f1b12ea7ee" 

# --- Fetch functions (unchanged) ---
@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US&append_to_response=credits,videos"
        data = requests.get(url, timeout=10).json()
        if 'status_code' in data and data['status_code'] == 34:
            return None

        cast = data.get("credits", {}).get("cast", [])
        crew = data.get("credits", {}).get("crew", [])
        director = next((c for c in crew if c['job'] == 'Director'), None)
        writer = next((c for c in crew if c['job'] in ['Writer', 'Screenplay']), None)
        producer = next((c for c in crew if c['job'] == 'Producer'), None)

        trailer_key = None
        for vid in data.get("videos", {}).get("results", []):
            if vid['site'] == 'YouTube' and vid['type'] == 'Trailer':
                trailer_key = vid['key']
                break

        return {
            "title": data.get("title"),
            "poster": f"https://image.tmdb.org/t/p/w500/{data['poster_path']}" if data.get("poster_path") else None,
            "overview": data.get("overview", "No description available."),
            "release_date": data.get("release_date", "N/A"),
            "rating": data.get("vote_average", 0.0),
            "genres": [genre["name"] for genre in data.get("genres", [])],
            "cast": cast[:6],
            "director": director,
            "writer": writer,
            "producer": producer,
            "trailer_key": trailer_key
        }
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def fetch_trending_movies():
    try:
        url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
        data = requests.get(url, timeout=10).json()
        trending_list = []
        for movie in data.get("results", []):
            details = fetch_movie_details(movie.get('id'))
            genres = details['genres'] if details else []
            trending_list.append({
                "title": movie.get("title"),
                "poster": f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}" if movie.get("poster_path") else None,
                "rating": movie.get("vote_average", 0.0),
                "id": movie.get("id"),
                "genres": genres
            })
        return trending_list
    except Exception:
        return []

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:]
    except IndexError:
        st.error(f"Movie '{movie}' not found in the dataset.")
        return []
    
    recs = []
    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        details = fetch_movie_details(movie_id)
        if details and details["poster"]:
            recs.append(details)
        if len(recs) == 5:
            break
    return recs

# ---------------- UI ----------------
st.title("CineVerse Recommender")

if "selected_detail" not in st.session_state:
    st.session_state.selected_detail = None
    st.session_state.recommendations = []
    st.session_state.current_movie = None

# --- FULL DETAILS PAGE ---
if st.session_state.selected_detail:
    movie = st.session_state.selected_detail
    if st.button("⬅️ Back to Recommendations", key="back_button"):
        st.session_state.selected_detail = None
        st.rerun()
    st.markdown(f"<h3 class='icon-movie'>{movie['title']}</h3>", unsafe_allow_html=True)
    left_col, right_col = st.columns([1, 2])
    with left_col:
        st.image(movie["poster"], width=300)
        stars = "⭐" * int(round(movie["rating"] / 2))
        st.markdown(f"**{stars}** ({movie['rating']:.1f}/10)")
        st.write(f"📅 **Release Date:** {movie['release_date']}")
        st.write("🎭 " + ", ".join(movie["genres"]))
    with right_col:
        st.markdown("<h3 class='icon-overview'>Overview</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#ccc; font-size:15px; line-height:1.6;'>{movie['overview']}</p>", unsafe_allow_html=True)
        st.markdown("<h3 class='icon-crew'>Crew</h3>", unsafe_allow_html=True)
        crew_cols = st.columns(3)
        if movie["director"]: 
            with crew_cols[0]: st.caption(f"**Director:** {movie['director']['name']}")
        if movie["writer"]: 
            with crew_cols[1]: st.caption(f"**Writer:** {movie['writer']['name']}")
        if movie["producer"]: 
            with crew_cols[2]: st.caption(f"**Producer:** {movie['producer']['name']}")
        st.markdown("<h3 class='icon-cast'>Cast</h3>", unsafe_allow_html=True)
        cast_cols = st.columns(4)
        for idx, actor in enumerate(movie["cast"]):
            if idx < 4:
                with cast_cols[idx]:
                    if actor.get("profile_path"):
                        st.image(f"https://image.tmdb.org/t/p/w200{actor['profile_path']}", width=100)
                    st.caption(f"**{actor['name']}**")
                    st.caption(f"*{actor['character']}*")
    if movie["trailer_key"]:
        st.markdown("---")
        st.markdown("<h3 class='icon-trailer'>Trailer</h3>", unsafe_allow_html=True)
        st.video(f"https://www.youtube.com/watch?v={movie['trailer_key']}")

# --- MAIN RECOMMENDATIONS PAGE ---
else:
    tab1, tab2 = st.tabs(["Search & Recommend", "Trending Now"])
    with tab1:
        selected_movie = st.selectbox("", movies['title'].values, key="movie_selector")
        if selected_movie != st.session_state.current_movie:
            st.session_state.current_movie = selected_movie
            with st.spinner("Finding similar movies..."):
                st.session_state.recommendations = recommend(selected_movie)
                st.rerun()
        if st.session_state.recommendations:
            st.markdown("---")
            cols = st.columns(5)  # Changed from 4 to 5 columns
            for idx, movie in enumerate(st.session_state.recommendations):
                with cols[idx]:  # Use idx directly instead of idx % 4
                    genres_html = "".join([f"<span class='genre-badge'>{g}</span>" for g in movie.get('genres', [])[:2]])
                    st.markdown(f"""
                        <div class="movie-card">
                            <img src="{movie['poster']}" alt="{movie['title']} poster">
                            <div class="movie-overlay">
                                <div class="movie-title-overlay">{movie['title']}</div>
                                <div class="movie-rating-overlay">
                                    {"⭐" * int(round(movie['rating'] / 2))} ({movie['rating']:.1f}/10)
                                </div>
                                {genres_html if genres_html else ""}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("ℹ️", key=f"info_button_{idx}"):
                        st.session_state.selected_detail = movie
                        st.rerun()
    with tab2:
        st.markdown("<h2 class='icon-trending'>Trending Movies This Week</h2>", unsafe_allow_html=True)
        trending_movies = fetch_trending_movies()
        if trending_movies:
            # Create two rows of 5 columns each for the 10 trending movies
            for row in range(2):
                cols = st.columns(5)
                for col in range(5):
                    idx = row * 5 + col
                    if idx < len(trending_movies[:10]):
                        movie = trending_movies[idx]
                        with cols[col]:
                            genres_html = "".join([f"<span class='genre-badge'>{g}</span>" for g in movie.get('genres', [])[:2]])
                            st.markdown(f"""
                                <div class="movie-card">
                                    <img src="{movie['poster']}" alt="{movie['title']} poster">
                                    <div class="movie-overlay">
                                        <div class="movie-title-overlay">{movie['title']}</div>
                                        <div class="movie-rating-overlay">
                                            {"⭐" * int(round(movie['rating'] / 2))} ({movie['rating']:.1f}/10)
                                        </div>
                                        {genres_html if genres_html else ""}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("ℹ️", key=f"trending_info_button_{idx}"):
                                details = fetch_movie_details(movie['id'])
                                if details:
                                    st.session_state.selected_detail = details
                                    st.rerun()
