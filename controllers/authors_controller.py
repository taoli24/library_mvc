from flask import Blueprint, request, jsonify, abort
from main import db
from models import Author
from schemas import author_schema, authors_schema
from datetime import date
from flask_jwt_extended import jwt_required

authors = Blueprint("authors", __name__, url_prefix="/authors")


@authors.route("/", methods=["GET"])
def get_authors():
    author_list = Author.query.all()
    return jsonify(authors_schema.dump(author_list))


@authors.route("/<int:id>", methods=["GET"])
def get_author(id):
    author = Author.query.get(id)
    if not author:
        return abort(400, description="Author does not exist in database.")

    return jsonify(author_schema.dump(author))


# post new authors
@authors.route("/", methods=["POST"])
@jwt_required()
def new_author():
    author_fields = author_schema.load(request.json)
    author = Author(
        name=author_fields["name"],
        country=author_fields["country"],
        dob=date.fromisoformat(author_fields["dob"])
    )

    db.session.add(author)
    db.session.commit()

    return jsonify(author_schema.dump(author))


# delete an author
@authors.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def del_author(id):
    author = Author.query.get(id)
    if not author:
        return abort(400, description="Author is not the database")

    db.session.delete(author)
    db.session.commit()

    return jsonify(author_schema.dump(author))


# update an author
@authors.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_author(id):
    author = Author.query.get(id)
    if not author:
        return abort(400, description="Author is not the database")

    author_field = author_schema.load(request.json)
    author.name = author_field.get("name", author.name)
    author.country = author_field.get("country", author.country)
    author.dob = author_field.get("dob", author.dob)

    db.session.commit()

    return jsonify(author_schema.dump(author))

