from random import randint
from datetime import timedelta
from flask import request, jsonify, make_response, redirect, json
from flask_jwt_extended import (create_access_token, jwt_required)
from flask_restful import Resource
from flask_security.utils import verify_and_update_password, login_user
from flask_security import current_user
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from src import BaseView, limiter, db, redis_store, sms
from src import api
from src.user.schemas import UserSchema
from src.utils.api import set_user
from src.utils.methods import List, Fetch, Create, Update
from .models import User, UserToUser
from .resources import UserResource


@api.register()
class UserView(BaseView):
    api_methods = [List, Fetch, Create, Update]

    @classmethod
    def get_resource(cls):
        return UserResource


class UserLoginResource(Resource):
    model = User

    decorators = [limiter.limit("300/day;30/hour;5/minute;2/second")]

    def post(self):

        if request.json:
            data = request.json
            print(data)
            user = self.model.query.filter(self.model.email == data['email']).first()
            print(user)
            if user and verify_and_update_password(data['password'], user) and login_user(user):
                expires = timedelta(days=365)
                return make_response(
                    jsonify({'id': user.id,
                             'user': UserSchema(only=('id', 'email', 'first_name', 'last_name')).dump(user).data,
                             'authentication_token': create_access_token(identity=user.id, expires_delta=expires)}), 200)
            else:
                return make_response(jsonify({'meta': {'code': 403}}), 403)

        else:
            data = request.form
            user = self.model.query.filter(self.model.email == data['email']).first()
            if user and verify_and_update_password(data['password'], user) and login_user(user):
                return make_response(redirect('/admin/', 302))
            else:
                return make_response(redirect('/api/v1/login', 403))


class UserRegisterResource(Resource):
    model = User
    schema = UserSchema

    def post(self):
        data = request.json
        user = User.query.filter(User.email == data['email']).first()
        if user:
            return make_response(jsonify({}), 400)
        user, errors = self.schema().load(data)
        if errors:
            return make_response(jsonify(errors), 400)

        try:
             db.session.add(user)
             db.session.commit()

        except (IntegrityError, InvalidRequestError) as e:
            print(e)
            db.session.rollback()
            return make_response(jsonify(str(e)), 400)

        return make_response(jsonify({}), 200)

    def get(self):
        return "Works"

api.add_resource(UserLoginResource, '/login/', endpoint='login')
api.add_resource(UserRegisterResource, '/register/', endpoint='register')
