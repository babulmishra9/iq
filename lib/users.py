users = {}


def is_user(id_):
    """Checks if a user is new or old."""

    return id_ in users.keys()


def new_user(id_, name, subject, subject_ranks):
    users[id_] = {
        'username': name,
        'subject': subject,
        'subject-ranks': subject_ranks,
        'points': 0,
        'major-points': 0,
        'quest': None,
        'answer': None,
    }
