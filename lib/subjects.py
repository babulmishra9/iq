from . import users
import json

subjects = ['math', 'astronomy', 'biology', 'chemistry', 'geograpy', 'physics', 'tech']

ranks = json.load(open('./data/ranks.json'))

MAX_POINTS = 8


def get_quest_answer(id_):
    """Returns the question and the answer in a list."""

    user = users.users[id_]
    subject = user['subject']

    # The dictionary containing all the questions and their answers.
    quest_answers = ranks[subject][user['subject-level']]['questions']
    
    questions = list(quest_answers.keys())

    question = questions[user['points']]
    answer = quest_answers[question]
    
    return [question, answer]


def level_up(id_):
    user = users.users[id_]
    subject = user['subject']

    major_points = user['major-points']
    major_points += 1

    user['points'] = 0

    user['subject-level'] = ranks[subject][subject + '_ranks'][major_points]


def get_ranks(id_=None, user_subject=None, level=None):
    if user_subject:
        for subject in ranks.keys():
            if user_subject == subject:
                return ranks[subject][subject + '_ranks']

    if id_:
        user = users.users[id_]

        for subject in ranks.keys():
            if user['subject'] == subject:
                return ranks[subject][subject + '_ranks']
