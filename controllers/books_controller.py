from flask import Blueprint, request, jsonify
from main import db
from models import Book
from schemas import book_schema, books_schema

books = Blueprint("books", __name__, url_prefix="/books")


@books.route("/", methods=["GET"])
def get_books():
    book_list = Book.query.all()
    return jsonify(books_schema.dump(book_list))


@books.route("/<int:id>", methods=["GET"])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"Error": "Book does not exist."})
    return jsonify(book_schema.dump(book))


@books.route("/", methods=["POST"])
def create_book():
    book_fields = book_schema.load(request.json)
    new_book = Book(
        title=book_fields['title'],
        genre=book_fields['genre'],
        year=book_fields['year'],
        length=book_fields['length'],
        author_id=1
    )
    db.session.add(new_book)
    db.session.commit()

    return jsonify(book_schema.dump(new_book))

