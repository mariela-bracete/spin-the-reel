from flask import Blueprint, render_template, request
import pandas as pd
import psycopg
from recommender import recommend_by_title
from recommender import recommend_by_title_mongo
from recommender import recommend_by_title_sql
from pymongo import MongoClient

#Connect to Postgres
db_user = 'postgres'
db_password = '123'  
db_host = 'localhost'
db_port = '5432'
db_name = 'movies_db'

conn = psycopg.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password)

cur = conn.cursor()

# Load movie metadata to match title to index
query = "SELECT * FROM MOVIES"
metadata = pd.read_sql_query(query, conn)
#metadata = pd.read_csv('data/tmdb_df.csv')

print("Finished querying metadata")

#Connect to Mongo
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["movies_db"]
mongo_collection = mongo_db["movies_collection"]
parquet_collection = mongo_db["parquet"]
# Get parquet data
df = pd.read_parquet('data/precomputed_recs.parquet')
#df = pd.DataFrame(list(mongo_collection.find()))

print("Finished querying parquet")

routes = Blueprint('main', __name__)

@routes.route('/', methods=['GET', 'POST'])
def home():
    recommendations = None
    movie_title = None
    error = None

    if request.method == 'POST':
        movie_title = request.form.get('title')
        print(f"User entered title: '{movie_title}'")  # Debug: input title

        try:
            recommendations_df = recommend_by_title(movie_title, metadata, df, top_n=5)
            print(f"Recommendations for '{movie_title}':\n{recommendations_df}")  # Debug: output
            recommendations = recommendations_df.to_dict(orient='records')
        except Exception as e:
            error = f"Something went wrong: {str(e)}"
            print(error)  # Debug: show error in terminal

    return render_template('index.html', recommendations=recommendations, movie_title=movie_title, error=error)

@routes.route('/mongo', methods=['GET', 'POST'])
def mongo():
    recommendations_df = None
    movie_title = None
    error = None

    if request.method == 'POST':
        movie_title = request.form.get('title')
        print(f"User entered title: '{movie_title}'")  # Debug: input title

        try:
            recommendations_df = recommend_by_title_mongo(movie_title, metadata, mongo_collection, df, top_n=5)
            print(f"Recommendations for '{movie_title}':\n{recommendations_df}")  # Debug: output
        except Exception as e:
            error = f"Something went wrong: {str(e)}"
            print(error)  # Debug: show error in terminal

    return render_template('mongo.html', movie_title=movie_title, error=error, df_table=recommendations_df)

@routes.route('/postgres', methods=['GET', 'POST'])
def postgres():
    recommendations_df = None
    movie_title = None
    error = None

    if request.method == 'POST':
        movie_title = request.form.get('title')
        print(f"User entered title: '{movie_title}'")  # Debug: input title

        try:
            recommendations_df = recommend_by_title_sql(movie_title, metadata, conn, df, top_n=5)
            print(f"Recommendations for '{movie_title}':\n{recommendations_df}")  # Debug: output
        except Exception as e:
            error = f"Something went wrong: {str(e)}"
            print(error)  # Debug: show error in terminal

    return render_template('postgres.html', movie_title=movie_title, error=error, df_table=recommendations_df)

