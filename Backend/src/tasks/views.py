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
        data = request.args
        if data and current_user.is_authenticated:
            if data['task_name']:
                self.schema.task_name = data["task_name"]
                owner = get_user(user_id = current_user.id)
                if owner == None:
                    return make_response(jsonify({"error" : "Owner with the given ID does not exist."}))
                
                try:
                    create_task(db = db, task_name = data['task_name'], owner = owner)
                except Exception as e:
                    return make_response(jsonify({"error" : str(e)}))
                
                return make_response(jsonify({"status" : "success"}))

            else:
                return jsonify({'error' : 'No task_name provided.'})
        
        elif not current_user.is_authenticated:
            return make_response(jsonify({'error' : 'User not authenticated'}))

        else:
            return make_response(jsonify({'error' : 'Parameter \'task_name\' absent.'}))
    
    def get(self):
        return "Please send a POST request."

class TaskDeleteResource(Resource):
    model = Tasks
    schema = TaskSchema

    def delete(self):
        data = request.args
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
                
            return make_response(jsonify({"error" : "No task exists with that ID that is owned by you."}))

        return make_response(jsonify({"error" : "Right parameters weren't passed in."}))

    def get(self):
        return "send a DELETE request instead."

class TaskListResource(Resource):
    model = Tasks
    schema = TaskSchema

    def get(self):
        if current_user.is_authenticated:
            tasks = get_tasks(owner_id = current_user.id)
            data = {}
            count = 0
            for task in tasks:
                data[count] = {"task_name" : task.task_name,
                            "task_id" : task.id}
                count =+ 1

            return data


api.add_resource(TaskCreateResource, '/taskcreate/', endpoint = 'taskcreate')
api.add_resource(TaskDeleteResource, '/taskdelete/', endpoint = 'taskdelete')
api.add_resource(TaskListResource, '/tasklist/', endpoint = 'tasklist')
