import streamlit as st
import pickle
import requests
import pandas as pd
import random 
import time # Import time for placeholder loading

st.set_page_config(layout="wide", page_title="CineVerse", page_icon="🎬")

# --- CSS STYLES (Mobile Responsiveness Fix Added) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');
        
        * {
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            background-attachment: fixed;
        }
        
        /* General Streamlit/Container Resets */
        .st-emotion-cache-z5fcl4, .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Premium Header styling */
        .main-header {
            background: linear-gradient(90deg, #0096ff 0%, #00d4ff 50%, #6e8efb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            font-size: 4rem !important;
            font-weight: 800 !important;
            margin: 0.5rem 0 0.2rem 0 !important;
            padding: 0 !important;
            line-height: 1.1 !important;
            text-shadow: 0 0 30px rgba(0, 150, 255, 0.3);
            letter-spacing: -0.5px;
        }

        .subtitle {
            text-align: center;
            color: #88c8ff;
            font-size: 1.2rem;
            margin: 0 0 2rem 0 !important;
            padding: 0 !important;
            font-weight: 300;
            line-height: 1.4;
            opacity: 0.9;
        }

        /* Enhanced Premium Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 25px;
            padding: 8px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 2rem !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            color: #88c8ff !important;
            border-radius: 20px !important;
            padding: 12px 28px !important;
            font-weight: 500 !important;
            font-size: 1.1rem !important;
            border: none !important;
            transition: all 0.3s ease !important;
            position: relative;
            overflow: hidden;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #0096ff 0%, #00d4ff 100%) !important;
            color: white !important;
            box-shadow: 0 8px 25px rgba(0, 150, 255, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            transform: translateY(-2px);
            font-weight: 600 !important;
        }

        .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
            background: rgba(255, 255, 255, 0.08) !important;
            color: #ffffff !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 15px rgba(0, 150, 255, 0.2);
        }

        /* Enhanced Search Box */
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 2px solid rgba(0, 150, 255, 0.4) !important;
            border-radius: 20px !important;
            padding: 15px 25px !important;
            color: white !important;
            font-size: 1.1rem !important;
            backdrop-filter: blur(20px);
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 150, 255, 0.1);
        }

        .stSelectbox > div > div:hover {
            border-color: #0096ff !important;
            box-shadow: 0 8px 25px rgba(0, 150, 255, 0.3) !important;
            transform: translateY(-2px);
        }

        /* Enhanced Movie Card Design - ALWAYS SHOW DETAILS */
        .movie-card-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            margin-bottom: 2rem;
            width: 100%;
            gap: 1rem;
        }

        .movie-card {
            position: relative;
            border-radius: 25px;
            overflow: hidden;
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
            border: 2px solid transparent;
            background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            backdrop-filter: blur(20px);
            width: 100%;
            aspect-ratio: 2/3;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .movie-card:hover {
            transform: translateY(-15px) scale(1.05);
            box-shadow: 0 25px 50px rgba(0, 150, 255, 0.4);
            border: 2px solid #0096ff;
        }

        .movie-poster {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: all 0.5s ease;
            display: block;
        }

        /* ALWAYS VISIBLE OVERLAY */
        .movie-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0, 0, 0, 0.95));
            padding: 1.5rem 1rem 1rem;
            transform: translateY(0); 
            transition: transform 0.3s ease;
        }

        .movie-title-overlay {
            color: white;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.5rem;
            line-height: 1.3;
        }

        .movie-rating-overlay {
            color: #ffd700;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }

        /* Enhanced Genre Badges */
        .genre-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            justify-content: center;
            max-width: 100%;
            overflow: hidden;
        }

        .genre-badge {
            display: inline-block;
            background: rgba(0, 150, 255, 0.3);
            color: #88c8ff;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.7rem;
            border: 1px solid rgba(0, 150, 255, 0.5);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 80px;
        }

        /* --- MOBILE SCREEN CSS FIX (Max-width 600px) --- */
        @media (max-width: 600px) {
            /* Reduce space on overlay for small cards */
            .movie-overlay {
                padding: 0.75rem 0.5rem 0.5rem; 
            }

            /* Make title font smaller to fit narrow card */
            .movie-title-overlay {
                font-size: 0.8rem; 
                margin-bottom: 0.2rem;
                /* Ensure single line title works best */
                white-space: nowrap; 
                overflow: hidden;
                text-overflow: ellipsis;
            }

            /* Make rating font smaller */
            .movie-rating-overlay {
                font-size: 0.7rem; 
                margin-bottom: 0.3rem;
            }
            
            /* Make genre badges smaller */
            .genre-badge {
                padding: 0.1rem 0.4rem;
                font-size: 0.6rem;
                max-width: 50px; 
            }
            
            /* Adjust padding on other elements */
            .main-header {
                font-size: 2.5rem !important;
            }
            
            .subtitle {
                font-size: 1rem;
            }
        }
        /* --- END MOBILE SCREEN CSS FIX --- */

        /* Enhanced Button Styles (Rest of CSS omitted for brevity but remains the same) */
        .stButton > button {
            background: linear-gradient(135deg, #0096ff 0%, #00d4ff 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 5px 15px rgba(0, 150, 255, 0.3) !important;
            position: relative !important;
            overflow: hidden !important;
        }

        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(0, 150, 255, 0.5) !important;
        }

        .stButton > button:active {
            transform: translateY(-1px) !important;
        }

        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }

        .stButton > button:hover::before {
            left: 100%;
        }

        /* Back Button Special Style */
        .stButton > button[key="back_button"] {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%) !important;
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3) !important;
        }

        .stButton > button[key="back_button"]:hover {
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.5) !important;
        }

        /* Simple Text-Only Movie Details */
        .movie-details-simple {
            margin-bottom: 2rem;
        }

        .movie-details-header {
            color: #88c8ff;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            padding-left: 10px;
            border-left: 5px solid #0096ff;
        }

        .movie-detail-line {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            color: #ffffff;
            font-size: 1.1rem;
        }

        .detail-icon {
            font-size: 1.3rem;
            margin-right: 1rem;
            width: 30px;
            text-align: center;
        }

        .detail-text {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
        }

        .rating-stars {
            color: #ffd700;
            font-size: 1.4rem;
            margin-right: 0.5rem;
        }

        .rating-value {
            color: #88c8ff;
            font-weight: 500;
            margin-left: 0.5rem;
        }

        /* Cast & Crew Styles */
        .simple-cast-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }

        .simple-cast-card:hover {
            transform: translateY(-5px);
            border-color: #0096ff;
            box-shadow: 0 10px 20px rgba(0, 150, 255, 0.2);
        }
        
        .cast-image {
            border-radius: 10px;
            margin-bottom: 0.8rem;
            width: 80px;
            height: 80px;
            object-fit: cover;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        .simple-crew-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }

        .simple-crew-card:hover {
            transform: translateY(-3px);
            border-color: #0096ff;
        }

        /* Section Headers */
        .section-header {
            background: linear-gradient(90deg, #0096ff, #6e8efb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            margin: 1.5rem 0 2rem 0 !important;
            padding: 0 !important;
            text-align: center;
            line-height: 1.2;
            text-shadow: 0 0 20px rgba(0, 150, 255, 0.3);
        }
        
        .subsection-header {
            color: #88c8ff;
            font-size: 1.8rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            padding-left: 10px;
            border-left: 5px solid #0096ff;
        }
        
        /* Simple Genre Title Style - Like Currently Trending */
        .genre-title-simple {
            color: #88c8ff;
            font-size: 1.8rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            padding-left: 10px;
            border-left: 5px solid #0096ff;
        }
        
        .info-message {
            color: #88c8ff;
            font-size: 1rem;
            margin-bottom: 1rem;
            padding-left: 10px;
        }
        
        .footer {
            text-align: center;
            color: #88c8ff;
            padding: 3rem 0 1.5rem 0;
            margin-top: 3rem;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            font-size: 0.9rem;
            opacity: 0.8;
        }

        /* Enhanced Loading Animation */
        .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 150px;
            padding: 2rem 0;
        }

        .loading-dots {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1rem;
        }

        .loading-dots div {
            width: 12px;
            height: 12px;
            background-color: #0096ff;
            border-radius: 50%;
            margin: 0 5px;
            animation: bounce 1.2s infinite ease-in-out;
        }

        .loading-dots div:nth-child(1) { animation-delay: -0.32s; }
        .loading-dots div:nth-child(2) { animation-delay: -0.16s; }
        .loading-dots div:nth-child(3) { animation-delay: 0s; }
        .loading-dots div:nth-child(4) { animation-delay: 0.16s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }

        /* Genre Section Enhancements */
        .genre-section {
            margin-bottom: 3rem;
        }

        /* Remove horizontal scroll from all containers */
        .row-widget.stColumns {
            overflow: visible !important;
        }
        
        .element-container {
            overflow: visible !important;
        }
        
        /* Ensure no horizontal scrolling in movie cards */
        .movie-card-container {
            overflow: visible !important;
        }

        /* Full Width Overview Section */
        .overview-full-width {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            margin: 2rem 0;
        }

        .overview-header {
            color: #88c8ff;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            padding-left: 10px;
            border-left: 5px solid #0096ff;
        }

        .overview-content {
            color: #e0e0e0;
            line-height: 1.8;
            font-size: 1.1rem;
            text-align: justify;
        }
    </style>
""", unsafe_allow_html=True)

# --- GLOBAL VARIABLES & CACHING ---
@st.cache_data(show_spinner="Loading Model Data...")
def load_data():
    """Loads and caches the large model files only once."""
    try:
        movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
        similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
        return movies, similarity
    except FileNotFoundError:
        st.error("Model files not found. Please ensure 'artifacts/movie_list.pkl' and 'artifacts/similarity.pkl' are in the correct directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading model files: {e}")
        st.stop()

movies, similarity = load_data()

try:
    API_KEY = st.secrets["TMDB_API_KEY"]
except KeyError:
    st.warning("TMDB_API_KEY not found in st.secrets. API calls may fail.")
    API_KEY = "dummy_api_key_for_no_secret" 

# --- TMDB Genre Mapping ---
GENRES_TO_DISPLAY = {
    "Action": 28,
    "Adventure": 12,
    "Romance": 10749,
    "Horror": 27,
    "Sci-Fi": 878,
    "Drama": 18,
    "Mystery": 9648
}

# --- Fetch functions ---
@st.cache_data(show_spinner=False, ttl=3600) # Cache API data for 1 hour
def fetch_movie_details(movie_id):
    """Fetches full movie details including credits and trailer."""
    if isinstance(movie_id, (pd.Series, pd.DataFrame)):
        try:
            movie_id = movie_id.iloc[0]['movie_id']
        except:
            return None
    
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
            "trailer_key": trailer_key,
            "runtime": data.get("runtime"),
            "budget": data.get("budget"),
            "revenue": data.get("revenue"),
            "id": movie_id
        }
    except Exception:
        return None

@st.cache_data(show_spinner="Calculating Recommendations...")
def recommend(movie_title, movies_df, similarity_matrix):
    try:
        index = movies_df[movies_df['title'] == movie_title].index[0]
        distances = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])[1:]
    except IndexError:
        return []
    
    recs = []
    for i in distances:
        movie_id = movies_df.iloc[i[0]].movie_id
        details = fetch_movie_details(movie_id) 
        if details and details["poster"]:
            recs.append(details)
        if len(recs) == 5:
            break
    return recs

@st.cache_data(show_spinner="Fetching Top Trending...", ttl=3600)
def fetch_top_trending_movies(limit=5):
    """Fetches and processes full details for the top N overall trending movies."""
    try:
        url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
        data = requests.get(url, timeout=10).json()
        
        trending_list = []
        for movie_summary in data.get("results", [])[:limit*2]:
            movie_id = movie_summary.get('id')
            if movie_id:
                details = fetch_movie_details(movie_id) 
                if details and details["poster"]:
                    trending_list.append(details)
            if len(trending_list) >= limit:
                break
        return trending_list
    except Exception:
        return []

@st.cache_data(show_spinner="Fetching Genre Data...", ttl=3600)
def get_popular_by_genre_data(genre_name, genre_id, limit=5, movies_df=movies):
    """Fetches movies by genre using a robust 3-step fallback, now cached."""
    
    def fetch_movies_from_url(url, limit):
        movies_found = []
        try:
            data = requests.get(url, timeout=10).json()
            for movie_summary in data.get("results", [])[:limit*2]:
                movie_id = movie_summary.get('id')
                if movie_id:
                    details = fetch_movie_details(movie_id) 
                    if details and details["poster"]:
                        movies_found.append(details)
                if len(movies_found) >= limit:
                    break
        except Exception:
            pass
        return movies_found

    # --- Attempt 1: Current Trending/Popular ---
    trending_url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=en-US&sort_by=popularity.desc&with_genres={genre_id}&page=1&vote_count.gte=50"
    movie_list = fetch_movies_from_url(trending_url, limit)
    if len(movie_list) == limit: 
        return movie_list, "trending"

    # --- Attempt 2: All-Time Popular/Highest Voted (Fallback 1) ---
    all_time_url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=en-US&sort_by=vote_count.desc&with_genres={genre_id}&page=1&vote_average.gte=7.0&vote_count.gte=1000"
    movie_list = fetch_movies_from_url(all_time_url, limit)
    if len(movie_list) == limit:
        return movie_list, "all-time"

    # --- Attempt 3: Local Dataset Fallback (Fallback 2) ---
    if not movie_list:
        try:
            genre_tag = genre_name.lower().replace(" ", "")
            if genre_tag == "sci-fi": 
                genre_tag = "sciencefiction" 
            
            potential_fallbacks = movies_df[movies_df['tags'].str.contains(genre_tag, case=False, na=False)]
            
            if not potential_fallbacks.empty:
                local_movies_for_genre = []
                if len(potential_fallbacks) >= limit:
                    sampled_rows = potential_fallbacks.sample(n=limit, random_state=random.randint(0, 1000))
                    for index, row in sampled_rows.iterrows():
                        details = fetch_movie_details(row.movie_id)
                        if details and details["poster"]:
                            local_movies_for_genre.append(details)
                else:
                    for index, row in potential_fallbacks.iterrows():
                        details = fetch_movie_details(row.movie_id)
                        if details and details["poster"]:
                            local_movies_for_genre.append(details)
                    while len(local_movies_for_genre) < limit and local_movies_for_genre:
                        local_movies_for_genre.extend(local_movies_for_genre)
                    local_movies_for_genre = local_movies_for_genre[:limit]

                if len(local_movies_for_genre) == limit:
                    return local_movies_for_genre, "local_fallback"
        except Exception:
            pass 

    return [], "none"

# --- Helper function to display movie cards (no change needed here) ---
def display_movie_row(movie_list, key_prefix):
    # Streamlit automatically handles 5 columns becoming stacked vertically on mobile,
    # but the content inside still benefits from the CSS media query for sizing.
    num_cols = min(len(movie_list), 5)
    cols = st.columns(5, gap="medium")
    
    for idx, movie in enumerate(movie_list):
        if idx < num_cols:
            with cols[idx]:
                genres_html = "".join([f"<span class='genre-badge'>{g}</span>" for g in movie.get('genres', [])[:2]])
                st.markdown(f"""
                    <div class="movie-card-container">
                        <div class="movie-card">
                            <img class="movie-poster" src="{movie['poster']}" alt="{movie['title']} poster">
                            <div class="movie-overlay">
                                <div class="movie-title-overlay">{movie['title']}</div>
                                <div class="movie-rating-overlay">
                                    {"⭐" * int(round(movie['rating'] / 2))} ({movie['rating']:.1f}/10)
                                </div>
                                <div class="genre-badges">{genres_html}</div>
                            </div>
                        </div>
                        <div style="width: 100%;">
                """, unsafe_allow_html=True)
                
                if st.button("Explore Movie 🎬", key=f"{key_prefix}_info_button_{movie['id']}-{idx}", use_container_width=True):
                    st.session_state.selected_detail = movie
                    st.rerun()
                
                st.markdown("</div></div>", unsafe_allow_html=True)

# --- Custom Loading Animation (no change needed here) ---
def show_loading_animation():
    st.markdown("""
        <div class="loading-container">
            <div class="loading-dots">
                <div></div><div></div><div></div><div></div>
            </div>
            <p style="color: #88c8ff; font-size: 1.1rem; font-weight: 500; text-align: center;">Discovering cinematic masterpieces...</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------- PROFESSIONAL PREMIUM UI ----------------
st.markdown('<h1 class="main-header">CINIVERSE</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Gateway to Cinematic Excellence</p>', unsafe_allow_html=True)

if "selected_detail" not in st.session_state:
    st.session_state.selected_detail = None
    st.session_state.recommendations = []
    st.session_state.current_movie = None
    st.session_state.selected_movie_info = None

# --- PROFESSIONAL MOVIE DETAILS PAGE (View for a single movie) ---
if st.session_state.selected_detail:
    movie = st.session_state.selected_detail
    
    if st.button("⬅️ Back to Recommendations", key="back_button", use_container_width=True):
        st.session_state.selected_detail = None
        st.rerun()
    
    st.markdown(f'<h2 class="section-header">{movie["title"]}</h2>', unsafe_allow_html=True)
    
    # First Row: Poster and Movie Details
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.image(movie["poster"], use_container_width=True)
    
    with col2:
        # Simple Text-Only Movie Details
        st.markdown('<div class="movie-details-simple">', unsafe_allow_html=True)
        st.markdown('<div class="movie-details-header">🎬 Movie Details</div>', unsafe_allow_html=True)
        
        # Rating with stars
        stars = "⭐" * int(round(movie["rating"] / 2))
        st.markdown(f"""
            <div class="movie-detail-line">
                <div class="detail-icon">⭐</div>
                <div class="detail-text">
                    <span class="rating-stars">{stars}</span>
                    <span class="rating-value">({movie["rating"]:.1f}/10)</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Release Date
        st.markdown(f"""
            <div class="movie-detail-line">
                <div class="detail-icon">📅</div>
                <div class="detail-text">
                    <span>Release Date</span>
                    <span style="margin-left: 10px; color: #88c8ff;">{movie['release_date']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Runtime (if available)
        if movie.get('runtime'):
            st.markdown(f"""
                <div class="movie-detail-line">
                    <div class="detail-icon">⏱️</div>
                    <div class="detail-text">
                        <span>Runtime</span>
                        <span style="margin-left: 10px; color: #88c8ff;">{movie['runtime']} minutes</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Genres (if available)
        if movie.get('genres'):
            st.markdown(f"""
                <div class="movie-detail-line">
                    <div class="detail-icon">🎭</div>
                    <div class="detail-text">
                        <span>Genres</span>
                        <span style="margin-left: 10px; color: #88c8ff;">{', '.join(movie['genres'])}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) 
        
        # Production Team
        st.markdown("### 👥 Production Team")
        crew_cols = st.columns(3)
        crew_info = [
            ("Director", movie.get("director")),
            ("Writer", movie.get("writer")),
            ("Producer", movie.get("producer"))
        ]
        
        for idx, (role, person) in enumerate(crew_info):
            with crew_cols[idx]:
                if person:
                    st.markdown(f"""
                    <div class="simple-crew-card">
                        <strong>{role}</strong><br>
                        {person['name']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Cast Section
        st.markdown("### 🌟 Featured Cast")
        cast_cols = st.columns(4)
        for idx, actor in enumerate(movie["cast"]):
            if idx < 4:
                with cast_cols[idx]:
                    profile_path = actor.get("profile_path")
                    
                    if profile_path:
                        image_html = f'<img class="cast-image" src="https://image.tmdb.org/t/p/w200{profile_path}" alt="{actor["name"]} profile">'
                    else:
                        image_html = '<div class="cast-image" style="background: rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: center; font-size: 30px; color: #fff;">👤</div>'

                    st.markdown(f"""
                    <div class="simple-cast-card">
                        {image_html}
                        <strong>{actor['name']}</strong><br>
                        <small><em>{actor['character']}</em></small>
                    </div>
                    """, unsafe_allow_html=True)

    # Full Width Overview Section
    st.markdown('<div class="overview-full-width">', unsafe_allow_html=True)
    st.markdown('<div class="overview-header">📖 Synopsis</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="overview-content">{movie["overview"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Trailer Section
    if movie["trailer_key"]:
        st.markdown("### 🎥 Official Trailer")
        st.video(f"https://www.youtube.com/watch?v={movie['trailer_key']}")


# --- PROFESSIONAL MAIN RECOMMENDATIONS PAGE ---
else:
    tab1, tab2 = st.tabs(["🎯 Smart Recommendations", "🔥 Trending Now"])
    
    with tab1:
        selected_movie = st.selectbox(
            "Search from our extensive movie collection...", 
            movies['title'].values, 
            key="movie_selector",
            index=0
        )
        
        if selected_movie and (selected_movie != st.session_state.current_movie or not st.session_state.recommendations):
            st.session_state.current_movie = selected_movie
            
            with st.empty():
                show_loading_animation()
                
                try:
                    movie_id_row = movies[movies['title'] == selected_movie].iloc[0]
                    selected_movie_id = movie_id_row['movie_id']
                    
                    # Fetching main movie details (cached)
                    st.session_state.selected_movie_info = fetch_movie_details(selected_movie_id)
                    
                    # Fetching recommendations (cached)
                    st.session_state.recommendations = recommend(selected_movie, movies, similarity)
                    
                except Exception as e:
                    st.error(f"Error processing selection: {e}")
                    st.session_state.recommendations = []
                    st.session_state.selected_movie_info = None
                    
                st.rerun() 

        # 2. Display the selected movie's information first
        if st.session_state.get('selected_movie_info'):
            main_movie = st.session_state.selected_movie_info
            
            st.markdown(f'<h3 class="subsection-header">Your Selection: {main_movie["title"]}</h3>', unsafe_allow_html=True)
            
            # This section now uses dynamic sizing for the poster
            col_poster, col_overview = st.columns([1, 4], gap="large")
            
            with col_poster:
                if main_movie.get("poster"):
                    # FIX: Use use_container_width=True for responsiveness
                    st.image(main_movie["poster"], use_container_width=True) 
                else:
                    st.warning("Poster not found.")
                
            with col_overview:
                st.markdown('<div class="movie-details-header" style="margin-top:0;">Details</div>', unsafe_allow_html=True)
                st.markdown(f"""
                    <div style="color: #e0e0e0; font-size: 1.1rem; line-height: 1.6;">
                        <strong>Rating:</strong> {"⭐" * int(round(main_movie["rating"] / 2))} ({main_movie["rating"]:.1f}/10)<br>
                        <strong>Release:</strong> {main_movie["release_date"]}<br>
                        <strong>Genres:</strong> {', '.join(main_movie["genres"])}
                    </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="overview-header" style="margin-top:1.5rem; margin-bottom:1rem;">Synopsis</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="overview-content" style="font-size:1rem; line-height:1.6; color: #ccc; margin-bottom: 1.5rem;">{main_movie["overview"]}</div>', unsafe_allow_html=True)
                
                if st.button("See Full Details 🔍", key="main_explore_button", use_container_width=False):
                     st.session_state.selected_detail = main_movie
                     st.rerun()
            
            st.markdown("---")

            # 3. Display Recommendations
            st.markdown(f'<h3 class="subsection-header">Top 5 Recommendations for You</h3>', unsafe_allow_html=True)
            
        if st.session_state.recommendations:
            display_movie_row(st.session_state.recommendations, "recommend")
    
    with tab2:
        st.markdown('<h3 class="section-header">🔥 Trending Now</h3>', unsafe_allow_html=True)
        
        # --- 1. CURRENTLY TRENDING (Overall Top 5) ---
        st.markdown('<p class="subsection-header">🌟 Currently Trending</p>', unsafe_allow_html=True)
        
        top_trending = fetch_top_trending_movies(limit=5)
        
        if top_trending:
            display_movie_row(top_trending, "top_overall")
        else:
            st.info("Could not fetch overall trending movies at this time.")

        st.markdown("---")
        
        # --- 2. GENRE BREAKDOWN (Strict 5 Movies per Genre) ---
        st.markdown('<p class="subsection-header">🎬 Trending by Genre</p>', unsafe_allow_html=True)

        genre_data = {}
        for genre_name, genre_id in GENRES_TO_DISPLAY.items():
            genre_movies, source = get_popular_by_genre_data(genre_name, genre_id, limit=5)
            genre_data[genre_name] = (genre_movies, source)

        displayed_genres = 0
        for genre_name, (genre_movies, source) in genre_data.items():
            if len(genre_movies) == 5:
                displayed_genres += 1
                with st.container():
                    st.markdown(f'<div class="genre-title-simple">{genre_name}</div>', unsafe_allow_html=True)
                    
                    display_movie_row(genre_movies, f"genre_{genre_name}")
                    
                    if displayed_genres < len([g for g in genre_data.values() if len(g[0]) == 5]):
                        st.markdown("<br>", unsafe_allow_html=True)
