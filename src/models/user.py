from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import db_base


class User(db_base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)  # , unique=True, index=True
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # bidirectional relationship in one-to-many
    rates = relationship("Rating", back_populates="user")
