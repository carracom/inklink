from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from utils.database import Base

class AuthorDB(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)

    books = relationship("BookDB", back_populates="author")