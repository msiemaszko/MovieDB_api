from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, inspect
from sqlalchemy.orm import relationship

from src.database import db_base


class Item(db_base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # owner = relationship("User", back_populates="items")
