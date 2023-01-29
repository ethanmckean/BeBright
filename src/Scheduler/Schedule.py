from flask import Flask, request, jsonify
from Database.database import (
    get_database_questions,
    add_to_database,
    remove_database_questions,
)
from Interfaces.question import Question
from twilio.rest import Client
from typing import List

app = Flask(__name__)

# Download the helper library from https://www.twilio.com/docs/python/install

# Your Account Sid and Auth Token from twilio.com/console
twilio_account_sid = "ACf035803b5397b0314e38ff0ec61760b2"
twilio_auth_token = "52a9c08cc9a488a76dd78640b7506a9c"
twilio_number = "[+][1][8446830525]"

client = Client(twilio_account_sid, twilio_auth_token)


@app.get("/tasks")
def get_scheduled_tasks():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    data = request.get_json()
    group = data["group"]
    questions = get_database_questions(group)

    if len(questions) == 0:
        return None

    number = int(data["number"])

    remove_database_questions(group, question=questions[0][0].get_ans())

    text = client.messages.create(
        body="You have a new BeBright question avaliable",
        from_=f"[+][1][{number}]",
        to=f"[+][1][{number}]",
    )

    print(text.sid)

    return questions[0][0].get_dict()


@app.post("/tasks")
def schedule_task():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    data = request.get_json()
    question = Question(data["qs"], data["choices"], data["ans"])
    group = data["group"]
    post_time = data["post_time"]

    add_to_database(question, group, post_time)
