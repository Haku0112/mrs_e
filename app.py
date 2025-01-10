import streamlit as st
import pickle
import pandas as pd
import requests

#https://api.themoviedb.org/3/movie/1363?api_key=2607986bf31bbce91fe94fdbdf75cd23&language=en-US
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=2607986bf31bbce91fe94fdbdf75cd23&language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNjA3OTg2YmYzMWJiY2U5MWZlOTRmZGJkZjc1Y2QyMyIsIm5iZiI6MTczNjM1NDMzNy4zNzIsInN1YiI6IjY3N2VhYTIxMTI2Njc5Njg4NTRlNzMxZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XhR0TjctzKPkog-0iPkHYeukldiPNp_TfWLLxqRVFWk"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

##Recommendation of 5 similar movies
def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster =[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetching poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))
    
    return recommended_movies,recommended_movies_poster    


movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))
        
st.title('Movie Recommender System')
selected_movie = st.selectbox(
    'Select movie',
    (movies['title'].values)
)

#creting recommend button functionality

if st.button('Recommend'):
    #st.write(selected_movie)
    recommendations,posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])