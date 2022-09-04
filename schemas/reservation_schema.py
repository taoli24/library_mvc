from main import ma
from marshmallow import fields


class ReservationSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "start", "length", "user_id", "book_id", "user", "book")
        load_only = ("user_id", "book_id")

    user = fields.Nested("UserSchema", only=("username", "email"))
    book = fields.Nested("BookSchema")


reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)
