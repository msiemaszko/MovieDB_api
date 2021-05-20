from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

db_base = declarative_base()

db_engine = create_engine("sqlite:///../sql_app.db")
db_base.metadata.create_all(db_engine)

db_session = sessionmaker()
db_session.configure(bind=db_engine)
