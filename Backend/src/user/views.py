import os
from random import randint
from datetime import timedelta
from flask import request, jsonify, make_response, redirect, json
from flask_jwt_extended import (create_access_token, jwt_required)
from flask_restful import Resource
from flask_security.utils import verify_and_update_password, login_user, logout_user
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

    decorators = [limiter.limit("300/day;500/hour;50/minute;20/second")]

    def post(self):

        data = request.json
        #debug = Debug(os.environ.get("DEBUG_WEBHOOK"))
        #debug.print_webhook(request.json.get("email"))

        if data.get('email') and data.get('password'):
            user = self.model.query.filter(self.model.email == data.get('email')).first()

            password = data.get('password')
            
            if user and crud.verify_password(user, password) and login_user(user):
                expires = timedelta(days=365)
                session_cookie = create_access_token(identity=user.id, expires_delta=expires)
                resp = make_response(
                    jsonify({'id': user.id,
                             'user': UserSchema(only=('id', 'email', 'name')).dump(user).data,
                             'authentication_token': session_cookie}), 200)
                
                #resp.set_cookie("session", session_cookie)
                return resp
            else:
                return make_response(jsonify({'meta': {'code': 403}}), 403)

        else:
            data = request.form
            user = self.model.query.filter(self.model.email == data['email']).first()
            if user and verify_and_update_password(data['password'], user) and login_user(user):
                return make_response(redirect('/admin/', 302))
            else:
                return make_response(redirect('/api/v1/login', 403))
    
    def options(self):
        resp = make_response()
        resp.headers['Allow'] = "OPTIONS, GET, POST"
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'

        return resp

    def get(self):
        return "send a POST request instead."

class UserRegisterResource(Resource):
    model = User
    schema = UserSchema

    def post(self):
        data = request.json

        try:
            user = User.query.filter(User.email == data.get('email')).first()
        except Exception as e:
            return make_response(jsonify({"error" : str(e), "data" : data}))

        #debug = Debug(os.environ.get('DEBUG_WEBHOOK'))
        #debug.print_webhook(crud.email_password_unique(email = data.get('email'), password = data.get('password')))

        if user or not crud.email_password_unique(email = data.get('email'), password = data.get('password')):
            return make_response(jsonify({'meta': {'code': 403}}), 403)
        
        new_data = { "email" : data.get('email'), "name" : data.get('name'),"password" : data.get('password')}
        print(new_data)
        user, errors = self.schema().load(new_data)
        if errors:
            return make_response(jsonify(errors), 403)

        try:
            crud.create_user(db, user)
        except Exception as e:
            return make_response(jsonify({"error" : str(e)}), 403)

        return make_response(jsonify({""}), 200)

    def options(self):
        resp = make_response()
        resp.headers['Allow'] = "OPTIONS, GET, POST"
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
        return resp

    def get(self):
        return "Send a POST request instead."

class UserLogoutResource(Resource):
    model = User

    def post(self):
        if current_user.is_authenticated:
            logout_user()
        else:
            return make_response(jsonify({}), 403)

    def options(self):
        resp = make_response()
        resp.headers['Allow'] = "OPTIONS, POST"
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'

        return resp

api.add_resource(UserLoginResource, '/login/', endpoint='login')
api.add_resource(UserRegisterResource, '/register/', endpoint='register')
api.add_resource(UserLogoutResource, '/logout/', endpoint = 'logout')
