import streamlit as st
import pandas as pd
import pickle



with open(r"C:\Users\thaku\OneDrive\Desktop\.ipynb_checkpoints\movie_data.pkl", "rb") as file:
    movies, cosine_sim = pickle.load(file)

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title']==title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]       # get top 10 movies and for top 5 write 1:6
    movies_indices = [i[0] for i in sim_scores]
    return movies.iloc[movies_indices]


import requests

def fetch_poster(movie_id):
    api_key = "c1ffd3b562b6ef201d2ba66f1f1fb7e2"
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    poster_path = data.get('poster_path')  # SAFE
    
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


import streamlit as st

# Define the dropdown BEFORE using it
selected_movie = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

# Now you can use it in the button
if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    st.write("Top 10 recommended movies:")
    for movie in recommendations:
        st.write(movie)

    # Create a 2x5 grid layout
    for i in range(0, 10, 5):  #loop over rows (2 rows, 5 movies each)
        cols = st.columns(5)   # create 5 columns foreach row     and col is column
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    st.image(poster_url, width=130)
                    st.write(movie_title)


        
        