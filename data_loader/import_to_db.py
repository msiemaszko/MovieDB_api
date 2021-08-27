from time import time
from data_loader.read_from_file import read_clear_movies, read_rating, read_users

from src.database import db_base, db_engine, db_session
from src.models.movie import Movie
from src.models.rating import Rating
from src.models.user import User

from data_loader.dump_params import *


def import_all():
    print("Apply migrations to db: ", end='')
    db_base.metadata.create_all(bind=db_engine)
    print("success")

    print("Starting data import...")
    now = time()
    import_users()
    import_movies()
    import_ratings()
    print("Time elapsed: " + str(time() - now) + " s.")


# ## USERS ##
def import_users():
    (row_success, row_error) = (0, 0)
    ses = db_session()
    data = read_users(full_user_csv).values
    for i in data:
        try:
            record = User(
                **{
                    "id": i[0],
                    "full_name": i[1],
                    "email": i[2],
                    "hashed_password": i[3],
                    "is_active": i[4],
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
    print(f"User result: success: {row_success}, failed: {row_error}")


# ## MOVIES ##
def import_movies():
    (row_success, row_error) = (0, 0)
    ses = db_session()
    data = read_clear_movies(reduced_movie_csv).values
    for i in data:
        try:
            record = Movie(
                **{
                    "id": i[0],
                    "imdb_id": i[1],
                    "title": i[2],
                    "genres": i[3],
                    "release_date": i[4],
                    "overview": i[5],
                    "vote_average": i[6],
                    "vote_count": i[7],
                    "popularity": i[8],
                    "budget": i[9],
                    "release_year": i[10]

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
    print(f"Movie result: success: {row_success}, failed: {row_error}")


# ## RATING ##
def import_ratings():
    (row_success, row_error) = (0, 0)
    ses = db_session()
    data = read_rating(reduced_rating_csv).values
    for i in data:
        try:
            record = Rating(
                **{"user_id": i[0], "movie_id": i[1], "rating": i[2], "time_stamp": i[3]}
            )
            ses.add(record)
            ses.commit()
            row_success += 1
        except:
            row_error += 1
            ses.rollback()
            ses = db_session()
    ses.close()
    print(f"Rating result: success: {row_success}, failed: {row_error}")


if __name__ == "__main__":
    import_all()
