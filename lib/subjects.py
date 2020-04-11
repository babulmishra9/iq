import random

random = random.SystemRandom()

subjects = ['math', 'astronomy']


def get_quest_answer(dict):
    """Returns the question and the answer in a list."""

    question = random.choice(list(dict.keys()))

    answer = dict[question]

    return [question, answer]
