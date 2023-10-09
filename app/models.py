import re
from app import USERS,POSTS


class User:
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = 0
        self.posts = []

    @staticmethod
    def is_valid_email(email):
        patterns = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if re.match(patterns, email):
            return True
        else:
            return False

    @staticmethod
    def is_valid_user_id(user_id):
        if user_id < 0 or user_id >= len(USERS):
            return True
        return False


class Posts:
    def __init__(self, id, author_id, text):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.reactions = []

    @staticmethod
    def is_valid_author_id(author_id):
        if author_id < 0 or author_id >= len(USERS):
            return True
        return False

    @staticmethod
    def is_valid_post_id(post_id):
        if post_id < 0 or post_id >= len(POSTS):
            return True
        return False