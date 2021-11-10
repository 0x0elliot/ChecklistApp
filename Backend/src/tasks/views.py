from flask import json
from src.utils.crud import delete_task, get_task, get_tasks, get_user
from src import db
from src.utils.crud import create_task

from src.tasks.schemas import TaskSchema
from .resources import TaskResource

from flask.json import jsonify
from src import api, BaseView
from src.user.models import Tasks
from src.utils.methods import List, Fetch, Create, Update, Delete

import os
from flask_security import current_user
from flask_restful import Resource
from flask import request, make_response
from src.utils.debug import Debug

@api.register()
class TaskView(BaseView):
    api_methods = [List, Fetch, Create, Update, Delete]

    @classmethod
    def get_resource(cls):
        return TaskResource


class TaskCreateResource(Resource):
    model = Tasks
    schema = TaskSchema

    def post(self):
        data = request.json
        if data and current_user.is_authenticated:
            if data.get('task_name'):
                self.schema.task_name = data.get('task_name')
                owner = get_user(user_id = current_user.id)
                if owner == None:
                    return make_response(jsonify({"error" : "Owner with the given ID does not exist."}))
                
                try:
                    create_task(db = db, task_name = data.get('task_name'), owner = owner)
                except Exception as e:
                    return make_response(jsonify({"error" : str(e)}))
                
                return make_response(jsonify({"status" : "success"}))

            else:
                return make_response(jsonify({'error' : 'No task_name provided.'}), 403)
        
        elif not current_user.is_authenticated:
            return make_response(jsonify({'error' : 'User not authenticated'}), 403)

        else:
            return make_response(jsonify({'error' : 'Parameter \'task_name\' absent.'}))
    
    def get(self):
        return "Please send a POST request."

    def options(self):
        resp = make_response()
        resp.headers['Allow'] = "OPTIONS, GET, POST"
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
        return resp

class TaskDeleteResource(Resource):
    model = Tasks
    schema = TaskSchema

    def post(self):
        data = request.json
        if data['task_id'] and current_user.is_authenticated():
            task_id = data['task_id']
            owner_id = current_user.id
            if get_task(task_id, owner_id = owner_id):
                try:
                    response = delete_task(db, task_id)
                    if response:
                        return make_response(jsonify({"status" : "OK"}))
                except Exception as e:
                    return make_response(jsonify({"error" : str(e)}))
                
            return make_response(jsonify({"error" : "No task exists with that ID that is owned by you."}), 403)

        return make_response(jsonify({"error" : "Right parameters weren't passed in."}))

    def get(self):
        return "send a DELETE request instead."

    def options(self):
        resp = make_response()
        resp.headers['Allow'] = "OPTIONS, GET, POST"
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
        return resp

class TaskListResource(Resource):
    model = Tasks
    schema = TaskSchema

    def get(self):
        if current_user.is_authenticated:
            try:
                tasks = get_tasks(owner_id = current_user.id)
            except Exception as e:
                print(e)
            data = []
            count = 1
            for task in tasks:
                new = {"count" : count,
                        "task_name" : task.task_name,
                        "task_id" : task.id}
                data.append(new)
                count += 1
            return make_response(jsonify(data), 200)
        else:
            return make_response(jsonify({"error" : "User not authenticated."}), 403)
            


api.add_resource(TaskCreateResource, '/taskcreate/', endpoint = 'taskcreate')
api.add_resource(TaskDeleteResource, '/taskdelete/', endpoint = 'taskdelete')
api.add_resource(TaskListResource, '/tasklist/', endpoint = 'tasklist')
