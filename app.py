import streamlit as st 
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2435c28a2b20d56e871865b384c6619a&language=en-US'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse = True , key = lambda x:x[1])[1:6]


    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
       movie_id = movies.iloc[i[0]].movie_id
       recommended_movies.append(movies.iloc[i[0]].title)
             
       #next we will get the poster from the api
       recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict) # movies is the name of the dataframe here 

similarity = pickle.load(open('similarity.pkl', 'rb'))




st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    'Search for the movie you are looking for ',
    (movies['title'].values)
)

left_column, center_column, right_column = st.columns([1,1,1])

names = []  # Initialize as empty lists
posters = []

with center_column:
    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)

if names:  
    num_images = len(names)
    # We need 2 * num_images - 1 columns to include gaps
    total_cols_with_gaps = (2 * num_images) - 1
    cols = st.columns(total_cols_with_gaps)
    image_cols = [cols[i] for i in range(total_cols_with_gaps) if i % 2 == 0]
    
    for i, col in enumerate(image_cols):
        with col:
            st.text(names[i])
            st.image(posters[i], width=150)  # Adjust width as needed



