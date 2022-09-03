from flask import Blueprint, request, jsonify, abort
from main import db
from models import Book
from schemas import book_schema, books_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

books = Blueprint("books", __name__, url_prefix="/books")


def librarian_only(function):
    def wrapper(*args, **kwargs):
        if "lib" in get_jwt_identity():
            return function(*args, **kwargs)
        else:
            return abort(403, description="Unauthorised.")

    return wrapper


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
@jwt_required()
@librarian_only
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


@books.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_book(id):
    book = Book.query.get(id)

    if not book:
        return abort(400, description="Book not found.")

    book_fields = book_schema.load(request.json)
    book.title = book_fields.get("title", book.title)
    book.genre = book_fields.get("genre", book.genre)
    book.year = book_fields.get("year", book.year)
    book.length = book_fields.get("length", book.length)
    book.author_id = book_fields.get("author_id", book.author_id)

    db.session.commit()
