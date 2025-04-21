import pickle
import streamlit as st
import requests
import joblib

# Set page config
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.markdown("""
    <style>
        /* Remove top padding and adjust spacing */
        .block-container {
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)


# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = joblib.load(open('similarity.pkl', 'rb'))

# Fetch poster from API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Image"
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

# Recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:7]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Header
st.markdown("<h1 style='text-align: center; color: #ffffff;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox("🔍 Search or select a movie:", movie_list)

# Button to trigger recommendations
if st.button('📽️ Show Recommendations'):
    names, posters = recommend(selected_movie)
    st.markdown("Top 5 Recommendations:")
    cols = st.columns(6)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster, use_container_width=True)

            st.markdown(f"<p style='color:#ffffff; font-weight:bold; font-size:15px; text-align:center'>{name}</p>",unsafe_allow_html=True)
