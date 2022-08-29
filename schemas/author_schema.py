from main import ma
from marshmallow import fields


class AuthorSchema(ma.Schema):

    class Meta:
        ordered = True
        fields = ("id", "name", "country", "dob")


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
