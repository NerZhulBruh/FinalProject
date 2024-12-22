from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import re

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://www.kinoafisha.info/rating/movies/"
driver.get(url)
time.sleep(5)

titles = []
ratings = []
genres = []
years = []

movies = driver.find_elements(By.CLASS_NAME, "movieItem")

for movie in movies:
    try:
        title = movie.find_element(By.CLASS_NAME, "movieItem_title").text
    except:
        title = "N/A"
    titles.append(title)
    try:
        rating = movie.find_element(By.CLASS_NAME, "movieItem_rating").text
    except:
        rating = "N/A"
    ratings.append(rating)
    try:
        details = movie.find_element(By.CLASS_NAME, "movieItem_details")
        genre = details.find_element(By.CLASS_NAME, "movieItem_genres").text
        year = details.find_element(By.CLASS_NAME, "movieItem_year").text
    except:
        genre, year = "N/A", "N/A"
    genres.append(genre)
    years.append(year)

driver.quit()
data = {
    "Title": titles,
    "Rating": ratings,
    "Genres": genres,
    "Year": years
}
df = pd.DataFrame(data)

print(df)
df.to_csv("movies_ratings.csv", index=False, encoding="utf-8")


file_path = 'IMDb_Data_final.csv'
df2 = pd.read_csv(file_path)
df2.dropna(inplace=True)

def clean_duration(duration):
    duration = re.sub(r'min', '', str(duration)).strip()
    return int(duration) if duration else None

df2['Duration'] = df2['Duration'].apply(clean_duration)
df2['ReleaseYear'] = pd.to_numeric(df2['ReleaseYear'], errors='coerce')
df2['Stars'] = df2['Stars'].str.replace(',', ', ')
df[['Year', 'Country']] = df['Year'].str.split(', ', expand=True)

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Movie Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Filter by Category:"),
        dcc.Dropdown(
            id="category-filter",
            options=[{"label": cat, "value": cat} for cat in df2["Category"].unique()],
            value=None,
            placeholder="Select Category",
            multi=True
        ),
        html.Label("Filter by Release Year:"),
        dcc.RangeSlider(
            id="year-slider",
            min=df2["ReleaseYear"].min(),
            max=df2["ReleaseYear"].max(),
            step=1,
            marks={year: str(year) for year in range(int(df2["ReleaseYear"].min()), int(df2["ReleaseYear"].max()), 5)},
            value=[df2["ReleaseYear"].min(), df2["ReleaseYear"].max()]
        )
    ], style={"margin-bottom": "20px"}),

    html.Div([
        dcc.Graph(id="rating-duration-scatter"),
        dcc.Graph(id="category-bar-chart"),
        dcc.Graph(id="director-rating-bar-chart"),
        dcc.Graph(id="censor-rating-scatter"),
        dcc.Graph(id="genre-pie-chart"),
        dcc.Graph(id="movie-trends-line-chart-df"),
        dcc.Graph(id="movie-trends-line-chart-df2"),
    ])
])

@app.callback(
    [
        Output("rating-duration-scatter", "figure"),
        Output("category-bar-chart", "figure"),
        Output("director-rating-bar-chart", "figure"),
        Output("censor-rating-scatter", "figure"),
        Output("genre-pie-chart", "figure"),
        Output("movie-trends-line-chart-df", "figure"),
        Output("movie-trends-line-chart-df2", "figure"),
    ],
    [
        Input("category-filter", "value"),
        Input("year-slider", "value"),
    ]
)
def update_graphs(selected_categories, selected_years):
    filtered_df2 = df2.copy()
    if selected_categories:
        filtered_df2 = filtered_df2[filtered_df2["Category"].isin(selected_categories)]
    if selected_years:
        filtered_df2 = filtered_df2[
            (filtered_df2["ReleaseYear"] >= selected_years[0]) &
            (filtered_df2["ReleaseYear"] <= selected_years[1])
        ]

    scatter_fig = px.scatter(
        filtered_df2,
        x="Duration",
        y="IMDb-Rating",
        color="Category",
        hover_data=["Title", "Director"],
        title="IMDb Rating vs Duration (df2)"
    )

    category_counts = filtered_df2["Category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Count"]
    bar_fig = px.bar(
        category_counts,
        x="Category",
        y="Count",
        title="Number of Movies by Category (df2)",
        labels={"Category": "Category", "Count": "Number of Movies"}
    )

    director_rating = filtered_df2.groupby("Director", as_index=False)["IMDb-Rating"].mean()
    director_rating_fig = px.bar(
        director_rating,
        x="Director",
        y="IMDb-Rating",
        title="Average IMDb Rating by Director (df2)",
        labels={"IMDb-Rating": "Average IMDb Rating"}
    )

    censor_rating_fig = px.box(
        filtered_df2,
        x="Censor-board-rating",
        y="IMDb-Rating",
        title="Censor Board Rating vs IMDb Rating (df2)",
        labels={"Censor-board-rating": "Censor Board Rating", "IMDb-Rating": "IMDb Rating"}
    )

    genre_counts = df["Genres"].str.split(", ", expand=True).stack().value_counts().reset_index()
    genre_counts.columns = ["Genre", "Count"]
    genre_pie_chart = px.pie(
        genre_counts,
        names="Genre",
        values="Count",
        title="Distribution of Movie Genres (df)"
    )

    movie_trends_df = df.groupby("Year").size().reset_index(name="Count")
    movie_trends_line_chart_df = px.line(
        movie_trends_df,
        x="Year",
        y="Count",
        title="Movie Release Trends (df)",
        labels={"Year": "Year", "Count": "Number of Movies"}
    )

    movie_trends_df2 = df2.groupby("ReleaseYear").size().reset_index(name="Count")
    movie_trends_line_chart_df2 = px.line(
        movie_trends_df2,
        x="ReleaseYear",
        y="Count",
        title="Movie Release Trends (df2)",
        labels={"ReleaseYear": "Release Year", "Count": "Number of Movies"}
    )

    return scatter_fig, bar_fig, director_rating_fig, censor_rating_fig, genre_pie_chart, movie_trends_line_chart_df, movie_trends_line_chart_df2

if __name__ == "__main__":
    app.run_server(debug=True)