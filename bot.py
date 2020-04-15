from lib import users
from lib import subjects
from lib import files

from discord.ext import commands
import discord
import json
import os

TOKEN = json.load(open('token.json'))

client = commands.Bot(command_prefix='iq ')

# Handles cogs.
files.load_subjects(client, load_all=True)


@client.event
async def on_ready():
    print('Bot is online.')


@commands.has_role('.')
@client.command()
async def load(ctx, extension):
    client.load_extension(f'subjects.{extension}')


@commands.has_role('.')
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'subjects.{extension}')


@client.command()
async def join(ctx, subject):
    """Joins a subject."""

    author_id = ctx.author.id
    author_name = ctx.author.name

    subject = subject.lower()

    if subject in subjects.subjects:

        if users.is_user(author_id):
            user = users.users[author_id]

            old_subject = user['subject']

            users.new_user(author_id, author_name, subject, subjects.get_ranks(user_subject=subject))

            if old_subject == subject:
                await ctx.send(f'You are already in the {subject} subject. :x:')

            elif old_subject is not None:
                await ctx.send(f'{author_name}, you have joined {subject} and left {old_subject}. :white_check_mark:')

            else:
                await ctx.send(f'{author_name}, you have joined {subject}. :white_check_mark:')

        else:
            users.new_user(author_id, author_name, subject, subjects.get_ranks(user_subject=subject))

            await ctx.send(f'{author_name}, you have joined {subject}. :white_check_mark:')

    else:
        await ctx.send(f'{subject}, is not a valid subject. :x:')

@client.command()
async def answer(ctx, ans):
    """Answers a question."""
 
    author_id = ctx.author.id

    if not users.is_user(author_id):
        await ctx.send('You are not signed up for any subject. :x:')
    
    user = users.users[author_id]

    if user['quest'] is None:
        await ctx.send('You have no question. :x:')

    if user['answer'] == ans.lower():
        
        user['points'] += 1

        if user['points'] == subjects.MAX_POINTS:
            
            subjects.level_up(author_id)

            user['quest'] = None

            await ctx.send(f'Congrats, you are now in {user["subject-level"]}! :white_check_mark:')

        else:
            
            user['quest'] = None

            await ctx.send(f'Congrats, you got it right. You now have {user["points"]} points! :white_check_mark:')

    else:
        
        user['quest'] = None

        await ctx.send('Sad, your answer was incorrect! :x:')


@client.command()
@commands.has_role('.')
async def new_subject(ctx, name):
    """Makes a new subject."""

    name = name.lower()

    if os.path.exists(f'subjects/{name}.py'):
        await ctx.send('Subject already exists. :x:')

    else:
        subjects.subjects.append(name)

        subjects.ranks[name] = {
            name + '_ranks': [name, name + ' level 2', name + ' level 3'],

            name: {
                'questions': {}
            },

            name + ' level 2': {
                'questions': {}
            },

            name + ' level 3': {
                'questions': {}
            },
        }

        # Writes the new subject.
        files.new_subject_file(name, subjects.sbj_code(name))

        # Updates every file in data/
        files.update_data()

        await ctx.send(f'Successfully made subject \'{name}\'! :white_check_mark:')


@client.command()
@commands.has_role('.')
async def add_quest(ctx, subject, level, question, answer):
    """Adds a question to a specific subject."""

    subject = subject.lower()
    
    if int(level) > 3 or int(level) < 1:
        await ctx.send('IQ only supports level 1, 2 and 3. :x:')

    if subject in subjects.ranks.keys():
        subject_dict = subjects.ranks[subject]
        
        if int(level) == 1:
            subject_dict[subject]['questions'][question.replace('"', '')] = answer

            files.update_data()

            try:
                files.load_subjects(client, load=subject)
            except Exception:
                pass


            await ctx.send(f"The question was successfully added to the {subject} subject! :white_check_mark:")

        else:
            for level_name in subject_dict.keys():
                if level in level_name:
                    subject_dict[level_name]['questions'][question.replace('"', '')] = answer
                    
                    files.update_data()
                    
                    try:
                        files.load_subjects(client, load=subject)
                    except Exception:
                        pass

                    await ctx.send(f"The question was successfully added to the {subject} subject! :white_check_mark:")
    
    else:
        await ctx.send(f"Subject '{subject}' is not a valid subject. :x:")


@client.command()
@commands.has_role('.')
async def remove_subject(ctx, subject):
    """Removes a subject."""

    subject = subject.lower()

    if subject in subjects.ranks.keys():
        # Removes the subject from the dictionary.
        del subjects.ranks[subject.lower()]

        # Removes the subject from the list.
        subjects.subjects.remove(subject)

        # Updates the files.
        files.update_data()

        os.remove(f'subjects/{subject}.py')

        await ctx.send(f'Successfully removed subject \'{subject}\'! :white_check_mark:')
    
    else:
        await ctx.send(f'Subject \'{subject}\' is not a valid subject. :x:')


client.run(TOKEN)
