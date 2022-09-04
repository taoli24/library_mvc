from main import db


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String())
    year = db.Column(db.Integer)
    length = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    reservations = db.relationship("Reservation", backref="book", cascade="all, delete")
