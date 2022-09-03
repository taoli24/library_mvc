from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, abort, jsonify
from models import User, Librarian
from main import bcrypt, db
from schemas import user_schema, librarian_schema
from datetime import timedelta
from flask_jwt_extended import create_access_token

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def auth_login():
    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(username=user_fields["username"]).first()

    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username or password.")

    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({"username": user.username, "access_token": access_token})


# register new users
@auth.route("/register", methods=["POST"])
def auth_register():
    user_fields = user_schema.load(request.json)

    user = User(
        username=user_fields["username"],
        email=user_fields["email"],
        password=bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return abort(400, description="User already exist in database.")

    expire = timedelta(days=1)
    access_token = create_access_token(identity=user.id, expires_delta=expire)

    return jsonify({"username": user.username, "access_token": access_token})


@auth.route("/librarian/login", methods=["POST"])
def lib_login():
    lib_fields = librarian_schema.load(request.json)
    lib = Librarian.query.filter_by(username=lib_fields["username"]).first()

    if not lib or not bcrypt.check_password_hash(lib.password, lib_fields["password"]):
        return abort(401, description="Incorrect username or password.")

    expiry = timedelta(days=1)
    access_token = create_access_token(identity=f"librarian{lib.id}", expires_delta=expiry)

    return jsonify({"username": lib.username, "access_token": access_token})
