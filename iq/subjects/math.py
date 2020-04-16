from .context import subjects
from .context import users
from .context import files
from discord.ext import commands
import discord


class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Math online.')

    @commands.command()
    async def math(self, ctx):
        """A math question."""

        if not users.is_user(ctx.author.id):
            await ctx.send('You are not signed up for any subject. :x:')

        elif users.users[str(ctx.author.id)]['subject'] != 'math':      
            await ctx.send('You are not joined math. :x:')

        else:
            id_ = str(ctx.author.id)

            user = users.users[id_]

            quest_answer = subjects.get_quest_answer(id_)

            user['quest'] = quest_answer[0]
            user['answer'] = quest_answer[1]

            files.update_users()

            await ctx.send(user['quest'])


def setup(client):
    client.add_cog(Math(client))