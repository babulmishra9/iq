from . import users
import random

random = random.SystemRandom()

subjects = ['math', 'astronomy']

ranks = {
    'math': ['math', 'math level 1', 'math level 2']
}

MAX_POINTS = 8


def get_quest_answer(id_, dict):
    """Returns the question and the answer in a list."""

    points = users.users[id_]['points']
    
    questions = list(dict.keys())

    question = questions[points]
    answer = dict[question]
    
    return [question, answer]


def level_up(id_, ranks):
    major_points = users.users[id_]['major-points']

    major_points += 1

    users.users[id_]['subject'] = ranks[major_points]


def get_ranks(id_=None, user_subject=None):
    if user_subject:
        for subject in ranks.keys():
            if user_subject == subject:
                return ranks[subject]

    user = users.users[id_]

    for subject in ranks.keys():
        if user['subject'] == subject:
            return ranks[subject]
