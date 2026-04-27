from peewee import SqliteDatabase, Model, CharField, BooleanField, DateTimeField
from datetime import datetime
import os

db = SqliteDatabase(None)


class Todo(Model):
    title = CharField()
    done = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db


def init_db(data_dir="."):
    db.init(os.path.join(data_dir, "todos.db"))
    db.connect()
    db.create_tables([Todo], safe=True)


def get_all_todos():
    return list(Todo.select().order_by(Todo.done, Todo.created_at))


def add_todo(title):
    return Todo.create(title=title.strip())


def toggle_todo(todo_id):
    todo = Todo.get_by_id(todo_id)
    todo.done = not todo.done
    todo.save()
    return todo


def delete_todo(todo_id):
    Todo.get_by_id(todo_id).delete_instance()


def clear_done():
    Todo.delete().where(Todo.done == True).execute()
