from main import ma
from marshmallow import fields


class AuthorSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "country", "dob", "books")

    books = fields.List(fields.Nested("BookSchema", exclude=("author",)))


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
