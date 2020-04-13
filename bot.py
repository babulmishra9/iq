from lib import users
from lib import subjects

from discord.ext import commands
import discord
import json
import os

TOKEN = json.load(open('token.json'))

client = commands.Bot(command_prefix='iq ')

# Handles cogs.
for filename in os.listdir('./subjects'):
    if filename.endswith('.py'):
        if filename == '__init__.py' or filename == 'context.py':
            pass

        else:
            client.load_extension(f'subjects.{filename[:-3]}')

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
            
            old_subject = users.users[author_id]['subject']

            users.users[author_id]['subject'] = subject

            if old_subject == subject:
                await ctx.send(f'You are already in the {subject} subject. :x:')

            elif old_subject is not None:
                await ctx.send(f'{author_name}, you have joined {subject} and left {old_subject}. :white_check_mark:') 

            else:
                await ctx.send(f'{author_name}, you have joined {subject}. :white_check_mark:')

        else:
            users.new_user(author_id, author_name, subject)

            await ctx.send(f'{author_name}, you have joined {subject}. :white_check_mark:')

    else:
        await ctx.send(f'{subject}, is not a valid subject. :x:')


client.run(TOKEN)
