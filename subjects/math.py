from .context import subjects
from .context import users
from discord.ext import commands
import discord

math_ranks = ['math', 'math level 1', 'math level 2']

math_questions = {
    'What is 3^5?': '243',
    '20 % of 2 is equal to?': '0.4',
    'What\'s sin(90 deg)?': '1',
    'What\'s 90 deg in radians?': '1.57',
    'If 15% of x is 45,what is 20% of x?': '60',
    'What is the value of the expression: 2^2 - 3^2 + 4^2': '11',
    'Is this: 3x^2 - 4x + 12 = 9 considered an equation?': 'yes',
    'What\'s sin(1.57 deg)?': '0.03',
}


class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Math online.')
    
    @commands.command()
    async def math(self, ctx):
        """A math question."""
        
        user = users.users[ctx.author.id]

        quest_answer = subjects.get_quest_answer(ctx.author.id, math_questions)

        user['quest'] = quest_answer[0]
        user['answer'] = quest_answer[1]
        
        await ctx.send(user['quest'])
    
    @commands.command()
    async def answer_math(self, ctx, ans):
        """Answers a math question."""

        author_id = ctx.author.id

        if not users.is_user(author_id):
            await ctx.send('You are not signed up for any subject. :x:')

        if users.users[ctx.author.id]['ans'] == ans.lower():
            users.users[author_id]['points'] += 1

            if users.users[author_id]['points'] == subjects.MAX_POINTS:
                subjects.level_up(author_id, users.users[author_id]['subject-ranks'])

                await ctx.send(f'Congrats, you are now in {users.users[author_id]["subject"]}! :white_check_mark:')

            else:
                await ctx.send(f'Congrats, you got it right. You now have {users.users[author_id]["points"]} points! :white_check_mark:')

        else:
            await ctx.send('Sad, your answer was incorrect! :x:')


def setup(client):
    client.add_cog(Math(client))