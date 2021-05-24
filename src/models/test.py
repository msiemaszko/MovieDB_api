from sqlalchemy import (Column, Float, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from src.database import db_base



class Bug(db_base):
    __tablename__ = 'bug'
    id = Column('bug_id', Integer, primary_key=True)
    tags = relationship('Tag', backref='bug')

class Tag(db_base):
    id = Column('tag_id', Integer, primary_key=True)
    name = Column('tag_name', String)
    bug_id = Column('bug_id', ForeignKey('bug.bug_id'))