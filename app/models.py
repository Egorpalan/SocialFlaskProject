import re


class User:
    def __init__(self, id, first_name, last_name, email, total_reactions, posts=[]):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = posts

    @staticmethod
    def is_valid_email(email):
        patterns = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if re.match(patterns, email):
            return True
        else:
            return False
