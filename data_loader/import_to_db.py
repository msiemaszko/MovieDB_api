from time import time
import pandas as pd

from data_loader.read_from_file import read_clear_movies, read_rating, read_users
from data_loader.dump_params import *
from data_loader.dump_params import reduce_movie_id_to
from data_loader.reduce_datafile import reduce_data_file

from src.database import db_base, db_engine, db_session
from src.models.movie import Movie
from src.models.rating import Rating
from src.models.user import User


users, movies = pd.DataFrame, pd.DataFrame


def import_all():
    print("Apply migrations to db: ", end='')
    db_base.metadata.create_all(bind=db_engine)
    print("success")

    print("Reducing size of imported data to ", reduce_movie_id_to, "records: ", end='')
    reduce_data_file()

    print("Starting data import...")
    now = time()
    import_users()
    import_movies()
    import_ratings()
    print("Time elapsed: " + str(time() - now) + " s.")


# ## USERS ##
def import_users():
    global users
    (row_success, row_error) = (0, 0)
    ses = db_session()
    users = read_users(full_user_csv)
    users = users[:-10]  # drop last 10 rows
    for user in users.values:
        try:
            record = User(
                **{
                    # "id": user[0],  # - nie wstawiam id, bo popsuje auto increment
                    "full_name": user[1],
                    "email": user[2],
                    "hashed_password": user[3],
                    "is_active": user[4],
                }
            )
            ses.add(record)
            ses.commit()
            row_success += 1
        except:
            ses.rollback()
            ses = db_session()
            row_error += 1
    ses.close()
    print(f"User table results: success: {row_success}, failed: {row_error}")


# ## MOVIES ##
def import_movies():
    global movies
    (row_success, row_error) = (0, 0)
    ses = db_session()
    movies = read_clear_movies(reduced_movie_csv)
    for movie in movies.values:
        try:
            record = Movie(
                **{
                    "id": movie[0],
                    "imdb_id": movie[1],
                    "title": movie[2],
                    "genres": movie[3],
                    "release_date": movie[4],
                    "overview": movie[5],
                    "vote_average": movie[6],
                    "vote_count": movie[7],
                    "popularity": movie[8],
                    "budget": movie[9],
                    "release_year": movie[10]
                }
            )
            ses.add(record)
            ses.commit()
            row_success += 1
        except:
            ses.rollback()
            ses = db_session()
            row_error += 1
    ses.close()
    print(f"Movie table results: success: {row_success}, failed: {row_error}")


# ## RATING ##
def import_ratings():
    (row_success, row_error) = (0, 0)
    ses = db_session()
    ratings = read_rating(reduced_rating_csv)
    ratings = ratings[ratings["movieId"].isin(movies['id'])]
    ratings = ratings[ratings["userId"].isin(users['id'])]
    for rating in ratings.values:
        try:
            record = Rating(
                **{"user_id": rating[0], "movie_id": rating[1], "rating": rating[2], "time_stamp": rating[3]}
            )
            ses.add(record)
            ses.commit()
            row_success += 1
        except:
            row_error += 1
            ses.rollback()
            ses = db_session()
    ses.close()
    print(f"Rating table results: success: {row_success}, failed: {row_error}")


if __name__ == "__main__":
    import_all()
