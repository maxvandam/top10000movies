import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
from ast import literal_eval
import imdb
import streamlit as st

ia = imdb.IMDb()

movieDF = pd.read_csv("Top_10000_Popular_Movies.csv",converters={'genre': literal_eval})
movieDF = movieDF.drop('Unnamed: 0',1)

movieDF2 = movieDF.sort_values("vote_average",ascending=False)

movieDF = movieDF[movieDF['vote_count'] > 10]
genreList = []

for ind, row in movieDF.iterrows():
    genreList.extend(row['genre'])

print(genreList)

def my_function(x):
  return list( dict.fromkeys(x) )

genreList = my_function(genreList)


Action = 0
Thriller = 0
Adventure = 0
Animation = 0
Comedy = 0
Fantasy = 0
Drama = 0
SciFi = 0
Documentary = 0
Crime = 0
Family = 0
Western = 0
History = 0
Romance = 0
Horror = 0
Mystery = 0
Music = 0
War = 0
TVmovie = 0

for col, row in movieDF.iterrows():
    if "Action" in row['genre']:
        Action = Action + 1
    if "Thriller" in row['genre']:
        Thriller = Thriller + 1
    if "Adventure" in row['genre']:
        Adventure = Adventure + 1
    if "Animation" in row['genre']:
        Animation = Animation + 1
    if "Comedy" in row['genre']:
        Comedy = Comedy + 1
    if "Fantasy" in row['genre']:
        Fantasy = Fantasy + 1
    if "Drama" in row['genre']:
        Drama = Drama + 1
    if "Science Fiction" in row['genre']:
        SciFi = SciFi + 1
    if "Documentary" in row['genre']:
        Documentary = Documentary + 1
    if "Crime" in row['genre']:
        Crime = Crime + 1
    if "Family" in row['genre']:
        Family = Family + 1
    if "Western" in row['genre']:
        Western = Western + 1
    if "History" in row['genre']:
        History = History + 1
    if "Romance" in row['genre']:
        Romance = Romance + 1
    if "Horror" in row['genre']:
        Horror = Horror + 1
    if "Mystery" in row['genre']:
        Mystery = Mystery + 1
    if "Music" in row['genre']:
        Music = Music + 1
    if "War" in row['genre']:
        War = War + 1
    if "TV Movie" in row['genre']:
        TVmovie = TVmovie + 1

genreDict = dict(
    genre=['Action', 'Thriller', 'Adventure', 'Animation', 'Comedy', 'Fantasy', 'Drama', 'SciFi', 'Documentary',
           'Crime', 'Family', 'Western', 'History', 'Romance', 'Horror', 'Mystery', 'Music', 'War', 'TV Movie'],
    count=[Action, Thriller, Adventure, Animation, Comedy, Fantasy, Drama, SciFi, Documentary, Crime, Family, Western,
           History, Romance, Horror, Mystery, Music, War, TVmovie])

genres = pd.DataFrame.from_dict(genreDict)
genres = genres.sort_values('count',ascending=False)


fig = px.bar(x=genres['genre'],y=genres['count'],labels=dict(x="Genre",y="Aantal waarnemingen"),title="Aantal waarnemingen van genres in top 10000 films")
st.plotly_chart(fig)