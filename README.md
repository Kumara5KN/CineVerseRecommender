🎬 CINIVERSE – Movie Recommendation System
Your Gateway to Cinematic Excellence

CINIVERSE is an advanced AI-powered movie recommendation system built using Python, Streamlit, and TMDb API.
It provides smart personalized recommendations, trending movies, genre-based discovery, and detailed movie insights through a modern, beautifully designed UI.

🚀 Live Demo

🔗 https://cineverserecommender.streamlit.app

📌 Features
🎯 1. Smart Recommendations

AI-powered similarity matching

Uses metadata such as overview, cast, crew, genres, keywords, tagline

Displays Top 5 personalized recommendations

🔥 2. Trending Movies Section

Shows what’s hot right now

Displays:

Movie poster

Ratings

Genres

Explore Movie button

🎭 3. Genre-based Recommendations

Available categories include:

Action

Adventure

Romance

Horror

Mystery

Thriller

Comedy

Fantasy
… and more!

Each genre page includes:

High-quality poster

Movie rating

Genre badges

Explore Movie button

📘 4. Complete Movie Details Page

For every movie you select, you get:

HD poster

⭐ Rating

📅 Release date

⏳ Runtime

🏷 Genres

🎬 Director

✍️ Writer

🎥 Producer

👨‍🎤 Cast (with profile photos & character names)

🖼 5. Modern Cinematic UI

Dark theme

Neon blue highlights

Hover animations

Clean card layouts

Fully responsive interface

🧠 Tech Stack
Frontend

Streamlit

HTML/CSS (custom components)

Responsive layout system

Backend

Python

Movie similarity engine (cosine similarity)

Data processing using Pandas & NumPy

APIs

TMDb API for fetching:

Posters

Cast

Crew

Ratings

Trending data

Model

Content-based filtering

Vectorized metadata (genres, cast, crew, keywords)

📂 Project Structure
CINIVERSE/
│── data/
│   ├── movies.pkl
│   ├── similarity.pkl
│   └── tmdb_ids.csv
│
│── assets/
│   ├── backgrounds/
│   ├── icons/
│   └── styles.css
│
│── app.py                   # Main Streamlit application
│── utils.py                 # Helper functions
│── recommend.py             # Recommendation engine
│── requirements.txt
│── README.md

⚙️ How It Works
📝 Step 1 — Preprocessing

Movie dataset is cleaned and combined with:

Keywords

Genre labels

Cast names

Director/Writer

Overview text

🔍 Step 2 — Vectorization

TF-IDF or CountVectorizer converts metadata → feature vectors.

🧮 Step 3 — Similarity Calculation

Cosine similarity matrix is generated and saved as similarity.pkl.

🎯 Step 4 — Real-Time Recommendation

User selects a movie → top 5 most similar movies retrieved.

🎬 Step 5 — UI Rendering in Streamlit

All results displayed with posters, genres, buttons, and details.

🛠 Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/ciniverse.git
cd ciniverse

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Add TMDb API Key

Create a .env file and add:

TMDB_API_KEY=your_api_key_here

4️⃣ Run the app
streamlit run app.py

📸 Screenshots

(Use the screenshots you uploaded — add them to the repo)

🌐 Deployment

CINIVERSE is deployed on Streamlit Cloud.

To deploy:

Push code to GitHub

Go to → https://share.streamlit.io

Select your repo

Add API key in "Secrets" section

Deploy

🤝 Contributing

Pull requests are welcome.
For major feature updates, please open an issue first.

📜 License

MIT License © 2025 Kumara N

👤 Author

Kumara N
MCA – Presidency University
📧 kumaran.ds@example.com

🌐 GitHub: github.com/kumaran-data
🔗 LinkedIn: linkedin.com/in/kumaran
