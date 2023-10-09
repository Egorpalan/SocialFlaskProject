from flask import Flask

app = Flask(__name__)

USERS = []  # list for objects User
POSTS = []  # list for objects Posts

from app import views
from app import models
