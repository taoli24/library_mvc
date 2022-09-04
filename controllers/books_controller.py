from flask import Blueprint, request, jsonify, abort
from main import db
from models import Book, Reservation, User
from schemas import book_schema, books_schema, reservations_schema, reservation_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_util import librarian_only

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


@books.route("/reservations", methods=["GET"])
@jwt_required()
@librarian_only
def get_reservations():
    reservation_list = Reservation.query.all()
    return jsonify(reservations_schema.dump(reservation_list))


@books.route("/<int:id>/reservations", methods=["POST"])
@jwt_required()
def create_reservation(id):
    book = Book.query.get(id)
    if not book:
        return abort(401, description="Book does not exist in the database.")
    user_id = get_jwt_identity()
    if "lib" in user_id:
        return abort(401, description="Only users can make reservations.")
    user = User.query.get(user_id)
    if not user:
        return abort(401, description="User does not exist in database")
    reservation_fields = reservation_schema.load(request.json)
    reservation = Reservation(
        start=reservation_fields["start"],
        length=reservation_fields["length"],
        book=book,
        user=user
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify(reservation_schema.dump(reservation))


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
        author_id=book_fields['author_id']
    )
    db.session.add(new_book)
    db.session.commit()

    return jsonify(book_schema.dump(new_book))


@books.route("/<int:id>", methods=["PUT"])
@jwt_required()
@librarian_only
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

    return jsonify(book_schema.dump(book))
