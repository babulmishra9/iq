from . import subjects
from . import users
import json
import os


def update_data():
    with open('data/ranks.json', 'w') as f:
        json.dump(subjects.ranks, f, sort_keys=True, indent=4)

    with open('data/subjects.json', 'w') as f:
        json.dump(subjects.subjects, f, sort_keys=True, indent=4)


def new_subject_file(name, data):
    with open(f'subjects/{name}.py', 'w') as f:
        f.write(data)


def load_subjects(client, load_all=False, load=None):
    if load_all:
        for filename in os.listdir('./subjects'):
            if filename.endswith('.py'):
                if filename == '__init__.py' or filename == 'context.py':
                    pass

                else:
                    client.load_extension(f'subjects.{filename[:-3]}')
            
    elif load:
        client.load_extension(f'subjects.{load}')


def update_users():
    with open('data/users.json', 'w') as f:
        json.dump(users.users, f, indent=4)
