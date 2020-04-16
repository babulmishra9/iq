from . import files
import json

users = json.load(open('data/users.json'))

def is_user(id_):
    """Checks if a user is new or old."""

    return str(id_) in users.keys()


def new_user(id_, name, subject, subject_ranks):
    if is_user(id_):
        del users[id_]

    users[id_] = {
        'username': name,
        'subject': subject,
        'subject-level': subject,
        'subject-ranks': subject_ranks,
        'points': 0,
        'major-points': 0,
        'quest': None,
        'answer': None,
    }

    files.update_users()
