from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/api/todos', methods=['GET', 'POST'])
def get_or_create_todo_items():
    if request.method == 'GET':
        return [i.as_dict() for i in TodoItem.query.all()]
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return {'error': 'No data provided'}, 400
        if not data.get('title'):
            return {'error': 'No title provided'}, 400
        if not data.get('description'):
            return {'error': 'No description provided'}, 400

        data = {k: v for k, v in data.items() if k in TodoItem.__table__.columns.keys()}
        todo_item = TodoItem(title=data['title'], description=data['description'], done=data.get('done', False))
        db.session.add(todo_item)
        db.session.commit()
        return todo_item.as_dict()


@app.route('/api/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_todo_item(todo_id: int):
    todo = db.session.get(TodoItem, todo_id)
    if todo is None:
        return {'error': 'Todo item not found'}, 404
    if request.method == 'GET':
        return todo.as_dict()
    elif request.method == 'PUT':
        data = request.get_json()
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        todo.done = data.get('done', todo.done)
        db.session.commit()
        return todo.as_dict()
    elif request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
