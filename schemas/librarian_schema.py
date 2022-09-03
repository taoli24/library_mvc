from main import ma
from marshmallow.validate import Length


class LibrarianSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'name', 'shift', 'rate')
        load_only = ('password',)

    password = ma.String(validate=Length(min=8))


librarian_schema = LibrarianSchema()
librarians_schema = LibrarianSchema(many=True)
