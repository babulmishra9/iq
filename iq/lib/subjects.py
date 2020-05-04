from . import custom_subjects
from . import users


def level_up(id_):
    user = users.users[id_]
    subject = user['subject']

    major_points = user['major-points']
    major_points += 1

    user['points'] = 0

    user['subject-level'] = custom_subjects.quests[subject][subject + '_ranks'][major_points]


def get_ranks(id_=None, user_subject=None, level=None):
    if user_subject:
        for subject in custom_subjects.quests.keys():
            if user_subject == subject:
                return custom_subjects.quests[subject][subject + '_ranks']

    if id_:
        user = users.users[id_]

        for subject in custom_subjects.quests.keys():
            if user['subject'] == subject:
                return custom_subjects.quests[subject][subject + '_ranks']


