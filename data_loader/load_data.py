import sys
from time import time
from get_data import read_clear_movies, read_rating, read_users;
from models import User, Movie, Rating
from database import db_session, db_base, db_engine
db_base.metadata.create_all(bind=db_engine)

now = time()

### USERS
try:
    ses = db_session()
    df = read_users()
    data = df.values

    for i in data:
        record = User(**{
            'id': i[0],
            'full_name': i[1],
            'email': i[2],
            'hashed_password': i[3],
            'is_active': i[4]
        })
        ses.add(record) #Add all the records

    ses.commit() #Attempt to commit all the records
    print("User commited");
except:
    ses.rollback() #Rollback the changes on error
    print("User exception:", sys.exc_info()[1])
finally:
    ses.close() #Close the connection
    print("User session close\n");


### MOVIES
try:
    ses = db_session()
    data = read_clear_movies()
    data = data.values

    for i in data:
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
    print("Movie commited");
except:
    ses.rollback()
    print("Movie exception:", sys.exc_info()[1])
finally:
    ses.close()
    print("Movie session close\n");


### RATING
try:
    ses = db_session()
    data = read_rating()
    data = data.values

    for i in data:
        record = Rating(**{
        'user_id': i[0],
        'movie_id': i[1],
        'rating': i[2],
        'time_stamp': i[3]
        })
        ses.add(record)

    ses.commit()
    print("Rating commited");
except:
    ses.rollback()
    print("Rating exception:", sys.exc_info()[1])
finally:
    ses.close() #Close the connection
    print("Rating session close\n")

print("Time elapsed: " + str(time() - now) + " s.")