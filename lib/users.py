users = {}


def is_user(id_):
    """Checks if a user is new or old."""

    return id_ in users.keys()


def new_user(id_, name=None, subject=None):
    users[id_] = {
        'username': name,
        'subject': subject,
    }
