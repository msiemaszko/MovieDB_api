from src.database import get_db, db_session
from src.models import Movie, User, Rating
from data_loader.import_to_db import import_all

db = db_session()
try:
    print("Database migration check: ", end='')
    if \
        db.query(Movie).count() == 0 or \
        db.query(User).count() == 0 or \
        db.query(Rating).count() == 0:
        raise Exception('db is empty')
    print("data already populated.")
except:
    print("import is required!")
    import_all()
