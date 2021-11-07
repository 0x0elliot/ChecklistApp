from flask_security import current_user
from sqlalchemy import and_, or_


from src.utils import ModelResource, operators as ops
from .schemas import User, UserSchema


class UserResource(ModelResource):

    model = User
    schema = UserSchema

    auth_required = True

    roles_accepted = ('admin', 'owner', 'staff')

    optional = ('stores', 'current_login_at', 'current_login_ip', 'created_on', 'fixed_dues', 'subscriptions',
                'last_login_at', 'last_login_ip', 'login_count', 'confirmed_at', 'permissions', 'retail_brand')

    exclude = ('password', 'roles', 'active')

    filters = {
        'username': [ops.Equal, ops.Contains],
        'name': [ops.Equal, ops.Contains],
        'active': [ops.Boolean],
        'id': [ops.Equal],
        'first_name': [ops.Equal, ops.StartsWith],

    }

    related_resource = {

    }

    order_by = ['email', 'id', 'name']

    only = ()