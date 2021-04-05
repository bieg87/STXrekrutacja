from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.database import Base


class Books(Base):
    __tablename__ = 'books'
    id = Column(String(50), primary_key=True)
    title = Column(String(120))
    published_date = Column(String(120))
    average_rating = Column(Float)
    ratings_count = Column(Integer)
    thumbnail = Column(String(300))


class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    author = Column(String(120))
    books_id = Column(String(50), ForeignKey('books.id'))


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category = Column(String(120))
    books_id = Column(String(50), ForeignKey('books.id'))
