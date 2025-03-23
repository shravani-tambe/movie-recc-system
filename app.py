import streamlit as st  
import pickle 
import pandas as pd 
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b1ebec86ca7dd514f8d923cfdd6f496d&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    
    return recommended_movie_names, recommended_movie_posters

st.header("Movie Recommender System")

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown menu",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)  # Create 5 equal-width columns
    
    for i in range(5):
        with cols[i]:
            st.image(recommended_movie_posters[i], use_column_width=True)  # Ensures uniform width
            st.markdown(f"<p style='text-align: center; font-weight: bold;'>{recommended_movie_names[i]}</p>", unsafe_allow_html=True)