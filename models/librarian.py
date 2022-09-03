from main import db


class Librarian(db.Model):
    __tablename__ = "librarians"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    shift = db.Column(db.String(), default="Weekdays")
    rate = db.Column(db.Float(), default=30.0)

