from app import app, USERS, POSTS, models
from flask import request, Response, url_for
import json
from http import HTTPStatus
import matplotlib.pyplot as plt


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


@app.get("/users/<int:user_id>/posts")
def get_all_post(user_id):
    if models.User.is_valid_user_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    sort = data.get("sort")
    if sort != "asc" and sort != "desc":
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = USERS[user_id]
    user_posts = [POSTS[post_id] for post_id in user.posts]
    if sort == "asc":
        user_posts.sort(key=lambda post: len(post.reactions), reverse=False)
    if sort == "desc":
        user_posts.sort(key=lambda post: len(post.reactions), reverse=True)
    response = Response(
        json.dumps(
            {
                "posts": [
                    {
                        "id": post.id,
                        "author_id": post.author_id,
                        "text": post.text,
                        "reactions": post.reactions,
                    }
                    for post in user_posts
                ]
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def get_all_users():
    data = request.get_json()
    type = data.get("type")
    sort = data.get("sort")
    if (sort != "asc" and sort != "desc") and sort != None:
        return Response(status=HTTPStatus.BAD_REQUEST)
    if type != "list" and type != "graph":
        return Response(status=HTTPStatus.BAD_REQUEST)
    if sort == "asc":
        USERS.sort(key=lambda user: user.total_reactions, reverse=False)
    if sort == "desc":
        USERS.sort(key=lambda user: user.total_reactions, reverse=True)
    if type == "list":
        response = Response(
            json.dumps(
                {
                    "users": [
                        {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "total_reactions": user.total_reactions,
                        }
                        for user in USERS
                    ]
                }
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    if type == "graph":
        fig, ax = plt.subplots()
        users = [user for user in USERS]
        user_names = [f"{user.first_name} {user.last_name} {user.id}" for user in users]
        user_reactions = [user.total_reactions for user in users]
        ax.bar(user_names, user_reactions)
        ax.set_ylabel("User reactions")
        ax.set_title("User leaderboard by Reaction")
        plt.savefig("app/static/users_leaderboard.png")
        response = Response(
            f'<img src= "{url_for("static",filename="users_leaderboard.png")}">',
            HTTPStatus.OK,
            mimetype="text/html",
        )
        return response
