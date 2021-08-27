
full_movie_csv = "data_dump/full/movies_metadata.csv"
full_rating_csv = "data_dump/full/ratings.csv"
full_user_csv = "data_dump/full/users.csv"

reduced_movie_csv = "data_dump/reduced/movies_metadata.csv"
reduced_rating_csv = "data_dump/reduced/ratings.csv"

reduce_movie_id_to = 1000

movies_metadata_use_cols = [
    "id",
    "imdb_id",
    "title",
    "genres",
    "release_date",
    "overview",
    "vote_average",
    "vote_count",
    "popularity",
    "budget"
]
