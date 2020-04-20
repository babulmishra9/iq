from . import users
import json

subjects = json.load(open('./data/subjects.json', 'w'))

ranks = json.load(open('./data/ranks.json', 'w'))

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


def sbj_code(sbj):
    return f"""from .context import subjects
from .context import users
from .context import files
from discord.ext import commands
import discord


class {sbj.title()}(commands.Cog):       
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('{sbj.title()} online.')

    @commands.command()
    async def {sbj.lower()}(self, ctx):
        \"\"\"A {sbj.lower()} question.\"\"\"

        if not users.is_user(ctx.author.id):
            await ctx.send('You are not signed up for any subject. :x:')

        elif users.users[str(ctx.author.id)]['subject'] != '{sbj.lower()}':
            await ctx.send('You are not joined {sbj.lower()}. :x:')

        else:
            id_ = str(ctx.author.id)

            user = users.users[id_]

            quest_answer = subjects.get_quest_answer(id_)

            user['quest'] = quest_answer[0]
            user['answer'] = quest_answer[1]

            files.update_users()

            await ctx.send(user['quest'])


def setup(client):
    client.add_cog({sbj.title()}(client))"""
