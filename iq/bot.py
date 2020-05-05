from lib import custom_subjects
from lib import subjects
from lib import users
from discord.ext import commands
import discord
import json

TOKEN = json.load(open('token.json'))

client = commands.Bot(command_prefix='iq ')


@client.event
async def on_ready():
    print('Bot is online.')


@commands.has_role('iq.admin')
@client.command()
async def load(ctx, extension):
    client.load_extension(f'subjects.{extension}')


@commands.has_role('iq.admin')
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'subjects.{extension}')


@client.command()
async def join(ctx, subject):
    """Joins a subject."""

    author_id = str(ctx.author.id)
    author_name = ctx.author.name

    subject = subject.lower()

    if subject in custom_subjects.subjects:

        if users.is_user(author_id):
            user = users.users[author_id]

            old_subject = user['subject']

            if old_subject == subject:
                await ctx.send(f'You are already in the {subject} subject. :x:')

                return 

            else:
                users.new_user(author_id, author_name, subject, subjects.get_ranks(user_subject=subject))

            if old_subject:
                await ctx.send(f'{author_name}, you have joined {subject} and left {old_subject}. :white_check_mark:')

            else:
                await ctx.send(f'{author_name}, you have joined {subject}. :white_check_mark:')

        else:
            users.new_user(author_id, author_name, subject, subjects.get_ranks(user_subject=subject))

            await ctx.send(f'{author_name}, you have joined {subject}. :white_check_mark:')

    else:
        await ctx.send(f'{subject}, is not a valid subject. :x:')


@client.command()
async def question(ctx):
    """Sends a question."""

    if not users.is_user(ctx.author.id):
        await ctx.send('You are not signed up for any subject. :x:')

    else:
        id_ = str(ctx.author.id)

        user = users.users[id_]

        quest_answer = user['subject-class'].get_quest_answer(id_)

        user['quest'] = quest_answer[0]
        user['answer'] = quest_answer[1]

        await ctx.send(user['quest'])

@client.command()
async def answer(ctx, ans):
    """Answers a question."""

    author_id = str(ctx.author.id)

    if not users.is_user(author_id):
        await ctx.send('You are not signed up for any subject. :x:')

    user = users.users[author_id]

    if user['quest'] is None:
        await ctx.send('You have no question. :x:')

    if user['answer'] == ans.lower():

        user['points'] += 1

        if user['points'] == user['subject-class'].quest_per_level:

            subjects.level_up(author_id)

            user['quest'] = None
            user['answer'] = None

            await ctx.send(f'Congrats, you are now in {user["subject-level"]}! :white_check_mark:')

        else:

            user['quest'] = None
            user['answer'] = None

            await ctx.send(f'Congrats, you got it right. You now have {user["points"]} points! :white_check_mark:')

    else:

        user['quest'] = None
        user['answer'] = None

        await ctx.send('Sad, your answer was incorrect! :x:')


@client.command()
@commands.has_role('iq.admin')
async def new_subject(ctx, name, levels, quest_per_level):
    """Makes a new subject."""

    name = name.lower()
    
    if name in custom_subjects.subjects.keys():
        await ctx.send('Subject already exists. :x:')
    
    else:
        levels = int(levels)
        quest_per_level = int(quest_per_level)

        subject = custom_subjects.Subject(name, levels, quest_per_level)

        custom_subjects.subjects[name] = subject
        custom_subjects.quests[name] = subject.subject_dict

        await ctx.send(f'Successfully created subject \'{name}\' with {levels} levels and with {quest_per_level} questions per level. :white_check_mark:')


@client.command()
@commands.has_role('iq.admin')
async def remove_subject(ctx, subject):
    """Removes a subject."""

    subject = subject.lower()

    if subject in custom_subjects.subjects.keys():
        # Removes the subject from the dictionary.
        del custom_subjects.subjects[subject.lower()]

        await ctx.send(f'Successfully removed the {subject} subject :white_check_mark:')

    else:
        await ctx.send(f"Subject {subject} does not exist. :x:")


@client.command()
@commands.has_role('iq.admin')
async def add_quest(ctx, subject, level, question, answer):
    """Adds a question to a specific subject."""

    question = question[1:-1]

    subject = subject.lower()
    level = int(level)
    
    if subject in custom_subjects.subjects.keys():
        if level > custom_subjects.subjects[subject].levels:
            await ctx.send(f'Max level is {custom_subjects.subjects[subject].levels}, not {level}. :x:')

            return

        quests_dict = custom_subjects.quests[subject][subject + ' level ' + str(level)]['questions']

        if question in quests_dict.keys():
            await ctx.send('Question already exist. :x:')

        elif len(quests_dict.keys()) + 1 > custom_subjects.subjects[subject].quest_per_level:
            await ctx.send(f'Too many questions in {subject}. {len(quests_dict.keys()) + 1} > {custom_subjects.subjects[subject].quest_per_level}. :x:')

        else:
            custom_subjects.subjects[subject].new_quest(level, question, answer)

            await ctx.send(f"The question was successfully added to the {subject} subject! :white_check_mark:")

    else:
        await ctx.send(f"Subject {subject} does not exist. :x:")


@client.command()
@commands.has_role('iq.admin')
async def remove_quest(ctx, subject, level, question):
    """Removes a question from a specific subject."""

    question = question[1:-1]

    subject = subject.lower()
    level = int(level)

    if subject in custom_subjects.subjects.keys():
        if level > custom_subjects.subjects[subject].levels:
            await ctx.send(f'Max level is {custom_subjects.subjects[subject].levels}, not {level}. :x:')

        elif question not in custom_subjects.quests[subject][subject + ' level ' + level]['questions'].keys():
            await ctx.send('Question does not exist. :x:')

        else:
            custom_subjects.subjects[subject].rm_quest(level, question)

            await ctx.send(f"The question was successfully removed from the {subject} subject! :white_check_mark:")

    else:
        await ctx.send(f"Subject {subject} does not exist. :x:")


client.run(TOKEN)
