from main import ma
from marshmallow.validate import Length


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email", "password")
        load_only = ("password",)

    # validate password
    password = ma.String(validate=Length(min=8))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
