import os
from random import randint
from datetime import timedelta
from flask import request, jsonify, make_response, redirect, json
from flask_jwt_extended import (create_access_token, jwt_required)
from flask_restful import Resource
from flask_security.utils import verify_and_update_password, login_user
from flask_security import current_user
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from src.utils.debug import Debug

from src import BaseView, limiter, db, redis_store, sms
from src import api
from src.user.schemas import UserSchema
from src.utils.api import set_user
from src.utils.methods import List, Fetch, Create, Update
from .models import User
from .resources import UserResource

from src.utils import crud

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

        data = request.args
        print(data)

        if data['email']:
            data = request.args
            user = self.model.query.filter(self.model.email == data['email']).first()

            password = data['password']
            #debug = Debug(os.environ.get("DEBUG_WEBHOOK"))
            #debug.print_webhook(crud.verify_password(user, password))
            
            if user and crud.verify_password(user, password) and login_user(user):
                expires = timedelta(days=365)
                return make_response(
                    jsonify({'id': user.id,
                             'user': UserSchema(only=('id', 'email', 'name')).dump(user).data,
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
    
    def get(self):
        return "send a POST request instead."

class UserRegisterResource(Resource):
    model = User
    schema = UserSchema

    def post(self):
        data = request.args

        try:
            user = User.query.filter(User.email == data['email']).first()
        except Exception as e:
            return make_response(jsonify({"error" : str(e), "data" : data}))

        if user:
            return make_response(jsonify({}), 400)
        
        new_data = { "email" : data['email'], "name" : data['name'],"password" : data['password']}
        print(new_data)
        user, errors = self.schema().load(new_data)
        if errors:
            return make_response(jsonify(errors), 400)

        try:
            crud.create_user(db, user)
        except Exception as e:
            return make_response(jsonify({"error" : str(e)}), 400)

        return make_response(jsonify({""}), 200)

    def get(self):
        return "Send a POST request instead."

api.add_resource(UserLoginResource, '/login/', endpoint='login')
api.add_resource(UserRegisterResource, '/register/', endpoint='register')
