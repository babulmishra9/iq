from context import subjects
from discord.ext import commands
import discord

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
        self.quest = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Math online.')
    
    async def math(self, ctx):
        """A math question."""
        
        self.quest = subjects.get_quest_answer(math_questions)[0]

        await ctx.send(self.quest)


def setup(client):
    client.add_cog(Math(client))