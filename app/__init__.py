from flask import Flask

app = Flask(__name__)

USERS = []  # list for objects User

from app import views
from app import models
