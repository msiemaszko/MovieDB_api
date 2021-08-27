from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.consts.db_const import SQLALCHEMY_DATABASE_URL, POSTGRESQL_DATABASE_URL

db_engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    POSTGRESQL_DATABASE_URL
)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

db_base = declarative_base()


# Dependencies
def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
