from . import users
import random

random = random.SystemRandom()

subjects = ['math', 'astronomy']


def get_quest_answer(dict):
    """Returns the question and the answer in a list."""

    question = random.choice(list(dict.keys()))
    answer = dict[question]

    return [question, answer]


def level_up(id_, ranks):
    major_points = users.users[id_]['major-points']

    major_points += 1

    users.users[id_]['subject'] = ranks[major_points]
