from sqlalchemy import Boolean, Column, Integer, String

from database.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    root_path = Column(String)
    filename = Column(String)
    is_approved = Column(Boolean, default=False)
    thumbnail_path = Column(String)
