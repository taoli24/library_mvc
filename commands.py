from main import db, bcrypt
from flask import Blueprint
from models import Author, Book, User
from datetime import date

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command("seed")
def seed_db():
    author1 = Author(
        name="Tessa Tao",
        country="Australia",
        dob=date(2013, 3, 12)
    )

    author2 = Author(
        name="Kayla Tao",
        country="Australia",
        dob=date(2015, 2, 10)
    )

    db.session.add(author1)
    db.session.add(author2)
    db.session.commit()

    book1 = Book(
        title="The sugar plum fairy",
        genre="Children",
        year="2022",
        length=4,
        author_id=1
    )

    db.session.add(book1)
    db.session.commit()

    user1 = User(
        username="user1",
        email="user1@email.com",
        password=bcrypt.generate_password_hash("12345678").decode("utf-8")
    )

    db.session.add(user1)
    db.session.commit()

    print("Tables seeded")
