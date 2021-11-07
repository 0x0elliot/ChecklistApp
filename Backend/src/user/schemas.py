from src import ma, BaseSchema
from .models import User


class UserSchema(BaseSchema):
    class Meta:
        model = User
        exclude = ('updated_on',)

    id = ma.Integer(dump_only=True)
    email = ma.Email(required=False)
    name = ma.String(load=True)
    password = ma.String(load = True)