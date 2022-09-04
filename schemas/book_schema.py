from main import ma
from marshmallow import fields


class BookSchema(ma.Schema):
    class Meta:
        ordered = True
        # fields to expose
        fields = ("id", "title", "genre", "length", "year", "author_id", "author")
        load_only = ("author_id",)

    author = fields.Nested("AuthorSchema", only=("name", "country"))


# single book schema
book_schema = BookSchema()

# multiple books schema
books_schema = BookSchema(many=True)
