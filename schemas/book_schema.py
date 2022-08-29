from main import ma
from marshmallow import fields


class BookSchema(ma.Schema):
    class Meta:
        ordered = True
        # fields to expose
        fields = ("id", "title", "genre", "length", "year", "author")
    author = fields.Nested("AuthorSchema")


# single book schema
book_schema = BookSchema()

# multiple books schema
books_schema = BookSchema(many=True)
