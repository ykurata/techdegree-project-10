from flask import jsonify, Blueprint

from flask.ext.restful import (Resource, Api, reqparse, fields,
                                marshal, marshal_with, abort, url_for)

from auth import auth
import models


todo_fields = {
    'id': fields.Integer,
    'task': fields.String
}


def todo_or_404(todo_id):
    try:
        todo = models.Todo.get(models.Todo.id==todo_id)
    except models.Todo.DoesNotExist:
        abort(404, message="Todo {} does not exist".format(todo_id))
    else:
        return todo


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'task',
            required = True,
            help = 'No task provided',
            location = ['form', 'json']
        )
        super().__init__()

    def get(self):
        todos = [marshal(todo, todo_fields)
                for todo in models.Todo.select()]
        return {'todos': todos}


    @marshal_with(todo_fields)
    @auth.login_required
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return todo, 201, {
                'Location':url_for('resources.todos.todo', id=todo.id)
                }


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'task',
            required = True,
            help = 'No task provided',
            location = ['form', 'json']
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        return todo_or_404(id)

    @marshal_with(todo_fields)
    @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id==id)
        query.execute()
        return (models.Todo.get(models.Todo.id==id), 200,
                {'Location': url_for('resources.todos.todo', id=id)})

    @auth.login_required
    def delete(self, id):
        query = models.Todo.delete().where(models.Todo.id==id)
        query.execute()
        return ('', 204, {'Location': url_for('resources.todos.todos')})


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint = 'todos'
)
api.add_resource(
    Todo,
    '/api/v1/todos/<int:id>',
    endpoint = 'todo'
)
