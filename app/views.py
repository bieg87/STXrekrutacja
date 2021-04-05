from flask import Flask, request, render_template
from flask import Response

from flask_cors import CORS
from sqlalchemy import func, or_
from app.database import *
from app import application
from app.model import *

CORS(application)


@application.route('/')
def template():
    return render_template('index.html')


@application.route('/books', methods=['GET'])
def books():
    args = request.args
    published_date = args.get('published_date')
    author = args.get('author')

    if published_date is None and author is None:
        result = db_session.query(Books.id, Books.title, Books.published_date, func.group_concat(Authors.author,
                                                                                                 ', ').label(
            'author'), func.group_concat(Categories.category.distinct()).
                                  label('category')).join(Authors).join(Categories).group_by(Books.id).all()
        response = []
        for r in result:
            response.append(r._asdict())

        return {"books": response}
    else:
        published_data_filter = {}
        if published_date is not None:
            published_data_filter = {'published_date': published_date}

        published_data_filter = {key: value for (key, value) in published_data_filter.items() if value}

        author_filter = {}
        if author is not None:
            author_filter = {'author': author}

        author_filter = {key: value for (key, value) in author_filter.items() if value}

        result = db_session.query(Books.id, Books.title, Books.published_date,
                                  func.group_concat(Authors.author, ', ').label('author'),
                                  func.group_concat(Categories.category.distinct()).label('category')).filter_by(
            **published_data_filter).join(Authors).filter_by(**author_filter).join(Categories).group_by(Books.id).all()

        response = []
        for r in result:
            response.append(r._asdict())

        print(response)

        return {"books": response}


@application.route('/books/<book_id>', methods=['GET'])
def books_id(book_id):
    result = db_session.query(Books.id, Books.title, Books.published_date,
                              func.group_concat(Authors.author, ', ').label('author'),
                              func.group_concat(Categories.category.distinct()).label('category')).filter_by(
        id=book_id).join(Authors).join(Categories).group_by(Books.id).all()

    response = []

    for r in result:
        response.append(r._asdict())

    return {"book": response}


@application.route('/db', methods=['POST'])
def add():
    data = request.json
    books_list = data['items']

    for book in books_list:
        book_id = book['id']
        title = book['volumeInfo']['title']
        published_date = book['volumeInfo']['publishedDate']
        authors = book['volumeInfo']['authors'] if 'authors' in book['volumeInfo'] else None
        categories = book['volumeInfo']['categories'] if 'categories' in book['volumeInfo'] else None
        average_rating = book['volumeInfo']['averageRating'] if 'averageRating' in book['volumeInfo'] else None
        ratings_count = book['volumeInfo']['ratingsCount'] if 'ratingsCount' in book['volumeInfo'] else None
        book_to_insert = Books(id=book_id, title=title, published_date=published_date,
                               average_rating=average_rating, ratings_count=ratings_count)
        db_session.add(book_to_insert)

        for author in authors if authors else []:
            author_to_insert = Authors(author=author, books_id=book_id)
            db_session.add(author_to_insert)

        for category in categories if categories else []:
            category_to_insert = Categories(category=category, books_id=book_id)
            db_session.add(category_to_insert)

        db_session.flush()

    return Response("{ok}", status=201, mimetype='application/json')

