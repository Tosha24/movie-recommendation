import streamlit as st
import pickle
import pandas as pd
import requests

#  my api key : 6889ba9b469310bdd34e213b6c83ca80
st.set_page_config(layout='wide')

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox('Select the movie you already watched', movies['title'].values)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6889ba9b469310bdd34e213b6c83ca80&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movie_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_poster


if st.button('Recommend'):
    st.text("")
    names, poster = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(poster[0])
        st.subheader(names[0])
        st.text("")
    with col2:
        st.image(poster[1])
        st.subheader(names[1])
        st.text("")
    with col3:
        st.image(poster[2])
        st.subheader(names[2])
        st.text("")
    with col4:
        st.image(poster[3])
        st.subheader(names[3])
        st.text("")
    with col5:
        st.image(poster[4])
        st.subheader(names[4])
        st.text("")
