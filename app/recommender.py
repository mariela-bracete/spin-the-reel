#Movie recommendation function (content-based)

# Centralize repeating logic in this helper function
def recommend_by_title_helper(title, metadata, df, top_n=5):
    import pandas as pd

    if 'title' not in metadata.columns:
        raise ValueError("Expected a 'title' column in tmdb_df.csv")

    # Check if the title exists
    if title not in metadata['title'].values:
        raise ValueError(f"'{title}' not found in movie titles!")

    # Get the movie index for the input title
    movie_idx = metadata[metadata['title'] == title].index[0]

    # Get top N similar movies for that index
    similar_movies = df[df['movie_index'] == movie_idx].sort_values(
        by='similarity', ascending=False
    ).head(top_n)

    # Map back from index to title
    rec_titles = metadata.iloc[similar_movies['similar_index'].astype(int)]['title'].values

    return rec_titles

def recommend_by_title(title, metadata, df, top_n=5):
    import pandas as pd

    rec_titles = recommend_by_title_helper(title, metadata, df, top_n=5)

    rec_df = pd.DataFrame({'title': rec_titles})

    print(f"[DEBUG] Top {top_n} recommendations for '{title}':\n{rec_df}")

    return rec_df


def recommend_by_title_mongo(title, metadata, mongo_collection, df, top_n=5):
    import pandas as pd
    from pretty_html_table import build_table

    rec_titles = recommend_by_title_helper(title, metadata, df, top_n=5)

    # Find movies released after 2000 and only display the title and IMDb rating
    query = {"title": { "$in" : rec_titles.tolist() }}  # This query filters movies released after the year 2000
    projection = {"_id": 0, "title": 1, "vote_average": 1, "overview": 1}  # This projection specifies which fields to include in the result
    # The "_id": 0 excludes the default "_id" field from the result, while "title": 1 and "imdb.rating": 1 include the title and IMDb rating respectively
    results = list(mongo_collection.find(query, projection).limit(top_n))
    for movie in results:  # This loop iterates over the results of the query, limited to the first 10 matches
        print(movie)  # Each movie document is printed, showing only the title and IMDb rating as specified in the projection

    rec_df = build_table(pd.DataFrame(results), 'blue_light')

    return rec_df


def recommend_by_title_sql(title, metadata, conn, df, top_n=5):
    import pandas as pd
    from pretty_html_table import build_table

    rec_titles = recommend_by_title_helper(title, metadata, df, top_n=5)
    rec_titles = rec_titles.tolist()

    # Find movies released after 2000 and only display the title and IMDb rating
    query = "select title as Title, EXTRACT(YEAR FROM release_date) as Year, genre_clean as Genres, concat(runtime, ' mins') as Runtime FROM MOVIES where title IN %s" % repr(tuple(map(str,rec_titles)))
    print(query)
    results = pd.read_sql_query(query, conn)
    results['year'] = results['year'].astype(int)

    rec_df = build_table(results, 'blue_light')

    return rec_df



