from app import app, USERS, POSTS, models
from flask import request, Response
import json
from http import HTTPStatus


@app.route("/")
def index():
    return "<h1>Hello world!</h1>"


@app.post("/users/create")
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(user_id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "user_id": user.id,
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


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if models.User.is_valid_user_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "user_id": user.id,
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


@app.post("/posts/create")
def post_create():
    data = request.get_json()
    post_id = len(POSTS)
    author_id = data.get("author_id")
    text = data.get("text")
    post = models.Posts(post_id, author_id, text)
    if models.Posts.is_valid_author_id(author_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    POSTS.append(post)
    USERS[author_id].posts.append(post_id)
    response = Response(
        json.dumps(
            {
                "post_id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if models.Posts.is_valid_post_id(post_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "post_id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/posts/<int:post_id>/reaction")
def put_reaction(post_id):
    if models.Posts.is_valid_post_id(post_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    user_id = data.get("user_id")
    reaction = data.get("reaction")
    author_id = POSTS[post_id].author_id
    if user_id != author_id:
        return Response(status=HTTPStatus.FORBIDDEN)
    POSTS[post_id].reactions.append(reaction)
    USERS[user_id].total_reactions += 1
    return Response(status=HTTPStatus.OK)
