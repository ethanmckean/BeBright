from flask import Flask, request, jsonify
from Database.database import (
    get_database_questions,
    add_to_database,
    remove_database_questions,
)
from Interfaces.question import Question
from typing import List

app = Flask(__name__)


@app.get("/tasks")
def get_scheduled_tasks():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    group = request.get_json()["group"]
    questions = get_database_questions(group)

    remove_database_questions(group, question=questions[0][0].get_ans())


@app.post("/tasks")
def schedule_task():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    data = request.get_json()
    question = Question(data["qs"], data["choices"], data["ans"])
    group = data["group"]
    post_time = data["post_time"]

    add_to_database(question, group, post_time)
