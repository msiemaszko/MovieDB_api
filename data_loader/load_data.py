from time import time
from get_data import read_clear_movies, read_rating, read_users
from models import User, Movie, Rating
from database import db_session, db_base, db_engine

# Apply migrations to db and populate it
db_base.metadata.create_all(bind=db_engine)
now = time()

### USERS
(row_succes, row_error) = (0,0)
ses = db_session()
data = read_users().values
for i in data:
    try:
        record = User(**{
            'id': i[0],
            'full_name': i[1],
            'email': i[2],
            'hashed_password': i[3],
            'is_active': i[4]
        })
        ses.add(record)
        ses.commit()
        row_succes += 1
    except:
        ses.rollback()
        ses = db_session()
        row_error += 1
ses.close()
print(f"User result: succes: {row_succes}, faild: {row_error}")

### MOVIES
(row_succes, row_error) = (0,0)
ses = db_session()
data = read_clear_movies().values
for i in data:
    try:
        record = Movie(**{
            'id': i[0],
            'imdb_id': i[1],
            'title': i[2],
            'genres': i[3],
            'release_date': i[4],
            'overview': i[5]
        })
        ses.add(record)
        ses.commit()
        row_succes += 1
    except:
        ses.rollback()
        ses = db_session()
        row_error += 1
ses.close()
print(f"Movie result: succes: {row_succes}, faild: {row_error}")


### RATING
(row_succes, row_error) = (0,0)
ses = db_session()
data = read_rating().values
for i in data:
    try:
        record = Rating(**{
            'user_id': i[0],
            'movie_id': i[1],
            'rating': i[2],
            'time_stamp': i[3]
        })
        ses.add(record)
        ses.commit()
        row_succes += 1
    except:
        row_error += 1
        ses.rollback()
        ses = db_session()
ses.close()
print(f"Rating result: succes: {row_succes}, faild: {row_error}")

print("Time elapsed: " + str(time() - now) + " s.")


# MOVIE COPY
# try:
#     ses = db_session()
#     data = read_clear_movies()
#     data = data.values
#
#     for i in data:
#         record = Movie(**{
#             'id': i[0],
#             'imdb_id': i[1],
#             'title': i[2],
#             'genres': i[3],
#             'release_date': i[4],
#             'overview': i[5]
#         })
#         ses.add(record)
#
#     ses.commit()
#     print("Movie commited");
# except:
#     ses.rollback()
#     print("Movie exception:", sys.exc_info()[1])
# finally:
#     ses.close()
#     print("Movie session close\n");