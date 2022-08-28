from main import db


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    country = db.Column(db.String())
    dob = db.Column(db.Date())
    books = db.relationship("Book", backref='author', cascade="all, delete")
