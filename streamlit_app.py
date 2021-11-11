import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
from ast import literal_eval
import imdb
import streamlit as st
import geopandas as gpd

ia = imdb.IMDb()

st.set_page_config(layout="wide")
st.image("https://i.imgur.com/ZbOOGMN.png")
st.title("Dashboard analyse Top 10.000 films op TMDB")
st.subheader("Door Max van Dam en Gian van Veen")
col1, col2 = st.columns(2)
col1.header("Genres analyse")
col2.header("Top 50 films analyse")


movieDF = pd.read_csv("Top_10000_Popular_Movies.csv", converters={'genre': literal_eval})
movieDF = movieDF.drop('Unnamed: 0', 1)

movieDF2 = movieDF.sort_values("vote_average", ascending=False)

movieDF = movieDF[movieDF['vote_count'] > 10]
genreList = []

for ind, row in movieDF.iterrows():
    genreList.extend(row['genre'])


def my_function(x):
    return list(dict.fromkeys(x))


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
genres = genres.sort_values('count', ascending=False)

fig = px.bar(x=genres['genre'], y=genres['count'], labels=dict(x="Genre", y="Aantal waarnemingen"),
             title="Aantal waarnemingen van genres in top 10000 films")

with col1:
    st.subheader("De onderstaande histogram laat zien hoe vaak elk genre terugkomt in de top 10.000 films van TMDB.")
    st.plotly_chart(fig)

movieDFHigh = movieDF.sort_values('vote_average', ascending=False)
movieDFHigh = movieDFHigh[movieDFHigh['original_language'] == 'en']
# movieTop50 = movieDFHigh.head(50)

# ratings = []

# for ind,row in movieTop50.iterrows():
#    code = ia.search_movie(row['original_title'])[0].movieID
#    rating = ia.get_movie(code).data['rating']
#    ratings.append(rating)

# movieTop50['IMDB_rating'] = ratings
movieTop50 = pd.read_csv("movieTop50.csv")

with col2:
    st.subheader("Dit is het DataFrame van de top 50 Engelstalige films van TMDB.")
    st.dataframe(movieTop50)

df1 = movieTop50
df1.rename(columns={"vote_average": "TMDB rating", "IMDB_rating": "IMDB rating", "original_title": "Title"},
           inplace=True)

fig = px.scatter(df1,
                 x="TMDB rating",
                 y="IMDB rating",
                 title='TMDB ratings vs IMDB ratings van top 50 Engelstalige TMDB films',
                 labels=dict(x='TMDB rating', y='IMDB rating'),
                 color="Title",
                 hover_name="Title",
                 hover_data=["TMDB rating", "IMDB rating", "genre"])
fig.update_layout(legend_title_text='Movie name')

with col2:
    st.subheader(
        "Onderstaand scatterplot laat de vergelijking zien van de IMDB cijfers en de TMDB cijfers van de top 50 Engelstalige films. De IMDB cijfers zijn opgehaald door het 'imdbpy' package te gebruiken om de IMDB API te gebruiken.")
    st.plotly_chart(fig)

fig = go.Figure()

for genre in genreList:
    tempList = [genre]
    tempDF = movieDF['genre'].apply(lambda s: len(set(s) & set(tempList)) > 0)
    df = movieDF[tempDF]
    fig.add_trace(go.Box(x=df['vote_average'], legendgroup=genre, showlegend=True,
                         name=genre))  # legendgrouptitle={"text":genre}))

fig.update_layout(title="Verdeling cijfers van films per genre", xaxis_title="Cijfer", yaxis_title="Genre")

with col1:
    st.subheader("De boxplots laten voor elk genre van films zien hoe de TMDB cijfers zijn verdeeld.")
    st.plotly_chart(fig)

# Start map

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


def landPicker(lan):
    if lan == 'en':
        return ('United States of America')
    elif lan == 'ja':
        return ('Japan')
    elif lan == 'es':
        return ('Spain')
    elif lan == 'fr':
        return ('France')
    elif lan == 'ko':
        return ('South Korea')
    elif lan == 'zh':
        return ('China')
    elif lan == 'it':
        return ('Italy')
    elif lan == 'cn':
        return ('China')
    elif lan == 'de':
        return ('Germany')
    elif lan == 'ru':
        return ('Russia')
    elif lan == 'hi':
        return ('India')
    elif lan == 'pt':
        return ('Brazil')
    elif lan == 'no':
        return ('Norway')
    elif lan == 'da':
        return ('Denmark')
    elif lan == 'sv':
        return ('Sweden')
    elif lan == 'nl':
        return ('Netherlands')
    elif lan == 'pl':
        return ('Poland')
    elif lan == 'th':
        return ('Thailand')
    elif lan == 'tr':
        return ('Turkey')
    elif lan == 'id':
        return ('Indonesia')
    elif lan == 'fi':
        return ('Finland')
    elif lan == 'te':
        return ('India')
    elif lan == 'cs':
        return ('Czechia')
    elif lan == 'sr':
        return ('Serbia')
    elif lan == 'he':
        return ('Israel')
    elif lan == 'ro':
        return ('Romania')
    elif lan == 'Fa':
        return ('Iran')
    elif lan == 'eu':
        return ('Spain')
    elif lan == 'ar':
        return ('Saudi Arabia')
    elif lan == 'el':
        return ('Greece')
    elif lan == 'ta':
        return ('India')
    elif lan == 'nb':
        return ('Norway')
    elif lan == 'is':
        return ('Iceland')
    elif lan == 'ms':
        return ('Malaysia')
    elif lan == 'hu':
        return ('Hungary')
    elif lan == 'bn':
        return ('Iran')
    elif lan == 'tl':
        return ('Philippnes')
    elif lan == 'la':
        return ('Italy')


df_movies = movieDF.copy()

df_movies['vote_avg'] = df_movies.groupby('original_language')['vote_average'].transform('mean')
df_movies['aantal_films'] = df_movies.groupby('original_language')['vote_average'].transform('size')

df_movies.drop_duplicates(subset="original_language",keep="first",inplace=True)

testList = []
for ind, row in df_movies.iterrows():
    test = [landPicker(row['original_language'])]
    testList.extend(test)

df_movies['name'] = testList
df_movies = df_movies.merge(world, on='name')

gdf_movies = gpd.GeoDataFrame(df_movies, geometry='geometry')

gdf_movies = gdf_movies.to_crs(epsg=4326)

gdf_movies = gdf_movies.round({"vote_avg":2})

fig = px.choropleth_mapbox(gdf_movies,
                           geojson=gdf_movies.geometry,
                           locations=gdf_movies.index,
                           color='vote_avg',
                           hover_name='name',
                           hover_data=["vote_avg",'aantal_films'],
                           color_continuous_scale=px.colors.sequential.Reds,
                           mapbox_style="carto-positron",
                           zoom=1)
fig.update_layout(title='Gemiddeld cijfer per land')

gdf_movies = gdf_movies[["original_language","name","vote_avg","aantal_films"]]
gdf_movies = gdf_movies.sort_values("aantal_films",ascending=False)

with col1:
    st.header("Kaart van landen waar films afspelen")
    st.subheader("De onderstaande kaart laat per land zien welk cijfer films uit dat land gemiddeld hebben.")
    st.plotly_chart(fig)
    st.caption("Deze informatie is ook te vinden in onderstaand DataFrame:")
    st.dataframe(gdf_movies)

maxReviews = pd.read_csv('moviereviews.csv', encoding="ISO-8859-1")

reviews = maxReviews.merge(movieDF, left_on="Title", right_on="original_title", how="left")

df1 = reviews.copy()
df1.rename(columns={"vote_average": "TMDB rating", "Grade": "Max rating", "original_title": "title"}, inplace=True)

fig = px.scatter(df1,
                 x="TMDB rating",
                 y="Max rating",
                 title='TMDB ratings vs Max ratings',
                 labels=dict(x='TMDB rating', y='Max rating'),
                 color="Title",
                 hover_name="Title",
                 hover_data=["TMDB rating", "Max rating", "genre"])
fig.update_layout(legend_title_text='Movie name')


with col2:
    st.header("Vergelijking van Max zijn film cijfers")
    st.subheader(
        "De onderstaande scatterplot geeft een visualisatie weer van de TMDB ratings van films vergeleken met de cijfers die Max aan deze films heeft gegeven.")
    st.plotly_chart(fig)


st.image("https://i.imgur.com/ZbOOGMN.png")