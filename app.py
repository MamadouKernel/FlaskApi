# from typing import List
from flask import Flask, request, render_template, jsonify
from flask_expects_json import expects_json
from json_saver import JsonSaver
from datetime import datetime
import uuid

app = Flask(__name__, static_folder='assets')
data_helper=JsonSaver("data.json")
todo_schema = {
    "type":"object",
    "properties":{
        "title": {"type":"string"},
        "description": {"type":"string"},
        "status":{"type":"integer"},
        "due":{"type":"string"}
    },
    "required": ["title", "description", "status", "due"]
}

@app.route("/")
def home():
    message = "todoapp"
    return render_template('home.html', message=message)

@app.route("/todos", methods=["POST"])
@expects_json(todo_schema)
def create_todos():
    datas = request.get_json()
    datas["id"] = str(uuid.uuid4())
    responses = data_helper.add(datas["id"], datas)
    return jsonify(responses)

@app.route("/todos")
def get_todos():
    todos = data_helper.find_all()
    print(len(todos))
    return render_template('todos.html', todos=todos, datetime=datetime)

@app.route("/todos", methods=["PUT"])
def modifier_todos():
        todo = request.get_json()
        id = todo["id"]
        # del todo["id"]
        result = data_helper.update(id, todo)
        return jsonify(result)


@app.route("/todos", methods=["DELETE"])
def delete_todos():
    todo = request.get_json()
    id = todo["id"]
    result = data_helper.delete(id)
    return jsonify(result)
    
        



if __name__ == "__main__":
    app.run(debug=True)
