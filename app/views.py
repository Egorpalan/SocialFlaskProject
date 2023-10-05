from app import app, USERS, models
from flask import request, Response
import json
from http import HTTPStatus


@app.route("/")
def index():
    return "<h1>Hello world!</h1>"


@app.post("/users/create")
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    total_reactions = data.get("total_reactions")
    # todo: validate email
    user = models.User(id, first_name, last_name, email, total_reactions)
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
